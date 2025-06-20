import pandas as pd
from scipy.stats import ttest_rel, wilcoxon, shapiro
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("detailed_results.csv")

# Filter to children queries (original + for kids)
children_original = df[df["Query_Type"] == "Children (Original)"].reset_index(drop=True)
children_forkids = df[df["Query_Type"] == "Children (For Kids)"].reset_index(drop=True)

# Sanity check: equal number of snippets
min_len = min(len(children_original), len(children_forkids))
children_original = children_original.iloc[:min_len]
children_forkids = children_forkids.iloc[:min_len]

# Metrics to test
metrics = ["Flesch_Kincaid", "Dale_Chall", "Coleman_Liau", "Spache", "Profanity"]

# Results storage
results = []

for metric in metrics:
    # Convert to numeric if needed
    orig = children_original[metric].astype(float)
    forkids = children_forkids[metric].astype(float)

    # Shapiro-Wilk normality test on differences
    differences = orig - forkids
    stat, p_norm = shapiro(differences)

    if p_norm > 0.05:
        # Normal: paired t-test
        test_type = "Paired t-test"
        t_stat, p_val = ttest_rel(orig, forkids)
    else:
        # Not normal: use Wilcoxon signed-rank test (paired)
        test_type = "Wilcoxon"
        t_stat, p_val = wilcoxon(orig, forkids)

    results.append({
        "Metric": metric,
        "Normality p-value": round(p_norm, 4),
        "Test": test_type,
        "Test statistic": round(t_stat, 4),
        "p-value": round(p_val, 4)
    })

# Create a summary DataFrame
df_results = pd.DataFrame(results)

# Save as CSV
df_results.to_csv("significance_tests_summary.csv", index=False)
print("\n All significance tests complete. Summary saved to 'significance_tests_summary.csv'.")

# Save as PNG image
fig, ax = plt.subplots(figsize=(10, len(df_results)*0.6)) 
ax.axis("off")
table = ax.table(
    cellText=df_results.values,
    colLabels=df_results.columns,
    loc="center",
    cellLoc="center",
    colColours=["#f0f0f0"]*len(df_results.columns)
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)
plt.tight_layout()
plt.savefig("significance_tests_summary.png", dpi=300)
plt.close()
print("Summary table saved as 'significance_tests_summary.png'.\n")

print(df_results)
