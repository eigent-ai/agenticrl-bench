"""Pipeline configuration for text classification."""

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from custom_transformers import TextNormalizer, FeatureSelector


def build_pipeline():
    """Build and return the text classification pipeline."""
    pipeline = Pipeline([
        ('norm', TextNormalizer()),
        ('vect', CountVectorizer()),
        ('clf', MultinomialNB()),
        ('tfidf', TfidfTransformer()),
        ('select', FeatureSelector(k=1000)),
    ])
    return pipeline
