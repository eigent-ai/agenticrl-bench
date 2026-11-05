import json
import urllib2
from ConfigParser import SafeConfigParser
from StringIO import StringIO

from processor.pipeline import Pipeline

DEFAULT_CONFIG = """[processing]
batch_size = 100
timeout = 30
normalize = true
"""


def load_config():
    parser = SafeConfigParser()
    parser.readfp(StringIO(DEFAULT_CONFIG))
    return {
        "batch_size": parser.getint("processing", "batch_size"),
        "timeout": parser.getint("processing", "timeout"),
        "normalize": parser.getboolean("processing", "normalize")
    }


def transform_record(record):
    record["status"] = "processed"
    record["valid"] = True
    score = record.get("score", 0)
    if score < 0 or score > 100:
        record["valid"] = False
        record["status"] = "invalid"
    record["score"] = max(0.0, min(100.0, score))
    if not record.get("name", "").strip():
        record["valid"] = False
        record["status"] = "invalid"
    return record


def get_pipeline_class():
    return Pipeline


def fetch_remote_config(url):
    response = urllib2.urlopen(url)
    return response.read()
