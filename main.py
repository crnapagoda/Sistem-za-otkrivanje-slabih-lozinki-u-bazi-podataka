"""
Ovaj Python kod predstavlja sistem za analizu lozinki, osmišljen da detektuje slabe lozinke, ocenjuje jačinu lozinke, generiše predloge za unapređenje, identifikuje duplikate, proveri kompromitovane lozinke i vizualizuje rezultate analize, kao i da čuva izveštaj u Excel fajlu.

Funkcionalnosti:
- Učitavanje baza lozinki iz CSV fajlova.
- Provera jačine lozinki na osnovu dužine, kompleksnosti i prisustva specijalnih karaktera.
- Detekcija dupliranih lozinki i provera kompromitovanih lozinki u odnosu na poznatu bazu rockyou.txt.
- Generisanje detaljnih izveštaja u Excel formatu.
- Vizuelni prikaz podataka o jakim i slabim lozinkama.
- Generisanje predloga za poboljšanje slabih lozinki.
- Procenjivanje lozinki na osnovu unapred definisanih kriterijuma.

Tehnologije i biblioteke:
- os, re i datetime za rad sa datotekama, regularne izraze i rad sa vremenom.
- pandas za manipulaciju i analizu podataka.
- matplotlib.pyplot za vizualizaciju rezultata.

Program koristi interaktivni pristup kroz meni kako bi omogućio korisniku da bira opcije za analizu i generisanje izveštaja.
"""

import os
import re
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Funkcija za listanje dostupnih baza lozinki iz foldera
def list_password_files(folder_path):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        if not files:
            print("Nema dostupnih baza lozinki u folderu.")
            return []
        print("\nDostupne baze lozinki:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        return files
    except FileNotFoundError:
        print(f"Folder '{folder_path}' ne postoji.")
        return []

# Funkcija za izbor baze lozinki koje sa nalaze u folderu
def choose_password_file(files):
    while True:
        try:
            choice = int(input("\nUnesite broj baze lozinki za analizu: ")) - 1
            if 0 <= choice < len(files):
                return files[choice]
            else:
                print("Uneli ste nevažeći broj. Pokušajte ponovo.")
        except ValueError:
            print("Molimo unesite broj.")

# Funkcija za učitavanje lozinki iz CSV fajla
def load_passwords(file_path):
    df = pd.read_csv(file_path)
    print("Učitane lozinke:")
    print(df)
    return df

# Funkcija za proveru dužine lozinke
def check_length(password, min_length=8):
    return len(password) >= min_length

# Funkcija za proveru kompleksnosti lozinke
def check_complexity(password):
    if (re.search(r'[a-z]', password) and
        re.search(r'[A-Z]', password) and
        re.search(r'\d', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    return False

# Funkcija za analizu svih lozinki u tabeli
def analyze_passwords(df):
    df['length_check'] = df['password'].apply(lambda pwd: check_length(pwd))
    df['complexity_check'] = df['password'].apply(lambda pwd: check_complexity(pwd))
    df['is_strong'] = df['length_check'] & df['complexity_check']
    return df

# Funkcija za generisanje predloga unapređenja lozinki
def generate_password_suggestions(password):
    suggestions = []
    if not check_length(password):
        suggestions.append("Povećajte dužinu lozinke na najmanje 8 karaktera.")
    if not re.search(r'[a-z]', password):
        suggestions.append("Dodajte mala slova.")
    if not re.search(r'[A-Z]', password):
        suggestions.append("Dodajte velika slova.")
    if not re.search(r'\d', password):
        suggestions.append("Dodajte brojeve.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        suggestions.append("Dodajte specijalne karaktere.")
    return " ".join(suggestions)

# Funkcija za dodavanje predloga unapređenja lozinki u DataFrame
def add_password_suggestions(df):
    df['suggestions'] = df['password'].apply(generate_password_suggestions)
    return df    

# Funkcija za generisanje izveštaja 
def generate_report(df):
    total_passwords = len(df)
    weak_passwords = len(df[df['is_strong'] == False])
    strong_passwords = total_passwords - weak_passwords

    print("\nIzveštaj o lozinkama:")
    print(f"Ukupno lozinki: {total_passwords}")
    print(f"Slabe lozinke: {weak_passwords}")
    print(f"Jake lozinke: {strong_passwords}")

    print("\nDetalji o slabim lozinkama:")
    print(df[df['is_strong'] == False])

# Funkcija za detekciju duplikata lozinki
def find_duplicates(df):
    duplicate_passwords = df['password'].value_counts()
    duplicates = duplicate_passwords[duplicate_passwords > 1]
    if not duplicates.empty:
        print("\nPronađene duplirane lozinke:")
        print(duplicates)
    else:
        print("\nNema dupliranih lozinki.")

# Funkcija za proveru kompromitovanih lozinki
def check_compromised_passwords(df, compromised_file):
    with open(compromised_file, 'r', encoding='latin-1') as file:
        compromised_passwords = set(file.read().splitlines())
    df['compromised'] = df['password'].apply(lambda pwd: pwd in compromised_passwords)
    print("\nLozinke pronađene u kompromitovanoj bazi:")
    print(df[df['compromised']])

# Funkcija za vizuelizaciju analize lozinki
def visualize_password_analysis(df):
    total_passwords = len(df)
    weak_passwords = len(df[df['is_strong'] == False])
    strong_passwords = total_passwords - weak_passwords

    # Pie chart za odnos jakih i slabih lozinki
    labels = ['Slabe lozinke', 'Jake lozinke']
    sizes = [weak_passwords, strong_passwords]
    colors = ['#FF9999', '#99FF99']
    explode = (0.1, 0)  

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=explode)
    plt.title("Odnos jakih i slabih lozinki")
    plt.show()

    # Bar chart za duplikate lozinki
    duplicates = df['password'].value_counts()
    duplicates = duplicates[duplicates > 1]

    if not duplicates.empty:
        plt.figure(figsize=(8, 6))
        duplicates.plot(kind='bar', color='#FFCC99')
        plt.title("Duplirane lozinke i njihova učestalost")
        plt.xlabel("Lozinke")
        plt.ylabel("Broj pojavljivanja")
        plt.show()

# Funkcija za ocenjivanje lozinke
def password_score(password):
    score = 5  # Početna ocena (5 - lose, 10 - odlično)
    
    # Provera dužine lozinke
    if len(password) >= 12: 
        score += 1

    # Provera prisustva malih i velikih slova
    if re.search(r'[a-z]', password): 
        score += 1
    if re.search(r'[A-Z]', password): 
        score += 1

    # Provera prisustva brojeva
    if re.search(r'\d', password): 
        score += 1

    # Provera prisustva specijalnih karaktera
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): 
        score += 1

    # Penalizacija ako lozinka sadrži uobičajene fraze ili šablone
    common_patterns = ['123456', 'password', 'qwerty', 'iloveyou', 'admin']
    if any(pattern in password.lower() for pattern in common_patterns): 
        score -= 2  # Oduzimamo 2 poen

    # Osiguravamo da je rezultat između 5 i 10
    score = max(5, min(score, 10))

    return score

# Funkcija za cuvanje rezultata u Excel
def export_to_excel(df, base_filename):
    required_columns = ['id', 'username', 'password', 'is_strong', 'score', 'compromised', 'suggestions']
    df_to_export = df[required_columns] if all(col in df.columns for col in required_columns) else df
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'{base_filename}_izvestaj_{timestamp}.xlsx'
    df_to_export.to_excel(output_file, index=False)
    print(f"Izveštaj je sačuvan u fajlu: {output_file}")


folder_path = 'password_bases'  # Putanja do foldera sa bazama lozinki
password_files = list_password_files(folder_path)
selected_file = choose_password_file(password_files)
file_path = os.path.join(folder_path, selected_file)
password_data = load_passwords(file_path)
analyzed_data = analyze_passwords(password_data)
analyzed_data = add_password_suggestions(analyzed_data)
generate_report(analyzed_data)
find_duplicates(password_data)

# Provera kompromitovanih lozinki naspram rockzou.txt (baza kompromitovanih lozinki)
rockyou_file = 'rockyou.txt'  
check_compromised_passwords(analyzed_data, rockyou_file)

# Dodavanje kolone sa skorom u dataframe
analyzed_data['score'] = analyzed_data['password'].apply(password_score)

# Prikaz ažuriranih podataka
print("\nRezultati sa skorovima lozinki:")
print(analyzed_data[['id', 'username', 'password', 'score']])

# Ažurirani izveštaj nakon provere
print("\nAžurirani podaci sa informacijama o kompromitovanim lozinkama:")
print(analyzed_data[['id', 'username', 'password', 'is_strong', 'score', 'compromised']])

# Meni sa opcijama nakon analize
def handle_user_choice(analyzed_data, base_filename):
    while True:
        print("\nIzaberite opciju:")
        print("1. Vizuelni prikaz analize lozinki")
        print("2. Sačuvaj izveštaj u Excel fajl")
        print("3. Prekid rada")
        choice = input("\nUnesite broj opcije: ")

        if choice == "1":
            visualize_password_analysis(analyzed_data)
        elif choice == "2":
            export_to_excel(analyzed_data, base_filename)
        elif choice == "3":
            print("Izlazak iz programa :(")
            break
        else:
            print("Nevažeća opcija. Pokušajte ponovo.")

base_filename = os.path.splitext(selected_file)[0]
handle_user_choice(analyzed_data, base_filename)