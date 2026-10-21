# -*- coding: utf-8 -*-
"""MCP Server for LTL Freight NMFC Density & Reclassification Dispute Arbiter Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import LTLFreightNMFCDensityReclassifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "calculate_freight_density_and_nmfc_class",
        "description": "Calculate shipment cubic feet, density (PCF), and mapped National Motor Freight Classification (NMFC) tier.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "length_inches": {
                    "type": "number"
                },
                "width_inches": {
                    "type": "number"
                },
                "height_inches": {
                    "type": "number"
                },
                "weight_lbs": {
                    "type": "number"
                }
            },
            "required": [
                "length_inches",
                "width_inches",
                "height_inches",
                "weight_lbs"
            ]
        }
    },
    {
        "name": "audit_carrier_w_and_r_chargeback",
        "description": "Audit carrier Weight & Inspection (W&R) re-classification fee chargeback against verified packaging spec.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carrier_billed_class": {
                    "type": "integer"
                },
                "actual_verified_class": {
                    "type": "integer"
                },
                "billed_rate_usd": {
                    "type": "number"
                },
                "fuel_surcharge_pct": {
                    "type": "number"
                }
            },
            "required": [
                "carrier_billed_class",
                "actual_verified_class",
                "billed_rate_usd"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-ltl-freight-nmfc-density-reclassifier-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(LTLFreightNMFCDensityReclassifier, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-ltl-freight-nmfc-density-reclassifier-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
