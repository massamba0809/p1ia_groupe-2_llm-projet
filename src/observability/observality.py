"""Observabilité minimale : une ligne JSON par requête (latence, tokens, coût)."""
import json
import os
import time

import config

PRICE_IN = float(os.getenv("PRICE_IN_PER_M", "0"))   
PRICE_OUT = float(os.getenv("PRICE_OUT_PER_M", "0"))


def log(record: dict):
    record["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    record["cost_usd"] = round((record.get("tokens_in", 0) * PRICE_IN
                                + record.get("tokens_out", 0) * PRICE_OUT) / 1e6, 6)
    config.LOG_FILE.parent.mkdir(exist_ok=True)
    with open(config.LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
