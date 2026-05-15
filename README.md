<!-- =========================================================
     DataCleaner Pro - README
     Developed by Matias Isaac Frutos Gonzalez
     ========================================================= -->

<div align="center">

# 🧹 DataCleaner Pro

### Clean, analyze and export messy Excel, CSV and TXT files from a local Python desktop app.

<br>

![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=900&color=2563EB&center=true&vCenter=true&width=900&lines=Python+Desktop+Data+Cleaner;Excel+%7C+CSV+%7C+TXT+File+Processing;Pandas+%7C+CustomTkinter+%7C+OpenPyXL;Analyze+Data+Quality;Clean+Messy+Spreadsheets;Export+Clean+Files+to+XLSX+or+CSV)

<br>

<img src="https://img.shields.io/badge/status-MVP%20Functional-brightgreen" />
<img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/UI-CustomTkinter-2563EB" />
<img src="https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white" />
<img src="https://img.shields.io/badge/Excel-OpenPyXL-217346" />
<img src="https://img.shields.io/badge/Tests-Pytest-0A9EDC?logo=pytest&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-black" />

</div>

---

## 📌 Overview

**DataCleaner Pro** is a local desktop application built with **Python** that helps users clean, analyze and export messy data files.

It is designed for developers, data analysts, administrative teams and businesses that work with spreadsheets or text-based data files and need to prepare them before importing them into databases, CRMs, ERPs or reporting systems.

The application allows users to load files, preview their content, analyze data quality issues, apply automatic cleaning rules and export a clean version of the dataset.

---

## 🎯 Purpose

The main purpose of **DataCleaner Pro** is to reduce manual spreadsheet cleaning work and improve data quality before using files in production workflows.

Many business files contain problems such as:

- Empty rows
- Empty columns
- Duplicated records
- Invalid emails
- Inconsistent dates
- Mixed column names
- Extra spaces in text fields
- CSV files with wrong separators
- Old `.xls` files exported from legacy systems
- Data that looks correct visually but breaks when imported into another system

**DataCleaner Pro** solves this by providing a simple, local and practical desktop tool.

---

## ✨ Features

### 📂 File Loading

- Load `.xlsx` files
- Load `.xls` files
- Load `.csv` files
- Load `.txt` files
- Detect common CSV/TXT separators
- Handle legacy `.xls` files with fallback strategies
- Display file metadata

### 👀 Data Preview

- Show loaded file information
- Display row and column count
- Show memory usage
- Preview the first rows
- Limit table preview for better performance
- Display detected encoding and separator when available

### 📊 Data Analysis

DataCleaner Pro analyzes the loaded dataset and detects:

- Total rows
- Total columns
- Total cells
- Empty cells
- Empty rows
- Empty columns
- Duplicated rows
- Data types by column
- Empty percentage by column
- Quality score
- Risk level
- Warnings
- Cleaning recommendations

### 🛡️ Advanced Validations

The validation engine checks for:

- Possible invalid emails
- Date inconsistencies
- Columns with too many empty values
- Duplicate or equivalent column names
- Columns with dominant repeated values
- Risk points that affect the final quality score

### 🧽 Automatic Cleaning

The cleaning engine can apply safe rules such as:

- Remove empty rows
- Remove empty columns
- Remove duplicated rows
- Trim text values
- Normalize column names
- Normalize missing values
- Normalize detected date columns
- Reset row indexes after cleaning

### 📤 Export

Export clean data to:

- `.xlsx`
- `.csv`

The exported files are saved by default in:

```text
data/output/
```

### 🧾 Reports

After exporting, DataCleaner Pro generates a process report in:

```text
data/reports/
```

The report includes:

- Original file information
- Analysis result
- Cleaning actions
- Export details
- Warnings and recommendations

### 🪵 Logs

The application saves logs in:

```text
logs/app.log
```

Logs include:

- App startup
- Export events
- Errors
- Critical exceptions

---

## 🧠 How It Works

```text
User selects a file
        ↓
File is loaded with Pandas
        ↓
Data is previewed in the desktop UI
        ↓
Analysis engine detects data quality issues
        ↓
Validation engine checks advanced risks
        ↓
Cleaning engine applies automatic rules
        ↓
User exports clean file
        ↓
Report and logs are generated
```

---

## 🏗️ Architecture

DataCleaner Pro uses a clean layered architecture.

```text
datacleaner-pro/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── core/
│   │   ├── file_loader.py
│   │   ├── data_analyzer.py
│   │   ├── data_cleaner.py
│   │   ├── data_exporter.py
│   │   ├── report_builder.py
│   │   └── validation_engine.py
│   │
│   ├── models/
│   │   ├── file_model.py
│   │   ├── analysis_result.py
│   │   ├── cleaning_result.py
│   │   └── export_result.py
│   │
│   ├── services/
│   │   ├── file_service.py
│   │   ├── analysis_service.py
│   │   ├── cleaning_service.py
│   │   ├── export_service.py
│   │   └── log_service.py
│   │
│   ├── ui/
│   │   ├── app_window.py
│   │   ├── sidebar.py
│   │   ├── topbar.py
│   │   ├── dashboard_view.py
│   │   ├── file_preview_view.py
│   │   ├── analysis_view.py
│   │   ├── cleaning_view.py
│   │   ├── export_view.py
│   │   ├── components.py
│   │   └── styles.py
│   │
│   └── utils/
│       ├── file_utils.py
│       ├── text_utils.py
│       ├── date_utils.py
│       ├── dataframe_utils.py
│       └── constants.py
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── themes/
│
├── data/
│   ├── input/
│   ├── output/
│   ├── samples/
│   └── reports/
│
├── docs/
│   ├── project-overview.md
│   ├── architecture.md
│   ├── usage-guide.md
│   └── roadmap.md
│
├── logs/
│   └── app.log
│
├── scripts/
│   ├── run_dev.bat
│   ├── clean_outputs.bat
│   └── build_exe.bat
│
├── tests/
│   ├── test_file_loader.py
│   ├── test_data_analyzer.py
│   ├── test_data_cleaner.py
│   └── test_data_exporter.py
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run.py
```

---

## 📁 Folder Explanation

### `app/`

Main application source code.

### `app/core/`

Contains the business logic.

| File | Purpose |
|---|---|
| `file_loader.py` | Loads Excel, CSV and TXT files |
| `data_analyzer.py` | Detects basic data quality issues |
| `data_cleaner.py` | Cleans the loaded DataFrame |
| `data_exporter.py` | Exports clean data to XLSX or CSV |
| `validation_engine.py` | Runs advanced validation checks |
| `report_builder.py` | Generates process reports |

### `app/models/`

Contains internal data structures.

| File | Purpose |
|---|---|
| `file_model.py` | Represents the selected file |
| `analysis_result.py` | Represents the data analysis result |
| `cleaning_result.py` | Represents the cleaning process result |
| `export_result.py` | Represents the export result |

### `app/services/`

Connects the UI layer with the core logic.

| File | Purpose |
|---|---|
| `file_service.py` | Manages the active file and DataFrames |
| `analysis_service.py` | Runs analysis and validations |
| `cleaning_service.py` | Runs automatic cleaning |
| `export_service.py` | Exports files and generates reports |
| `log_service.py` | Handles application logging |

### `app/ui/`

Desktop interface built with **CustomTkinter**.

| File | Purpose |
|---|---|
| `app_window.py` | Main desktop window |
| `sidebar.py` | Left navigation menu |
| `topbar.py` | Header bar |
| `dashboard_view.py` | Main dashboard |
| `file_preview_view.py` | File loading and preview screen |
| `analysis_view.py` | Data quality analysis screen |
| `cleaning_view.py` | Automatic cleaning screen |
| `export_view.py` | Export screen |
| `components.py` | Reusable UI components |
| `styles.py` | Colors, fonts and visual settings |

### `app/utils/`

Reusable helper functions.

| File | Purpose |
|---|---|
| `file_utils.py` | File path and extension utilities |
| `text_utils.py` | Text and column name normalization |
| `date_utils.py` | Date detection and normalization |
| `dataframe_utils.py` | DataFrame preview and metrics helpers |
| `constants.py` | Shared constants |

---

## 🧰 Tech Stack

| Area | Technology |
|---|---|
| Language | Python |
| UI | CustomTkinter |
| Data processing | Pandas |
| Excel reading/writing | OpenPyXL |
| Legacy Excel support | xlrd |
| Date parsing | python-dateutil |
| Testing | Pytest |
| Packaging | PyInstaller |
| Version control | Git / GitHub |

---

## ✅ Requirements

Before installing the project, make sure you have:

- Python 3.11 or higher
- Git
- pip
- Windows, Linux or macOS

Recommended:

- VS Code
- GitHub Desktop or terminal Git
- A virtual environment

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/datacleaner-pro.git
```

### 2. Enter the project folder

```bash
cd datacleaner-pro
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python run.py
```

On Windows, you can also use:

```bash
scripts\run_dev.bat
```

---

## 🧪 Run Tests

```bash
pytest
```

The test suite validates:

- CSV loading
- TXT loading
- XLSX loading
- Data analysis
- Duplicate detection
- Cleaning behavior
- Export to CSV
- Export to XLSX

---

## 📦 Build Windows EXE

To generate a Windows executable:

```bash
scripts\build_exe.bat
```

The executable will be generated in:

```text
dist/
```

---

## 📥 Supported Input Formats

```text
.xlsx
.xls
.csv
.txt
```

---

## 📤 Supported Output Formats

```text
.xlsx
.csv
```

---

## 🖥️ Application Screens

### Dashboard

General overview of the workflow and current file state.

### File Preview

Allows the user to select and preview a file.

### Analysis

Displays data quality metrics, warnings, recommendations and risk level.

### Cleaning

Allows the user to apply automatic cleaning rules.

### Export

Allows the user to export the cleaned file to XLSX or CSV.

---

## 📊 Quality Score

DataCleaner Pro calculates a quality score based on:

- Empty cells
- Empty rows
- Empty columns
- Duplicated rows
- Advanced validation risks
- Invalid emails
- Inconsistent dates
- High-empty columns

Risk levels:

```text
85 - 100  -> Low risk
65 - 84   -> Medium risk
0 - 64    -> High risk
```

---

## 🧽 Cleaning Rules

The automatic cleaner can:

```text
Remove empty rows
Remove empty columns
Remove duplicates
Trim text values
Normalize column names
Normalize missing values
Normalize date columns
```

Example:

```text
" Customer Name " -> customer_name
"  John Smith  "  -> John Smith
"15/05/2026"     -> 2026-05-15
```

---

## 🧾 Generated Reports

After exporting a clean file, the app creates a report in:

```text
data/reports/
```

Report example:

```text
DATA CLEANER PRO - PROCESS REPORT

File:
- Name
- Path
- Extension
- Rows
- Columns

Analysis:
- Empty cells
- Empty rows
- Duplicates
- Quality score
- Risk level

Cleaning:
- Removed rows
- Removed columns
- Removed duplicates
- Normalized columns
- Normalized dates

Export:
- Output path
- Format
- Rows
- Columns
- Final file size
```

---

## 🪵 Logs

Logs are stored in:

```text
logs/app.log
```

Example log events:

```text
Application started
Export started
Export completed
Report generated
Critical error detected
```

---

## 🧭 Workflow

```text
1. Open DataCleaner Pro
2. Load an Excel, CSV or TXT file
3. Preview the loaded data
4. Go to Analysis
5. Review quality score and warnings
6. Go to Cleaning
7. Run automatic cleaning
8. Go to Export
9. Export clean file
10. Review generated report
```

---

## 📌 Example Use Cases

### CRM / ERP Imports

Prepare customer files before importing them into a CRM or ERP.

### Administrative Data Cleaning

Clean spreadsheets received from internal teams, vendors or clients.

### Database Migration

Prepare CSV or Excel files before inserting them into PostgreSQL, MySQL or another database.

### Reporting

Clean messy operational files before building dashboards or business reports.

### Portfolio Project

Showcase a real Python desktop application with business value.

---

## 🧱 Development Stages

### Stage 1

Project base, configuration and initial execution.

### Stage 2

Desktop UI with CustomTkinter.

### Stage 3

Dashboard and global file state.

### Stage 4

Real file loading and preview.

### Stage 5

Data quality analysis.

### Stage 6

Automatic cleaning engine.

### Stage 7

Advanced validation engine.

### Stage 8

Export to XLSX and CSV.

### Stage 9

Reports and logs.

### Stage 10

Tests, scripts, documentation and GitHub-ready release.

---

## 🛣️ Roadmap

### Version 0.2.0

- Dark mode
- Better table component
- Multi-sheet Excel support
- Manual column renaming
- Column selector before export
- Improved CSV detection

### Version 0.3.0

- Export to JSON
- Export to SQL
- PostgreSQL connection
- MySQL connection
- Saved cleaning profiles

### Version 0.4.0

- PDF reports
- Before/after comparison
- Data quality dashboard
- Custom validation rules
- Duplicate detection by selected columns

### Version 1.0.0

- Stable Windows executable
- Polished UI
- Full documentation
- Real sample datasets
- Production-ready portfolio release

---

## 🧑‍💻 Author

Developed by **Matias Isaac Frutos Gonzalez**.

```text
Full Stack Developer
Python · JavaScript · Node.js · PostgreSQL · Automation · Desktop Tools
```

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

### 🧹 DataCleaner Pro

**Turn messy files into clean, useful and export-ready data.**

<br>

![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=900&color=16A34A&center=true&vCenter=true&width=900&lines=Load+Data;Analyze+Quality;Clean+Automatically;Export+Clean+Files;Generate+Reports)

</div>
The application allows users to load files, preview their content, analyze data quality issues, apply automatic cleaning rules and export a clean version of the dataset.

---

## 🎯 Purpose

The main purpose of **DataCleaner Pro** is to reduce manual spreadsheet cleaning work and improve data quality before using files in production workflows.

Many business files contain problems such as:

- Empty rows
- Empty columns
- Duplicated records
- Invalid emails
- Inconsistent dates
- Mixed column names
- Extra spaces in text fields
- CSV files with wrong separators
- Old `.xls` files exported from legacy systems
- Data that looks correct visually but breaks when imported into another system

**DataCleaner Pro** solves this by providing a simple, local and practical desktop tool.

---

## ✨ Features

### 📂 File Loading

- Load `.xlsx` files
- Load `.xls` files
- Load `.csv` files
- Load `.txt` files
- Detect common CSV/TXT separators
- Handle legacy `.xls` files with fallback strategies
- Display file metadata

### 👀 Data Preview

- Show loaded file information
- Display row and column count
- Show memory usage
- Preview the first rows
- Limit table preview for better performance
- Display detected encoding and separator when available

### 📊 Data Analysis

DataCleaner Pro analyzes the loaded dataset and detects:

- Total rows
- Total columns
- Total cells
- Empty cells
- Empty rows
- Empty columns
- Duplicated rows
- Data types by column
- Empty percentage by column
- Quality score
- Risk level
- Warnings
- Cleaning recommendations

### 🛡️ Advanced Validations

The validation engine checks for:

- Possible invalid emails
- Date inconsistencies
- Columns with too many empty values
- Duplicate or equivalent column names
- Columns with dominant repeated values
- Risk points that affect the final quality score

### 🧽 Automatic Cleaning

The cleaning engine can apply safe rules such as:

- Remove empty rows
- Remove empty columns
- Remove duplicated rows
- Trim text values
- Normalize column names
- Normalize missing values
- Normalize detected date columns
- Reset row indexes after cleaning

### 📤 Export

Export clean data to:

- `.xlsx`
- `.csv`

The exported files are saved by default in:

```text
data/output/
```

### 🧾 Reports

After exporting, DataCleaner Pro generates a process report in:

```text
data/reports/
```

The report includes:

- Original file information
- Analysis result
- Cleaning actions
- Export details
- Warnings and recommendations

### 🪵 Logs

The application saves logs in:

```text
logs/app.log
```

Logs include:

- App startup
- Export events
- Errors
- Critical exceptions

---

## 🧠 How It Works

```text
User selects a file
        ↓
File is loaded with Pandas
        ↓
Data is previewed in the desktop UI
        ↓
Analysis engine detects data quality issues
        ↓
Validation engine checks advanced risks
        ↓
Cleaning engine applies automatic rules
        ↓
User exports clean file
        ↓
Report and logs are generated
```

---

## 🏗️ Architecture

DataCleaner Pro uses a clean layered architecture.

```text
datacleaner-pro/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── core/
│   │   ├── file_loader.py
│   │   ├── data_analyzer.py
│   │   ├── data_cleaner.py
│   │   ├── data_exporter.py
│   │   ├── report_builder.py
│   │   └── validation_engine.py
│   │
│   ├── models/
│   │   ├── file_model.py
│   │   ├── analysis_result.py
│   │   ├── cleaning_result.py
│   │   └── export_result.py
│   │
│   ├── services/
│   │   ├── file_service.py
│   │   ├── analysis_service.py
│   │   ├── cleaning_service.py
│   │   ├── export_service.py
│   │   └── log_service.py
│   │
│   ├── ui/
│   │   ├── app_window.py
│   │   ├── sidebar.py
│   │   ├── topbar.py
│   │   ├── dashboard_view.py
│   │   ├── file_preview_view.py
│   │   ├── analysis_view.py
│   │   ├── cleaning_view.py
│   │   ├── export_view.py
│   │   ├── components.py
│   │   └── styles.py
│   │
│   └── utils/
│       ├── file_utils.py
│       ├── text_utils.py
│       ├── date_utils.py
│       ├── dataframe_utils.py
│       └── constants.py
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── themes/
│
├── data/
│   ├── input/
│   ├── output/
│   ├── samples/
│   └── reports/
│
├── docs/
│   ├── project-overview.md
│   ├── architecture.md
│   ├── usage-guide.md
│   └── roadmap.md
│
├── logs/
│   └── app.log
│
├── scripts/
│   ├── run_dev.bat
│   ├── clean_outputs.bat
│   └── build_exe.bat
│
├── tests/
│   ├── test_file_loader.py
│   ├── test_data_analyzer.py
│   ├── test_data_cleaner.py
│   └── test_data_exporter.py
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run.py
```

---

## 📁 Folder Explanation

### `app/`

Main application source code.

### `app/core/`

Contains the business logic.

| File | Purpose |
|---|---|
| `file_loader.py` | Loads Excel, CSV and TXT files |
| `data_analyzer.py` | Detects basic data quality issues |
| `data_cleaner.py` | Cleans the loaded DataFrame |
| `data_exporter.py` | Exports clean data to XLSX or CSV |
| `validation_engine.py` | Runs advanced validation checks |
| `report_builder.py` | Generates process reports |

### `app/models/`

Contains internal data structures.

| File | Purpose |
|---|---|
| `file_model.py` | Represents the selected file |
| `analysis_result.py` | Represents the data analysis result |
| `cleaning_result.py` | Represents the cleaning process result |
| `export_result.py` | Represents the export result |

### `app/services/`

Connects the UI layer with the core logic.

| File | Purpose |
|---|---|
| `file_service.py` | Manages the active file and DataFrames |
| `analysis_service.py` | Runs analysis and validations |
| `cleaning_service.py` | Runs automatic cleaning |
| `export_service.py` | Exports files and generates reports |
| `log_service.py` | Handles application logging |

### `app/ui/`

Desktop interface built with **CustomTkinter**.

| File | Purpose |
|---|---|
| `app_window.py` | Main desktop window |
| `sidebar.py` | Left navigation menu |
| `topbar.py` | Header bar |
| `dashboard_view.py` | Main dashboard |
| `file_preview_view.py` | File loading and preview screen |
| `analysis_view.py` | Data quality analysis screen |
| `cleaning_view.py` | Automatic cleaning screen |
| `export_view.py` | Export screen |
| `components.py` | Reusable UI components |
| `styles.py` | Colors, fonts and visual settings |

### `app/utils/`

Reusable helper functions.

| File | Purpose |
|---|---|
| `file_utils.py` | File path and extension utilities |
| `text_utils.py` | Text and column name normalization |
| `date_utils.py` | Date detection and normalization |
| `dataframe_utils.py` | DataFrame preview and metrics helpers |
| `constants.py` | Shared constants |

---

## 🧰 Tech Stack

| Area | Technology |
|---|---|
| Language | Python |
| UI | CustomTkinter |
| Data processing | Pandas |
| Excel reading/writing | OpenPyXL |
| Legacy Excel support | xlrd |
| Date parsing | python-dateutil |
| Testing | Pytest |
| Packaging | PyInstaller |
| Version control | Git / GitHub |

---

## ✅ Requirements

Before installing the project, make sure you have:

- Python 3.11 or higher
- Git
- pip
- Windows, Linux or macOS

Recommended:

- VS Code
- GitHub Desktop or terminal Git
- A virtual environment

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/datacleaner-pro.git
```

### 2. Enter the project folder

```bash
cd datacleaner-pro
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python run.py
```

On Windows, you can also use:

```bash
scripts\run_dev.bat
```

---

## 🧪 Run Tests

```bash
pytest
```

The test suite validates:

- CSV loading
- TXT loading
- XLSX loading
- Data analysis
- Duplicate detection
- Cleaning behavior
- Export to CSV
- Export to XLSX

---

## 📦 Build Windows EXE

To generate a Windows executable:

```bash
scripts\build_exe.bat
```

The executable will be generated in:

```text
dist/
```

---

## 📥 Supported Input Formats

```text
.xlsx
.xls
.csv
.txt
```

---

## 📤 Supported Output Formats

```text
.xlsx
.csv
```

---

## 🖥️ Application Screens

### Dashboard

General overview of the workflow and current file state.

### File Preview

Allows the user to select and preview a file.

### Analysis

Displays data quality metrics, warnings, recommendations and risk level.

### Cleaning

Allows the user to apply automatic cleaning rules.

### Export

Allows the user to export the cleaned file to XLSX or CSV.

---

## 📊 Quality Score

DataCleaner Pro calculates a quality score based on:

- Empty cells
- Empty rows
- Empty columns
- Duplicated rows
- Advanced validation risks
- Invalid emails
- Inconsistent dates
- High-empty columns

Risk levels:

```text
85 - 100  -> Low risk
65 - 84   -> Medium risk
0 - 64    -> High risk
```

---

## 🧽 Cleaning Rules

The automatic cleaner can:

```text
Remove empty rows
Remove empty columns
Remove duplicates
Trim text values
Normalize column names
Normalize missing values
Normalize date columns
```

Example:

```text
" Customer Name " -> customer_name
"  John Smith  "  -> John Smith
"15/05/2026"     -> 2026-05-15
```

---

## 🧾 Generated Reports

After exporting a clean file, the app creates a report in:

```text
data/reports/
```

Report example:

```text
DATA CLEANER PRO - PROCESS REPORT

File:
- Name
- Path
- Extension
- Rows
- Columns

Analysis:
- Empty cells
- Empty rows
- Duplicates
- Quality score
- Risk level

Cleaning:
- Removed rows
- Removed columns
- Removed duplicates
- Normalized columns
- Normalized dates

Export:
- Output path
- Format
- Rows
- Columns
- Final file size
```

---

## 🪵 Logs

Logs are stored in:

```text
logs/app.log
```

Example log events:

```text
Application started
Export started
Export completed
Report generated
Critical error detected
```

---

## 🧭 Workflow

```text
1. Open DataCleaner Pro
2. Load an Excel, CSV or TXT file
3. Preview the loaded data
4. Go to Analysis
5. Review quality score and warnings
6. Go to Cleaning
7. Run automatic cleaning
8. Go to Export
9. Export clean file
10. Review generated report
```

---

## 📌 Example Use Cases

### CRM / ERP Imports

Prepare customer files before importing them into a CRM or ERP.

### Administrative Data Cleaning

Clean spreadsheets received from internal teams, vendors or clients.

### Database Migration

Prepare CSV or Excel files before inserting them into PostgreSQL, MySQL or another database.

### Reporting

Clean messy operational files before building dashboards or business reports.

### Portfolio Project

Showcase a real Python desktop application with business value.

---

## 🧱 Development Stages

### Stage 1

Project base, configuration and initial execution.

### Stage 2

Desktop UI with CustomTkinter.

### Stage 3

Dashboard and global file state.

### Stage 4

Real file loading and preview.

### Stage 5

Data quality analysis.

### Stage 6

Automatic cleaning engine.

### Stage 7

Advanced validation engine.

### Stage 8

Export to XLSX and CSV.

### Stage 9

Reports and logs.

### Stage 10

Tests, scripts, documentation and GitHub-ready release.

---

## 🛣️ Roadmap

### Version 0.2.0

- Dark mode
- Better table component
- Multi-sheet Excel support
- Manual column renaming
- Column selector before export
- Improved CSV detection

### Version 0.3.0

- Export to JSON
- Export to SQL
- PostgreSQL connection
- MySQL connection
- Saved cleaning profiles

### Version 0.4.0

- PDF reports
- Before/after comparison
- Data quality dashboard
- Custom validation rules
- Duplicate detection by selected columns

### Version 1.0.0

- Stable Windows executable
- Polished UI
- Full documentation
- Real sample datasets
- Production-ready portfolio release

---

## 🧑‍💻 Author

Developed by **Matias Isaac Frutos Gonzalez**.

```text
Full Stack Developer
Python · JavaScript · Node.js · PostgreSQL · Automation · Desktop Tools
```

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

### 🧹 DataCleaner Pro

**Turn messy files into clean, useful and export-ready data.**

<br>

![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=900&color=16A34A&center=true&vCenter=true&width=900&lines=Load+Data;Analyze+Quality;Clean+Automatically;Export+Clean+Files;Generate+Reports)

</div>#   D a t a C l e a n e r - P r o 
 
 
