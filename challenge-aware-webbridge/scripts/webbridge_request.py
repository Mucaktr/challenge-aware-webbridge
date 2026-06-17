#!/usr/bin/env python3
"""Send a Kimi WebBridge command with a UTF-8 JSON request body.

This helper keeps request formatting consistent across platforms. On Windows it
always uses `curl.exe` plus a temporary UTF-8 file body so non-ASCII content is
not corrupted by the shell.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True, help="Top-level session name")
    parser.add_argument("--action", required=True, help="WebBridge action name")
    parser.add_argument(
        "--args-json",
        default="{}",
        help="JSON object for action args. Defaults to an empty object.",
    )
    parser.add_argument(
        "--server-url",
        default="http://127.0.0.1:10086/command",
        help="Daemon command endpoint",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON responses",
    )
    return parser


def parse_args_json(raw: str) -> dict[str, Any]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("--args-json must decode to a JSON object")
    return value


def curl_binary() -> str:
    if platform.system().lower().startswith("win"):
        return "curl.exe"
    return shutil.which("curl") or "curl"


def invoke(
    *,
    session: str,
    action: str,
    args: dict[str, Any] | None = None,
    server_url: str = "http://127.0.0.1:10086/command",
) -> dict[str, Any]:
    body = {
        "action": action,
        "args": args or {},
        "session": session,
    }
    request_file = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            prefix="webbridge-req-",
            encoding="utf-8",
            delete=False,
        ) as handle:
            request_file = Path(handle.name)
            json.dump(body, handle, ensure_ascii=False)

        proc = subprocess.run(
            [
                curl_binary(),
                "-s",
                "-X",
                "POST",
                server_url,
                "-H",
                "Content-Type: application/json",
                "--data-binary",
                f"@{request_file}",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "curl failed")
        if not proc.stdout.strip():
            return {}
        return json.loads(proc.stdout)
    finally:
        if request_file and request_file.exists():
            request_file.unlink()


def main() -> int:
    parser = build_parser()
    ns = parser.parse_args()
    try:
        args = parse_args_json(ns.args_json)
        result = invoke(
            session=ns.session,
            action=ns.action,
            args=args,
            server_url=ns.server_url,
        )
    except Exception as exc:  # pragma: no cover - CLI surface
        print(str(exc), file=sys.stderr)
        return 1

    if ns.pretty:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
