import os
import json
import sys
from sklearn.tree import DecisionTreeClassifier
from dataset import get_dataset
from extract_rules import (
    tree_to_text,
    tree_to_pandas_conditions,
    rules_for_class,
    validate_rules,
)


def main():
    df, feature_names = get_dataset()
    X = df[feature_names]
    y = df['target']

    clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    clf.fit(X, y)

    os.makedirs('output', exist_ok=True)

    # Extract text rules
    text_rules = tree_to_text(clf, feature_names)
    with open('output/text_rules.txt', 'w') as f:
        f.write(text_rules)
    print("Text rules written to output/text_rules.txt")

    # Extract pandas conditions
    pandas_conditions = tree_to_pandas_conditions(clf, feature_names)
    with open('output/pandas_conditions.json', 'w') as f:
        json.dump(pandas_conditions, f, indent=2)
    print(f"Pandas conditions written ({len(pandas_conditions)} leaves)")

    # Extract class-specific rules
    class_rules = rules_for_class(clf, feature_names, class_id=0)
    with open('output/class_rules.json', 'w') as f:
        json.dump(class_rules, f, indent=2)
    print(f"Class 0 rules written ({len(class_rules)} rules)")

    # Validate manual traversal
    n_match, n_total = validate_rules(clf, X, feature_names)
    print(f"Validation: {n_match}/{n_total} samples match clf.apply()")


if __name__ == '__main__':
    main()
