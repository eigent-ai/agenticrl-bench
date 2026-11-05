"""python -m terminal_rl.proxy --model-path /models/GLM-4.7-Flash --engine-url http://127.0.0.1:30000 --port 8100"""

import argparse
import json
import logging

from aiohttp import web
from transformers import AutoTokenizer

from terminal_rl.proxy.server import ProxyApp


def main(argv=None):
    p = argparse.ArgumentParser(prog="terminal_rl.proxy")
    p.add_argument("--model-path", required=True, help="HF model or tokenizer dir (chat template is read from it)")
    p.add_argument("--engine-url", required=True, help="SGLang router/server base URL")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8100)
    p.add_argument("--served-model-name", default="policy")
    p.add_argument("--chat-template-kwargs", default="{}", help="JSON object passed to apply_chat_template")
    p.add_argument("--reasoning-parser", default="think", choices=["think", "none"])
    p.add_argument("--tool-call-parser", default="none", choices=["glm47", "none"])
    p.add_argument("--context-length", type=int, default=65536)
    p.add_argument("--default-max-tokens", type=int, default=8192)
    p.add_argument("--log-level", default="INFO")
    args = p.parse_args(argv)

    logging.basicConfig(level=args.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
    proxy = ProxyApp(
        tokenizer,
        args.engine_url,
        served_model_name=args.served_model_name,
        template_kwargs=json.loads(args.chat_template_kwargs),
        reasoning_parser=args.reasoning_parser,
        tool_call_parser=args.tool_call_parser,
        context_length=args.context_length,
        default_max_tokens=args.default_max_tokens,
    )
    web.run_app(proxy.build_app(), host=args.host, port=args.port, access_log=None)


if __name__ == "__main__":
    main()
