from textstat import (
    flesch_kincaid_grade,
    dale_chall_readability_score,
    coleman_liau_index,
    spache_readability
)

# Calculate readability for each of the four metrics 
def get_readability_scores(text):
    fk = flesch_kincaid_grade(text)
    dc = dale_chall_readability_score(text)
    cl = coleman_liau_index(text)
    sp = spache_readability(text)

    return {
        "flesch_kincaid": fk,
        "dale_chall": dc,
        "coleman_liau": cl,
        "spache": sp
    }
