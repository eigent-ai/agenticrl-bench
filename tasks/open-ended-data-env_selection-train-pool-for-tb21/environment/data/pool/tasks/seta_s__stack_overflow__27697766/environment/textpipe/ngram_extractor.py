"""Ngram extraction module for the text analysis pipeline."""

from sklearn.feature_extraction.text import CountVectorizer


def extract_ngrams(documents, ngram_range=(1, 2)):
    """Extract unigram and bigram features from documents.

    Args:
        documents: List of document strings
        ngram_range: Tuple specifying min and max ngram sizes

    Returns:
        Tuple of (feature_matrix, vocabulary_dict)
    """
    unigram_vec = CountVectorizer(ngram_range=(1, 1))
    unigram_vec.fit(documents)
    predefined_vocab = list(unigram_vec.vocabulary_.keys())

    ngram_vec = CountVectorizer(
        ngram_range=ngram_range,
        vocabulary=predefined_vocab,
        stop_words='english',
        lowercase=True
    )

    feature_matrix = ngram_vec.fit_transform(documents)
    vocabulary = ngram_vec.vocabulary_

    return feature_matrix, vocabulary
