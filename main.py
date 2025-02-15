import sys
import os
import re
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QTextEdit
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# Funkcije za analizu lozinki (same as before)
def check_length(password, min_length=8):
    return len(password) >= min_length

def check_complexity(password):
    return bool(re.search(r'[a-z]', password) and
                re.search(r'[A-Z]', password) and
                re.search(r'\d', password) and
                re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

def password_score(password):
    score = 5
    if len(password) >= 12: score += 1
    if re.search(r'[a-z]', password): score += 1
    if re.search(r'[A-Z]', password): score += 1
    if re.search(r'\d', password): score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 1
    common_patterns = ['123456', 'password', 'qwerty', 'admin']
    if any(pattern in password.lower() for pattern in common_patterns): score -= 2
    return max(5, min(score, 10))

def analyze_passwords(df):
    df['length_check'] = df['password'].apply(check_length)
    df['complexity_check'] = df['password'].apply(check_complexity)
    df['is_strong'] = df['length_check'] & df['complexity_check']
    df['score'] = df['password'].apply(password_score)
    return df

def export_to_excel(df, base_filename):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{base_filename}_izvestaj_{timestamp}.xlsx"
    df.to_excel(output_file, index=False)
    return output_file


# Funkcija za proveru lozinki naspram rockyou.txt
def check_compromised_passwords(df, rockyou_file):
    with open(rockyou_file, 'r', encoding='latin-1') as file:
        compromised_passwords = set(file.read().splitlines())
    
    df['is_compromised'] = df['password'].apply(lambda x: x in compromised_passwords)
    return df


# GUI aplikacija
class PasswordAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analiza Lozinki")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Izaberite CSV fajl sa lozinkama:")
        self.label.setFont(QFont("Arial", 12))
        self.label.setStyleSheet("color: #2e3d49;")
        self.layout.addWidget(self.label)

        self.select_file_button = QPushButton("Odaberi fajl")
        self.select_file_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; padding: 8px 12px;")
        self.select_file_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.select_file_button)

        self.analyze_button = QPushButton("Analiziraj lozinke")
        self.analyze_button.setEnabled(False)
        self.analyze_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 8px 12px;")
        self.analyze_button.clicked.connect(self.analyze_passwords)
        self.layout.addWidget(self.analyze_button)

        self.result_table = QTableWidget()
        self.result_table.setStyleSheet("QTableWidget {background-color: #f9f9f9; border: 1px solid #ccc; font-size: 12px;}")
        self.layout.addWidget(self.result_table)

        self.visualize_button = QPushButton("Prikaži grafičku analizu")
        self.visualize_button.setEnabled(False)
        self.visualize_button.setStyleSheet("background-color: #9C27B0; color: white; border-radius: 5px; padding: 8px 12px;")
        self.visualize_button.clicked.connect(self.visualize_passwords)
        self.layout.addWidget(self.visualize_button)

        self.export_button = QPushButton("Sačuvaj izveštaj")
        self.export_button.setEnabled(False)
        self.export_button.setStyleSheet("background-color: #FF5722; color: white; border-radius: 5px; padding: 8px 12px;")
        self.export_button.clicked.connect(self.export_report)
        self.layout.addWidget(self.export_button)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #2e3d49; color: white; font-size: 12px; padding: 10px;")
        self.layout.addWidget(self.log_output)

        self.setLayout(self.layout)
        self.df = None
        self.file_path = ""

    def open_file_dialog(self):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Odaberi CSV fajl", "", "CSV Files (*.csv)", options=options)
        
        if file_path:
            self.file_path = file_path
            self.label.setText(f"Odabrani fajl: {os.path.basename(file_path)}")
            self.analyze_button.setEnabled(True)

    def analyze_passwords(self):
        if not self.file_path:
            return
        
        try:
            self.df = pd.read_csv(self.file_path)
            if "password" not in self.df.columns:
                self.log_output.append("Greška: Fajl ne sadrži kolonu 'password'")
                return

            self.df = analyze_passwords(self.df)

            # Provera lozinki naspram rockyou.txt
            rockyou_file = 'rockyou.txt'
            self.df = check_compromised_passwords(self.df, rockyou_file)
            
            self.display_results()
            self.visualize_button.setEnabled(True)
            self.export_button.setEnabled(True)

        except Exception as e:
            self.log_output.append(f"Greška pri učitavanju: {str(e)}")

    def display_results(self):
        self.result_table.clear()
        self.result_table.setColumnCount(len(self.df.columns))
        self.result_table.setRowCount(len(self.df))
        self.result_table.setHorizontalHeaderLabels(self.df.columns)

        for row_idx, row in self.df.iterrows():
            for col_idx, value in enumerate(row):
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        self.result_table.resizeColumnsToContents()

    def visualize_passwords(self):
        if self.df is None:
            return

        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        lengths = self.df['password'].apply(len)
        sns.histplot(lengths, kde=True, ax=ax[0])
        ax[0].set_title('Distribucija dužine lozinki')

        complexity = self.df['complexity_check'].fillna(False).astype(int)

        sns.countplot(x=complexity, ax=ax[1])
        ax[1].set_title('Kompleksnost lozinki')
        ax[1].set_xticks([0, 1])
        ax[1].set_xticklabels(["Slabe", "Jake"])

        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)
        self.canvas.draw()

    def export_report(self):
        if self.df is None:
            return
        
        base_filename = os.path.splitext(os.path.basename(self.file_path))[0]
        file_path = export_to_excel(self.df, base_filename)
        self.log_output.append(f"Izveštaj sačuvan: {file_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordAnalyzerApp()
    window.show()
    sys.exit(app.exec())
