# Weak Password Detection System in Database

## Project Overview

This project is designed as a tool for analyzing and assessing the security of passwords within databases. The goal is to identify passwords that do not meet basic security standards and to suggest ways to improve them.

## Features

### Password Analysis and Evaluation:
- **Length Check**: Ensures passwords meet a minimum length requirement.
- **Complexity Check**: Validates that passwords contain a combination of lowercase and uppercase letters, numbers, and special characters.
- **Comparison with Compromised Passwords**: Checks passwords against a list of known compromised passwords (rockyou.txt).
- **Scoring System**: Each password receives a score from 5 to 10 based on predefined criteria.

### Reporting:
- **Excel Report Generation**: Creates Excel files with detailed information about password security.
- **Duplicate Detection**: Identifies duplicate passwords and generates statistics on strong and weak passwords.

### Improvement Suggestions:
- **Automatic Recommendations**: Generates suggestions for strengthening weak passwords.

## Installation

To run this project, ensure you have Python installed along with the required libraries. You can install the necessary libraries using pip:
```bash
pip install pandas seaborn matplotlib PyQt6
```


## Usage

1. Launch the application.
2. Click on "Select File" to choose a CSV file containing passwords.
3. Click on "Analyze Passwords" to evaluate the passwords.
4. View the results in the table and log output.
5. Use the "Visualize" button to see graphical representations of password strength and complexity.
6. Save the report by clicking on "Save Report".
