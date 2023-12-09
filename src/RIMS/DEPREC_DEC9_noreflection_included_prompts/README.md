those prompts raises llm_query:
    It completes the incomplete format in the prompt's last part. 
    even if I remove the last part of the 

e.g.

parse_dd = {
    '`Mistakes`:': '<mistakes made in the first attempt>',
    '`Hint for a better Method choice`:': '<    >',
    '`Corrected Attempt`:': '<     >',
    '`Answer`:': '<    >',
    '`Evaluation`': '< >',
}