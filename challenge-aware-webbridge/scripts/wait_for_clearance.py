#!/usr/bin/env python3
"""Poll a WebBridge session until a verification page clears or times out."""

from __future__ import annotations

import argparse
import json
import time

from detect_verification_page import probe_session


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True, help="Top-level WebBridge session name")
    parser.add_argument(
        "--server-url",
        default="http://127.0.0.1:10086/command",
        help="Daemon command endpoint",
    )
    parser.add_argument(
        "--timeout-sec",
        type=float,
        default=90.0,
        help="Maximum wait time before giving up",
    )
    parser.add_argument(
        "--interval-sec",
        type=float,
        default=2.0,
        help="Polling interval",
    )
    parser.add_argument(
        "--expect-url-substring",
        default="",
        help="Optional URL substring that should be present after clearance",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main() -> int:
    ns = build_parser().parse_args()
    started = time.time()
    last = {}
    polls = 0

    while time.time() - started <= ns.timeout_sec:
        polls += 1
        last = probe_session(ns.session, ns.server_url)
        url_ok = True
        if ns.expect_url_substring:
            url_ok = ns.expect_url_substring in (last.get("url") or "")
        if not last.get("challenge_detected") and url_ok:
            result = {
                "cleared": True,
                "elapsed_sec": round(time.time() - started, 2),
                "polls": polls,
                "final": last,
            }
            print(json.dumps(result, indent=2 if ns.pretty else None, ensure_ascii=False))
            return 0
        time.sleep(ns.interval_sec)

    result = {
        "cleared": False,
        "elapsed_sec": round(time.time() - started, 2),
        "polls": polls,
        "final": last,
    }
    print(json.dumps(result, indent=2 if ns.pretty else None, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
