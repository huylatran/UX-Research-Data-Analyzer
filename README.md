# UX Research Data Analyzer

A Python command-line tool that reads CSV files from usability studies and user research sessions, performs statistical analysis, generates charts, and exports a formatted report.

Built to solve a real problem in UX research workflows — turning raw study data into readable, shareable insights without needing Excel or SPSS.

## Live Example Output

```
════════════════════════════════════════════════════════════
  UX RESEARCH DATA ANALYZER
  by Huy La Tran
════════════════════════════════════════════════════════════

✅  Loaded 'sample_usability_study.csv' — 15 rows, 12 columns

  NUMERIC COLUMN STATISTICS
────────────────────────────────────────────────────────────

  📊  sus_score
      Mean      : 78.33
      Median    : 79.00
      Std Dev   : 11.08
      Min       : 55.00   Max : 93.00
      SUS Grade : Good (B)

  TASK COMPLETION ANALYSIS
────────────────────────────────────────────────────────────
  ✅  task_1_completion   Success Rate : 93.3%  (14/15 participants)
  ✅  task_2_completion   Success Rate : 80.0%  (12/15 participants)
```

## Features

- Loads any CSV file — survey results, SUS scores, task completion data, anything
- Calculates mean, median, standard deviation, min, max, and range for all numeric columns
- Auto-detects and grades SUS (System Usability Scale) scores
- Calculates task completion rates from yes/no or binary columns
- Generates bar charts with mean/median overlays for every numeric column
- Detects and reports missing data
- Exports a full text report to `/reports`
- Saves charts as PNG files to `/charts`

## Built With

- **Python 3**
- **pandas** — data loading and statistical analysis
- **matplotlib** — chart generation

## Installation

```bash
git clone https://github.com/huylatran/ux-data-analyzer.git
cd ux-data-analyzer
pip install -r requirements.txt
```

## Usage

```bash
# Analyze your own CSV file
python3 analyzer.py your_study_data.csv

# Run with the included sample data
python3 analyzer.py sample_usability_study.csv
```

## CSV Format

The tool works with any CSV. For best results, column names with these keywords get special treatment:

| Keyword in column name | Special handling |
|------------------------|-----------------|
| `sus` or `score`       | Auto-graded (A/B/C/D/F scale) |
| `task`, `completion`, `success` | Calculates pass/fail success rate |

See `sample_usability_study.csv` for a full example with participant IDs, demographics, SUS scores, task times, and satisfaction ratings.

## File Structure

```
ux-data-analyzer/
├── analyzer.py                    # Main script
├── sample_usability_study.csv     # Example dataset
├── requirements.txt               # Dependencies
├── reports/                       # Auto-generated text reports
├── charts/                        # Auto-generated PNG charts
└── README.md
```

## Why This Exists

After running usability studies for my UX projects (ClearChart, Grounded, ClearPath), I found myself manually calculating SUS scores and task completion rates in spreadsheets. This tool automates that process — load the CSV, get the report.

## Author

**Huy La Tran**
UX Designer · Human Systems Engineering, Arizona State University
[Portfolio](https://huytran-ux.netlify.app) · [LinkedIn](https://www.linkedin.com/in/huy-tran-5525801b0/)
