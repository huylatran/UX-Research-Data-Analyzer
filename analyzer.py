"""
UX Research Data Analyzer
--------------------------
Reads a CSV file of UX research data (survey results, SUS scores,
task completion times, etc.), performs statistical analysis, and
outputs a clean formatted report with optional chart generation.

Author: Huy La Tran
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving charts
import sys
import os
from datetime import datetime


# ── CONFIGURATION ─────────────────────────────────────────────────
REPORT_DIR = "reports"
CHART_DIR  = "charts"


# ── HELPERS ───────────────────────────────────────────────────────
def divider(char="─", width=60):
    return char * width


def section(title):
    print(f"\n{divider()}")
    print(f"  {title.upper()}")
    print(divider())


def load_data(filepath):
    """Load CSV and return a DataFrame, or exit on failure."""
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)

    try:
        df = pd.read_csv(filepath)
        print(f"\n✅  Loaded '{filepath}' — {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")
        sys.exit(1)


# ── ANALYSIS ──────────────────────────────────────────────────────
def overview(df):
    section("Dataset Overview")
    print(f"  Rows            : {len(df)}")
    print(f"  Columns         : {len(df.columns)}")
    print(f"  Column names    : {', '.join(df.columns.tolist())}")

    missing = df.isnull().sum()
    total_missing = missing.sum()
    if total_missing > 0:
        print(f"\n  ⚠️  Missing values detected ({total_missing} total):")
        for col, count in missing[missing > 0].items():
            pct = (count / len(df)) * 100
            print(f"     {col:<30} {count} missing ({pct:.1f}%)")
    else:
        print(f"\n  ✅  No missing values found.")


def numeric_stats(df):
    section("Numeric Column Statistics")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        print("  No numeric columns found.")
        return

    for col in numeric_cols:
        data = df[col].dropna()
        print(f"\n  📊  {col}")
        print(f"      Count     : {len(data)}")
        print(f"      Mean      : {data.mean():.2f}")
        print(f"      Median    : {data.median():.2f}")
        print(f"      Std Dev   : {data.std():.2f}")
        print(f"      Min       : {data.min():.2f}")
        print(f"      Max       : {data.max():.2f}")
        print(f"      Range     : {(data.max() - data.min()):.2f}")

        # SUS score interpretation (if column looks like SUS data)
        if "sus" in col.lower() or "score" in col.lower():
            mean = data.mean()
            if mean >= 85:
                grade = "Excellent (A)"
            elif mean >= 72:
                grade = "Good (B)"
            elif mean >= 52:
                grade = "OK (C/D)"
            else:
                grade = "Poor (F) — needs improvement"
            print(f"      SUS Grade : {grade}")


def categorical_summary(df):
    section("Categorical Column Summary")
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if not cat_cols:
        print("  No categorical columns found.")
        return

    for col in cat_cols:
        print(f"\n  🏷️   {col}")
        counts = df[col].value_counts()
        for val, count in counts.items():
            pct = (count / len(df)) * 100
            bar = "█" * int(pct / 5)
            print(f"      {str(val):<25} {count:>4}  ({pct:5.1f}%)  {bar}")


def task_completion_analysis(df):
    """Specialized analysis if task completion columns are detected."""
    task_cols = [c for c in df.columns if "task" in c.lower() or "completion" in c.lower() or "success" in c.lower()]
    if not task_cols:
        return

    section("Task Completion Analysis")
    for col in task_cols:
        data = df[col].dropna()
        if data.dtype in ["int64", "float64"]:
            rate = (data > 0).mean() * 100
            print(f"\n  ✅  {col}")
            print(f"      Success Rate : {rate:.1f}%")
            print(f"      Avg Value    : {data.mean():.2f}")
        elif set(data.unique()).issubset({"yes", "no", "Yes", "No", True, False, 1, 0}):
            success = data.isin(["yes", "Yes", True, 1]).sum()
            rate = (success / len(data)) * 100
            print(f"\n  ✅  {col}")
            print(f"      Success Rate : {rate:.1f}%  ({success}/{len(data)} participants)")


# ── CHARTS ────────────────────────────────────────────────────────
def generate_charts(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    generated = []

    for col in numeric_cols:
        data = df[col].dropna()
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f"Distribution: {col}", fontsize=14, fontweight="bold", color="#1A1A2E")

        # Histogram
        axes[0].hist(data, bins=min(10, len(data)), color="#5A5A9A", edgecolor="white", alpha=0.85)
        axes[0].set_title("Distribution", fontsize=12)
        axes[0].set_xlabel(col)
        axes[0].set_ylabel("Frequency")
        axes[0].axvline(data.mean(), color="#D4788A", linestyle="--", linewidth=2, label=f"Mean: {data.mean():.1f}")
        axes[0].axvline(data.median(), color="#7BAF94", linestyle="--", linewidth=2, label=f"Median: {data.median():.1f}")
        axes[0].legend()
        axes[0].set_facecolor("#F8F8FC")

        # Box plot
        bp = axes[1].boxplot(data, patch_artist=True, vert=True,
                              boxprops=dict(facecolor="#EEEEF8", color="#5A5A9A"),
                              medianprops=dict(color="#D4788A", linewidth=2),
                              whiskerprops=dict(color="#5A5A9A"),
                              capprops=dict(color="#5A5A9A"),
                              flierprops=dict(marker="o", color="#D4A24A", alpha=0.7))
        axes[1].set_title("Box Plot", fontsize=12)
        axes[1].set_ylabel(col)
        axes[1].set_facecolor("#F8F8FC")

        plt.tight_layout()
        filename = f"{col.lower().replace(' ', '_')}_chart.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        generated.append(filepath)

    return generated


# ── REPORT EXPORT ─────────────────────────────────────────────────
def export_report(df, filepath, charts):
    os.makedirs(REPORT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = os.path.basename(filepath).replace(".csv", "")
    report_path = os.path.join(REPORT_DIR, f"{filename}_report.txt")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    with open(report_path, "w") as f:
        f.write("UX RESEARCH DATA ANALYSIS REPORT\n")
        f.write(f"Generated : {timestamp}\n")
        f.write(f"Source    : {filepath}\n")
        f.write(divider("=") + "\n\n")

        f.write("DATASET OVERVIEW\n")
        f.write(divider() + "\n")
        f.write(f"Rows    : {len(df)}\n")
        f.write(f"Columns : {len(df.columns)}\n\n")

        if numeric_cols:
            f.write("NUMERIC STATISTICS\n")
            f.write(divider() + "\n")
            for col in numeric_cols:
                data = df[col].dropna()
                f.write(f"\n{col}\n")
                f.write(f"  Mean      : {data.mean():.2f}\n")
                f.write(f"  Median    : {data.median():.2f}\n")
                f.write(f"  Std Dev   : {data.std():.2f}\n")
                f.write(f"  Min/Max   : {data.min():.2f} / {data.max():.2f}\n")

        if charts:
            f.write(f"\nCHARTS GENERATED\n")
            f.write(divider() + "\n")
            for c in charts:
                f.write(f"  {c}\n")

    return report_path


# ── MAIN ──────────────────────────────────────────────────────────
def main():
    print(divider("═"))
    print("  UX RESEARCH DATA ANALYZER")
    print("  by Huy La Tran")
    print(divider("═"))

    # Accept filepath as argument or prompt
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("\n  Enter CSV file path: ").strip()

    df = load_data(filepath)

    overview(df)
    numeric_stats(df)
    categorical_summary(df)
    task_completion_analysis(df)

    # Charts
    section("Generating Charts")
    charts = generate_charts(df, CHART_DIR)
    if charts:
        for c in charts:
            print(f"  📈  Saved: {c}")
    else:
        print("  No numeric columns to chart.")

    # Export report
    section("Exporting Report")
    report_path = export_report(df, filepath, charts)
    print(f"  📄  Report saved: {report_path}")

    print(f"\n{divider('═')}")
    print("  Analysis complete.")
    print(divider("═"))


if __name__ == "__main__":
    main()
