import pandas as pd
from src.data.query_loader import load_queries
from src.api.brave_api import search_brave
from src.metrics.readability import get_readability_scores
from src.metrics.profanity import contains_profanity
from src.metrics.trustworthiness import is_url_unsafe
from src.config import BRAVE_API_KEY, CSV_PATH, SAFE_BROWSING_API_KEY
import re
from html import unescape

# Clean up the snippets
def clean_snippet(snippet):
    no_tags = re.sub(r"<[^>]+>", "", snippet)
    clean_text = unescape(no_tags).replace("\\'", "'").strip()
    return clean_text

# Apply preprocessing to queries and extract results from metrics
def process_query(query, type_label):
    results = search_brave(query, BRAVE_API_KEY)
    if not results or "web" not in results or "results" not in results["web"]:
        return []

    entries = []
    for item in results["web"]["results"]:
        url = item["url"]
        snippet = clean_snippet(item.get("description", ""))
        
        unsafe = is_url_unsafe(url, SAFE_BROWSING_API_KEY)
        profanity = contains_profanity(snippet)
        readability = get_readability_scores(snippet)

        entries.append({
            "Query": query,
            "Query_Type": type_label,
            "URL": url,
            "Snippet": snippet,
            "Flesch_Kincaid": readability["flesch_kincaid"],
            "Dale_Chall": readability["dale_chall"],
            "Coleman_Liau": readability["coleman_liau"],
            "Spache": readability["spache"],
            "Profanity": profanity,
            "Unsafe_URL": unsafe
        })

    return entries

def main():
    # Load the query sets in separate sets
    children_queries = load_queries(CSV_PATH, label_filter=1)
    adult_queries = load_queries(CSV_PATH, label_filter=0)

    final_results = []
    detailed_results = []

    # Add the processed children queries to the detailed results csv file
    for idx, query in enumerate(children_queries):
        if idx % 10 == 0:
            print(f"[INFO] Processed {idx}/{len(children_queries)} children queries...")

        original_entries = process_query(query, "Children (Original)")
        detailed_results.extend(original_entries)

        kids_entries = process_query(f"{query} for kids", "Children (For Kids)")
        detailed_results.extend(kids_entries)

    # Add the processed adult queries to the detailed results csv file
    for idx, query in enumerate(adult_queries):
        if idx % 10 == 0:
            print(f"[INFO] Processed {idx}/{len(adult_queries)} adult queries...")

        adult_entries = process_query(query, "Adults (Original)")
        detailed_results.extend(adult_entries)

    detailed_df = pd.DataFrame(detailed_results)
    detailed_df.to_csv("detailed_results.csv", index=False)

    # Calculate the average readability, profanity and url safety for each query type
    for type_label in detailed_df["Query_Type"].unique():
        subset = detailed_df[detailed_df["Query_Type"] == type_label]
        count = len(subset)
        avg_fk = subset["Flesch_Kincaid"].mean()
        avg_dc = subset["Dale_Chall"].mean()
        avg_cl = subset["Coleman_Liau"].mean()
        avg_sp = subset["Spache"].mean()
        profanity_rate = subset["Profanity"].mean()
        unsafe_rate = subset["Unsafe_URL"].mean()

        final_results.append({
            "Label": type_label,
            "Count": count,
            "Avg_Flesch_Kincaid": avg_fk,
            "Avg_Dale_Chall": avg_dc,
            "Avg_Coleman_Liau": avg_cl,
            "Avg_Spache": avg_sp,
            "Profanity_Rate": profanity_rate,
            "Unsafe_URL_Rate": unsafe_rate
        })

    final_df = pd.DataFrame(final_results)
    final_df.to_csv("aggregated_results.csv", index=False)
    print("\n All done! Saved 'aggregated_results.csv' and 'detailed_results.csv'.")

if __name__ == "__main__":
    main()