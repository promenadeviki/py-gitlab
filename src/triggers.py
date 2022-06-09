import re


match_triggers = (
    (re.compile("(hey|hi|hello|)"),"hello"),
    (re.compile("projects"), "projects"), # show gitlab projects per group
    (re.compile("issues"), "issues") # show issues per group
)

search_triggers = (
    (re.compile("weather"), "weather"),
    (re.compile("comic"), "comic"),
    (re.compile("joke"), "joke"),
    (re.compile("pics"), "pics"),
    (re.compile("(search)|(look up)|(google)"), "search"),
    (re.compile("synonyms"), "synonyms"),
    (re.compile("(wordcount)|(word count)"), "wordcount"),
    (re.compile("(play|video|youtube)"), "youtube"),
)


def get_response_key(command, regex_type='match'):
    regex = re.match if regex_type == 'match' else re.search
    lookup = match_triggers if regex_type == 'match' else search_triggers
    for key, value in lookup:
        if regex(key, command):
            return value
    return None
