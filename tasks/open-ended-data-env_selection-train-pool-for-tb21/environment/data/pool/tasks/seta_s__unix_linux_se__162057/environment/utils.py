import re
import json


def sanitize_string(text):
  cleaned = text.strip()
  cleaned = re.sub(r'\s+', ' ', cleaned)
  return cleaned


def load_json_file(filepath):
  try:
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data
  except FileNotFoundError:
      return None
  except json.JSONDecodeError:
    return {}


def merge_dicts(base, override):
  result = dict(base)
  for key, value in override.items():
      if key in result and isinstance(result[key], dict):
        result[key] = merge_dicts(result[key], value)
      else:
        result[key] = value
  return result


def flatten_list(nested):
  flat = []
  for item in nested:
    if isinstance(item, list):
        flat.extend(flatten_list(item))
    else:
      flat.append(item)
  return flat
