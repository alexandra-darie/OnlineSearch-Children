import pandas as pd

# Loads queries from the csv file
def load_queries(csv_path, query_col="Query", label_col="Label", label_filter=1):
    df = pd.read_csv(csv_path, sep="\t", header=None, names=["Query", "Label"])
    df["Label"] = df["Label"].astype(int)
    filtered_queries = df[df[label_col] == label_filter][query_col].dropna().unique().tolist()
    return filtered_queries