"""Terminate every sandbox the calling user holds on a broker (run by rld as the service user after a job).
    python3 broker_cleanup.py [--socket /run/rl-broker.sock]"""
import argparse
import json

from sandbox_broker.client import BrokerClient

ap = argparse.ArgumentParser()
ap.add_argument("--socket", default="/run/rl-broker.sock")
a = ap.parse_args()
c = BrokerClient(a.socket)
n = 0
for sb in c.list():
    try:
        c.sandbox(sb["id"]).terminate()
        n += 1
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"id": sb.get("id"), "error": str(e)[:200]}))
print(json.dumps({"terminated": n}))
