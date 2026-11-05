import json
import os
import sys
os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")
from litellm.utils import token_counter
for line in open(sys.argv[1]):
    msgs = json.loads(line)
    try:
        print(token_counter(model="hosted_vllm/policy", messages=msgs))
    except Exception as e:
        print(f"error:{type(e).__name__}")
