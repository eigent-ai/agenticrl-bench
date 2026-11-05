import spacy

nlp = spacy.load("en_core_web_md")

def get_entities(text):
    """Run NER on text and return list of (text, label) tuples."""
    doc = nlp(text)
    return [(ent.string, ent.label_) for ent in doc.ents]
