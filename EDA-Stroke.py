# ------------------------------------------------------------
# Stroke Prediction Dataset - Simple EDA (clean visuals + report)
# ------------------------------------------------------------
# Works with Kaggle file: healthcare-dataset-stroke-data.csv
#
# Outputs:
#   figs/...
#   outputs/report.md
# ------------------------------------------------------------

import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (9, 5)
os.makedirs("figs", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

file_path = None  #ลองเปลี่ยน path ได้นะ ถ้าautoไม่ติด

def autodetect_csv():
    if file_path and os.path.exists(file_path):
        return file_path
    for f in os.listdir():
        if f.lower().endswith(".csv") and "stroke" in f.lower():
            return f
    for f in os.listdir():
        if f.lower().endswith(".csv"):
            return f
    return None

csv_path = autodetect_csv()
if not csv_path or not os.path.exists(csv_path):
    print("❌ Could not find a CSV. Set file_path to your dataset path.")
    sys.exit(1)

print(f"✅ Using CSV: {os.path.abspath(csv_path)}")


df = pd.read_csv(csv_path)
print("\n===== BASIC INFO =====")
print(df.head(3))
print(df.info())

df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]


for col in ["age", "avg_glucose_level", "bmi"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

if "bmi" in df.columns and df["bmi"].isna().any():
    df["bmi"] = df["bmi"].fillna(df["bmi"].median())

for id_candidate in ["id", "patient_id"]:
    if id_candidate in df.columns:
        df = df.drop(columns=[id_candidate])

if "stroke" in df.columns:
    df["stroke"] = pd.to_numeric(df["stroke"], errors="coerce").fillna(0).astype(int)

if "age" in df.columns:
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 30, 45, 60, 200],
        labels=["<30", "30–45", "45–60", "60+"],
        right=True,
        include_lowest=True,
    )

def savefig(name):
    path = os.path.join("figs", name)
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"[PLOT] Saved: {path}")

if "gender" in df.columns:
    plt.figure()
    sns.countplot(x="gender", data=df, order=df["gender"].value_counts().index)
    plt.title("Number of Patients by Gender")
    plt.xlabel("Gender"); plt.ylabel("Count")
    savefig("01_gender_counts.png")

if "age" in df.columns:
    plt.figure()
    sns.histplot(df["age"].dropna(), bins=25, kde=True)
    plt.title("Age Distribution")
    plt.xlabel("Age"); plt.ylabel("Count")
    savefig("02_age_distribution.png")

if "stroke" in df.columns and "gender" in df.columns:
    rate_by_gender = (
        df.groupby("gender")["stroke"].mean().sort_values(ascending=False).rename("stroke_rate")
    )
    plt.figure()
    sns.barplot(x=rate_by_gender.index, y=rate_by_gender.values)
    plt.title("Stroke Rate by Gender")
    plt.xlabel("Gender"); plt.ylabel("Stroke Rate")
    savefig("03_stroke_rate_by_gender.png")

if "stroke" in df.columns and "age_group" in df.columns:
    rate_by_age = (
        df.groupby("age_group")["stroke"].mean().rename("stroke_rate")
    )
    plt.figure()
    sns.barplot(x=rate_by_age.index, y=rate_by_age.values)
    plt.title("Stroke Rate by Age Group")
    plt.xlabel("Age Group"); plt.ylabel("Stroke Rate")
    savefig("04_stroke_rate_by_age_group.png")

if "avg_glucose_level" in df.columns and "stroke" in df.columns:
    plt.figure()
    sns.kdeplot(data=df, x="avg_glucose_level", hue="stroke", common_norm=False)
    plt.title("Glucose Level by Stroke Outcome")
    plt.xlabel("Avg Glucose Level"); plt.ylabel("Density")
    savefig("05_glucose_by_stroke.png")

if "bmi" in df.columns and "stroke" in df.columns:
    plt.figure()
    sns.kdeplot(data=df, x="bmi", hue="stroke", common_norm=False)
    plt.title("BMI by Stroke Outcome")
    plt.xlabel("BMI"); plt.ylabel("Density")
    savefig("06_bmi_by_stroke.png")

if "smoking_status" in df.columns and "stroke" in df.columns:
    plt.figure()
    order = df["smoking_status"].value_counts().index
    sns.barplot(x="smoking_status", y="stroke", data=df, order=order, estimator=np.mean)
    plt.title("Stroke Rate by Smoking Status")
    plt.xlabel("Smoking Status"); plt.ylabel("Stroke Rate")
    plt.xticks(rotation=20)
    savefig("07_stroke_by_smoking_status.png")

num = df.select_dtypes(include=[np.number])
if not num.empty:
    corr = num.corr(numeric_only=True)
    corr_pairs = corr.unstack().sort_values(key=np.abs, ascending=False)
    corr_pairs = corr_pairs[corr_pairs != 1]
    top_corr = corr_pairs.drop_duplicates().head(5)

    print("\n🔥 Top 5 strongest numeric relationships:")
    for (a, b), v in top_corr.items():
        print(f" - {a} ↔ {b}: r = {v:.2f}")


    strong = corr[(corr > 0.5) | (corr < -0.5)]
    if strong.notna().any().any():
        plt.figure(figsize=(6,5))
        sns.heatmap(strong, annot=True, cmap="coolwarm", fmt=".2f", square=True, linewidths=1)
        plt.title("Simplified Correlation (|r| > 0.5)")
        savefig("08_correlation_simplified.png")

lines = []
add = lines.append

add("# Stroke Prediction – EDA Summary\n")
add(f"- **File:** `{os.path.basename(csv_path)}`")
add(f"- **Rows x Cols:** {df.shape[0]} x {df.shape[1]}")

overall_rate = None
if "stroke" in df.columns:
    overall_rate = df["stroke"].mean()
    add(f"- **Overall stroke rate:** {overall_rate:.2%}")

if "gender" in df.columns and "stroke" in df.columns:
    g = df.groupby("gender")["stroke"].mean().sort_values(ascending=False)
    add("\n## Stroke rate by Gender")
    for k, v in g.items():
        add(f"- {k}: {v:.2%}")

if "age_group" in df.columns and "stroke" in df.columns:
    a = df.groupby("age_group")["stroke"].mean()
    add("\n## Stroke rate by Age Group")
    for k, v in a.items():
        add(f"- {k}: {v:.2%}")

if "avg_glucose_level" in df.columns:
    add(f"\n- **Avg glucose (mean±std):** {df['avg_glucose_level'].mean():.1f} ± {df['avg_glucose_level'].std():.1f}")
if "bmi" in df.columns:
    add(f"- **BMI (mean±std):** {df['bmi'].mean():.1f} ± {df['bmi'].std():.1f}")

if not num.empty:
    add("\n## Top numeric correlations (by |r|)")
    for (a, b), v in top_corr.items():
        add(f"- {a} ↔ {b}: {v:.2f}")

add("\n---\n## Notes you can use in your report")
if overall_rate is not None:
    add(f"- The overall stroke rate is **{overall_rate:.1%}**. We examine how risk varies by gender and age.")
if "gender" in df.columns:
    add("- Gender distribution and stroke rates show which group appears more at risk in this dataset.")
if "age_group" in df.columns:
    add("- Stroke risk generally increases with age; the age-group chart makes this visible.")
if "avg_glucose_level" in df.columns:
    add("- Higher average glucose appears associated with stroke in the density plot.")
if "bmi" in df.columns:
    add("- BMI distribution suggests whether obesity relates to stroke in this sample.")

with open("outputs/report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n✅ Done!")
print(" - Plots saved in figs/")
print(" - Summary saved to outputs/report.md")