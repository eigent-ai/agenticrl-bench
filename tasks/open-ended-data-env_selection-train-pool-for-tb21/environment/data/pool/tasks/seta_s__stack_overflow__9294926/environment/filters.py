DATE_LABELS = {"DATE"}
TIME_LABELS = {"TIME"}
LOC_LABELS  = {"LOCATION", "PLACE"}

def extract_dates(entities):
    return [text for text, label in entities if label in DATE_LABELS]

def extract_times(entities):
    return [text for text, label in entities if label in TIME_LABELS]

def extract_locations(entities):
    return [text for text, label in entities if label in LOC_LABELS]
