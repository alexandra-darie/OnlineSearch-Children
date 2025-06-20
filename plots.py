import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("detailed_results.csv")

# Set Seaborn style
sns.set(style="whitegrid")

# Boxplots for each readability metric
metrics = ["Flesch_Kincaid", "Dale_Chall", "Coleman_Liau", "Spache"]
for metric in metrics:
    plt.figure(figsize=(8, 5))
    sns.boxplot(
        x="Query_Type", y=metric, data=df,
        palette="pastel", linewidth=2.5, fliersize=3
    )
    plt.ylabel("Score", fontsize=12)
    plt.xlabel("")
    plt.tight_layout()
    plt.savefig(f"{metric}_simple_boxplot.png", dpi=300)
    plt.close()

# Bar plot for Profanity rate
profanity_rates = df.groupby("Query_Type")["Profanity"].mean() * 100
plt.figure(figsize=(8, 5))
sns.barplot(
    x=profanity_rates.index, y=profanity_rates.values,
    color='tomato'
)
plt.ylabel("Profanity Rate (%)", fontsize=12)
plt.xlabel("")
plt.ylim(0, 5) 
plt.tight_layout()
plt.savefig("profanity_rate_barplot.png", dpi=300)
plt.close()

# Bar plot for Unsafe URL rates
unsafe_rates = df.groupby("Query_Type")["Unsafe_URL"].mean() * 100
plt.figure(figsize=(8, 5))
sns.barplot(
    x=unsafe_rates.index, y=unsafe_rates.values,
    color='grey'
)
plt.ylabel("Unsafe URL Rate (%)", fontsize=12)
plt.xlabel("")
plt.ylim(0, 1)  
plt.tight_layout()
plt.savefig("unsafe_url_barplot.png", dpi=300)
plt.close()

print("\n Final simple plots saved!")
