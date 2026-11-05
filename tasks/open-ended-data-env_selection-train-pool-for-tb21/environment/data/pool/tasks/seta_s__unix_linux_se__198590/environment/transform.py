def transform(text):
    lines = text.strip().split('\n')
    result = []
    for line in lines:
        result.append(line[::-1].upper())
    return '\n'.join(result) + '\n'
