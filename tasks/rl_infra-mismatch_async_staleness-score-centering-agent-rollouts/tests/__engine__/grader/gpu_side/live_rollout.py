import argparse
import asyncio
import json
import os
import pickle
import sys
import time
import traceback
from unittest.mock import patch
import httpx
ap = argparse.ArgumentParser()
ap.add_argument("--cases", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--router", required=True)
a = ap.parse_args()
import live_env
import replay
from argv import build_argv
CASES = json.load(open(a.cases))
TIMEOUT_ROLLOUT = 600
def live_argv(case):
    argv = [x.replace("replay.", "live_env.", 1) if x.startswith("replay.") else x
            for x in build_argv(case, router=a.router)]
    if any(x.startswith("replay.") for x in argv):
        raise RuntimeError("replay function left in the live command line")
    return argv
async def run_case(case, out_dir):
    from miles.rollout.inference_rollout.inference_rollout_common import GenerateState, generate_and_rm
    from miles.utils import http_utils
    from miles.utils.arguments import parse_args
    from miles.utils.http_utils import init_http_client
    from miles.utils.types import Sample
    with patch("sys.argv", ["train.py"] + live_argv(case)):
        args = parse_args()
    http_utils._http_client = None
    init_http_client(args)
    server = None
    if case["recipe"] == "session":
        from miles.rollout.session.config import compute_session_server_config
        from miles.rollout.session.server import SessionServer
        from miles.rollout.session.types import SessionServerInstance
        from miles.utils.test_utils.uvicorn_thread_server import UvicornThreadServer
        port = int(case["session_port"])
        instance_id = f"{args.run_uuid}-0"
        args.session_server_instances = [SessionServerInstance(addr=f"127.0.0.1:{port}", instance_id=instance_id)]
        cfg = compute_session_server_config(args, host="127.0.0.1", port=port, instance_id=instance_id,
                                            backend_url=f"http://{a.router}")
        server = UvicornThreadServer(SessionServer(cfg).app, host="127.0.0.1", port=port)
        server.start()
    try:
        state = GenerateState(args)
        samples = []
        index = 0
        async with httpx.AsyncClient(timeout=30) as client:
            for gi, group in enumerate(case["prompts"]):
                for j, src in enumerate(group):
                    rec = replay.data()[src]
                    uid = f"{case['id'].replace('-', '_')}_{gi}_{j}"
                    r = float(case["live_rewards"][j % len(case["live_rewards"])])
                    (await client.post(f"http://{a.router}/_live/begin", json={"uid": uid})).raise_for_status()
                    live_env.CURRENT["reward"] = r
                    prompt = rec["prompt_messages"] if case["recipe"] == "session" else rec["prompt_text"]
                    s = Sample(prompt=prompt, label="{}", metadata={"live_uid": uid, "live_reward": r}, index=index,
                               group_index=gi)
                    s.rollout_id = index
                    index += 1
                    out = await asyncio.wait_for(generate_and_rm(state, s, dict(state.sampling_params)),
                                                 timeout=TIMEOUT_ROLLOUT)
                    outs = out if isinstance(out, list) else [out]
                    for o in outs:
                        if o.status == Sample.Status.ABORTED:
                            raise RuntimeError(f"live rollout {uid} aborted")
                        o.metadata = {**(o.metadata or {}), "live_uid": uid}
                    samples.extend(outs)
            (await client.post(f"http://{a.router}/_live/begin", json={"uid": None})).raise_for_status()
        from miles.ray.rollout.train_data_conversion import convert_samples_to_train_data
        train_data = convert_samples_to_train_data(args, samples, {}, None, None)
        with open(os.path.join(out_dir, "train_data.pkl"), "wb") as f:
            pickle.dump(train_data, f)
        summary = [{"tokens": list(map(int, s.tokens)), "response_length": int(s.response_length),
                    "loss_mask": list(map(int, s.loss_mask or [])), "status": str(s.status),
                    "uid": (s.metadata or {}).get("live_uid")} for s in samples]
        with open(os.path.join(out_dir, "samples.json"), "w") as f:
            json.dump(summary, f)
    finally:
        if server is not None:
            server.stop()
def main():
    status = {}
    for case in CASES:
        out_dir = os.path.join(a.out, case["id"])
        os.makedirs(out_dir, exist_ok=True)
        t0 = time.time()
        try:
            asyncio.run(run_case(case, out_dir))
            status[case["id"]] = {"ok": True, "s": round(time.time() - t0, 1)}
        except BaseException as e:
            status[case["id"]] = {"ok": False, "s": round(time.time() - t0, 1),
                                  "error": f"{type(e).__name__}: {e}"[:2000], "tb": traceback.format_exc()[-6000:]}
        print(json.dumps({case["id"]: {k: v for k, v in status[case["id"]].items() if k != "tb"}}), flush=True)
        if "tb" in status[case["id"]]:
            print(status[case["id"]]["tb"], file=sys.stderr, flush=True)
        with open(os.path.join(a.out, "rollout_status.json"), "w") as f:
            json.dump(status, f)
main()
sys.exit(0)
