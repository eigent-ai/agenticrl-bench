"""Module C — String processing utilities."""


def camel_to_snake(name):
    result = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            result.append("_")
        result.append(ch.lower())
    return "".join(result)


def truncate(text, max_len=80):
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."
