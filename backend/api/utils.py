import re
from fuzzywuzzy import process
# Simple area extractor and fuzzy matcher
def extract_areas(text):
    text = text.lower().strip()
    text = re.sub(r'(?i)\b(analyze|show|compare|give|display|show me|price growth for|demand trends for|over the last \d+ years|in the last \d+ years)\b', '', text)
    parts = re.split(r'\band\b|,|vs|vs\.| versus | & ', text, flags=re.I)
    areas = []
    for p in parts:
        p = re.sub(r'(?i)\b(demand|demand trends|price growth|price|trends|over the last \d+ years|last \d+ years|years|for)\b', '', p).strip()
        p = re.sub(r'^[^\w]+|[^\w]+$', '', p)
        if p:
            areas.append(p.strip())
    return areas

def fuzzy_match(area, choices, limit=3, score_cutoff=60):
    if not choices:
        return None
    match, score = process.extractOne(area, choices)
    if score >= score_cutoff:
        return match
    return None
