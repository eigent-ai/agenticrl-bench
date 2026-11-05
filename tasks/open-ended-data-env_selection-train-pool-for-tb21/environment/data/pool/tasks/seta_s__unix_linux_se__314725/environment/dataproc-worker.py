#!/usr/bin/env python3
"""Data processing worker service."""
import os, json, time, signal, sys, logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

INBOX     = "/var/lib/dataproc/inbox"
PROCESSED = "/var/lib/dataproc/processed"
STATUS    = "/var/lib/dataproc/status"
POLL      = 5

running = True

def _stop(sig, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, _stop)
signal.signal(signal.SIGINT, _stop)

logger.info("dataproc-worker starting, polling every %ds", POLL)

while running:
    try:
        for fname in sorted(os.listdir(INBOX)):
            if fname.endswith(".json"):
                src = os.path.join(INBOX, fname)
                dst = os.path.join(PROCESSED, fname)
                with open(src) as f:
                    rec = json.load(f)
                rec["processed"] = True
                rec["processed_at"] = time.time()
                with open(dst, "w") as f:
                    json.dump(rec, f, indent=2)
                os.remove(src)
                logger.info("processed %s", fname)
        with open(STATUS, "w") as f:
            f.write(f"running\n{time.time()}\n")
    except Exception as exc:
        logger.error("worker error: %s", exc)
    time.sleep(POLL)
