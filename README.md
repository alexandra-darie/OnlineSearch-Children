# Query Evaluation Pipeline

This project analyzes web search results for adult and child-oriented queries.
It uses readability metrics, profanity detection, and URL safety checks to
evaluate the quality and appropriateness of search results.

## Pipeline Overview


The process begins by loading queries from a CSV file. Each row in the file contains a query
and an associated label, where a label of `1` indicates that the query is written by children,
and a label of `0` indicates an adult-written query. Based on these labels, the queries are
divided into two separate groups for further processing.
Each query is sent to the Brave Search API to retrieve web results. For child queries,
a second version of the query is also created by appending "for kids" to help encourage
more age-appropriate results.

The returned snippets are cleaned to remove HTML tags and escaped characters. Once cleaned,
each snippet is analyzed using four readability metrics (Flesch-Kincaid, Dale-Chall,
Coleman-Liau, and Spache). The snippet is also checked for profanity, and its URL is
submitted to the Google Safe Browsing API to assess safety.

All processed results are saved to `detailed_results.csv`. Then, the script computes
average scores and rates by query type (e.g., Children (Original), Children (For Kids), Adults),
which are saved to `aggregated_results.csv`.

This pipeline helps measure how suitable search results are for different age groups
based on language complexity, safety, and content appropriateness.

---

## Statistical Analysis

The script begins by loading the `detailed_results.csv` file, and then it filters
only the results labeled as "Children (Original)" and "Children (For Kids)".
To ensure a fair comparison, both sets are truncated to the same length.

Five metrics are selected for comparison:
- Flesch-Kincaid Grade Level
- Dale-Chall Readability Score
- Coleman-Liau Index
- Spache Score
- Profanity (binary)

For each metric, the script performs a paired statistical test to determine whether
there is a significant difference between the two query formulations.

Before selecting the test, a Shapiro-Wilk test is applied to the difference scores
to assess whether they are normally distributed. If the differences are approximately
normal (p > 0.05), a paired t-test is used. Otherwise, the Wilcoxon signed-rank test
is applied as a non-parametric alternative.

The results of all significance tests, including the test statistic, p-value,
normality result, and the test type used, are saved in a CSV file named
`significance_tests_summary.csv`. The results are also visualized as a table and
saved as a PNG image (`significance_tests_summary.png`) for easier reference.

This statistical evaluation helps determine whether explicitly tailoring queries
(e.g., adding "for kids") leads to significantly different results in terms of
readability or profanity.

---

## Requirements

Install dependencies using pip:

    pip install -r requirements.txt

Required packages include:
- pandas
- requests
- textstat
- better_profanity

---

## Setup

Update your API keys and CSV file path in:

    src/config.py

The API keys required are : BRAVE_API_KEY, CSV_PATH, SAFE_BROWSING_API_KEY.
BRAVE_API_KEY is the API key generated in order to use the Brave Search API v4.
CSV_PATH is the path to the children's query CSV.
SAFE_BROWSING_API_KEY is the Google Safe Browsing API key required to use the Google Safe Browsing API.

Example query CSV format (queries.csv):

    why do cats purr 1
    how do airplanes fly 0

Where:
- label = 1 indicates a child-focused query
- label = 0 indicates an adult query

---

## Running the Script

To run the pipeline, use:

    python main.py

This will produce two output files in the working directory:
- detailed_results.csv
- aggregated_results.csv

---

## Output Overview

**detailed_results.csv** contains:
- Query and query type
- URL and snippet
- Readability scores (Flesch-Kincaid, Dale-Chall, etc.)
- Flags for profanity and unsafe URLs

**aggregated_results.csv** contains:
- Average readability scores
- Profanity rate
- Unsafe URL rate
Grouped by query type.

---

## Purpose

This tool supports the evaluation of search engine results with respect to
child profanity, readability, and URL safety. 

