# 🚆 CBTC Log Analyzer with Fault Classification

This project is an end-to-end log analysis tool designed for CBTC (Communications-Based Train Control) railway systems. It uses Natural Language Processing (NLP) to parse and classify system logs into fault types, helping engineers and testers quickly identify operational issues.

This is a Streamlit-based interactive tool that allows users to upload, classify, and analyze CBTC (Communication-Based Train Control) system log files. The app uses basic NLP techniques to classify faults, stores them in a SQLite database, and provides interactive charts, search, filtering, and Power BI integration for visualization.

---

 **Key Features**

 Upload raw CBTC log files (CSV)

 Rule-based NLP for fault classification (e.g., Track Circuit, Signal Conflict, Communication Fault)

 Save & load logs using SQLite database

 Search logs and apply filters by fault type or keywords

 View fault trends and export cleaned logs for external BI tools

 GitHub-ready structure with requirements.txt, .gitignore, and README

 Plans to expand with ML-based fault classification

---

##  Getting Started

###  Clone the repo

```bash
git clone https://github.com/yourusername/CBTC_Log_Analyzer.git
cd CBTC_Log_Analyzer/streamlit_app
```

###  Install dependencies

```bash
pip install -r requirements.txt
```

> Example dependencies:
```txt
streamlit
pandas
matplotlib
```

### Initialize the Database

Run this **once** to create the `logs` table:

```bash
python init_db.py
```

### Run the App

```bash
streamlit run app.py
```

---

## How it Works

- Upload a `.csv` log file with at least the column `LogMessage`.
- The app applies basic NLP keyword matching to classify fault types.
- Missing `Timestamp` or `LogLevel` fields are auto-filled.
- Data is saved in `cbtc_logs.db` and displayed in a table.
- You can filter/search logs and export results to Excel.

---

##  Fault Classification Rules

| Keyword         | Classified As              |
|-----------------|----------------------------|
| `track`         | Track Circuit Failure      |
| `signal`        | Signal Conflict            |
| `balise`        | Balise Error               |
| `comm`/`communication` | Communication Fault |
| *(others)*      | Unknown                    |

---

## Sample Input Format

```csv
Timestamp,Subsystem,Component,LogMessage
2025-07-07 14:32:00,ATS,SignalRelay,Track circuit 528 failed self-check
```

---

##  Screenshots

> ui_home.png
classified_logs.png
search_filter.png


---

## 🙋‍♀️ Developed by

**Syeda Nishat**
