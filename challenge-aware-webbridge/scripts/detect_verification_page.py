#!/usr/bin/env python3
"""Detect likely browser verification interstitials in a WebBridge session."""

from __future__ import annotations

import argparse
import json
from typing import Any

from webbridge_request import invoke


CHALLENGE_CUES = [
    "checking your browser",
    "verify you are human",
    "security check",
    "captcha",
    "turnstile",
    "cf-turnstile",
    "checkloading",
    "bir dakika lutfen",
    "guvenlik dogrulamasi",
]


def normalize(text: str) -> str:
    table = str.maketrans(
        {
            "I": "i",
            "İ": "i",
            "ı": "i",
            "Ş": "s",
            "ş": "s",
            "Ğ": "g",
            "ğ": "g",
            "Ü": "u",
            "ü": "u",
            "Ö": "o",
            "ö": "o",
            "Ç": "c",
            "ç": "c",
        }
    )
    return text.translate(table).lower()


def call_evaluate(session: str, server_url: str) -> dict[str, Any]:
    code = """JSON.stringify((() => {
      const text = (document.body && document.body.innerText ? document.body.innerText : "").slice(0, 4000);
      const token = document.querySelector('[name=\"cf-turnstile-response\"]');
      return {
        title: document.title || "",
        href: location.href || "",
        body_excerpt: text,
        cf_turnstile: !!document.querySelector('.cf-turnstile,[name=\"cf-turnstile-response\"]'),
        token_length: token && token.value ? token.value.length : 0
      };
    })())"""
    result = invoke(
        session=session,
        action="evaluate",
        args={"code": code},
        server_url=server_url,
    )
    payload = result.get("data", {})
    if payload.get("type") != "string":
        return {}
    return json.loads(payload.get("value") or "{}")


def call_snapshot(session: str, server_url: str) -> dict[str, Any]:
    result = invoke(
        session=session,
        action="snapshot",
        args={},
        server_url=server_url,
    )
    return result.get("data", {}) if isinstance(result, dict) else {}


def detect_provider(haystack: str) -> str | None:
    if "cloudflare" in haystack or "turnstile" in haystack or "cf-turnstile" in haystack:
        return "cloudflare"
    if "hcaptcha" in haystack:
        return "hcaptcha"
    if "recaptcha" in haystack:
        return "recaptcha"
    if "captcha" in haystack or "verify" in haystack:
        return "generic"
    return None


def probe_session(session: str, server_url: str) -> dict[str, Any]:
    evaluated = call_evaluate(session, server_url)
    snapshot = call_snapshot(session, server_url)
    title = evaluated.get("title") or snapshot.get("title") or ""
    href = evaluated.get("href") or snapshot.get("url") or ""
    body_excerpt = evaluated.get("body_excerpt") or ""
    tree_excerpt = str(snapshot.get("tree") or "")[:2500]
    combined = normalize("\n".join([title, href, body_excerpt, tree_excerpt]))
    reasons = [cue for cue in CHALLENGE_CUES if cue in combined]
    detected = bool(reasons)
    provider = detect_provider(combined)
    token_length = int(evaluated.get("token_length") or 0)
    next_step = (
        "Ask the user to complete the verification manually, then wait for clearance."
        if detected
        else "Resume normal browsing."
    )
    return {
        "session": session,
        "url": href,
        "title": title,
        "challenge_detected": detected,
        "provider": provider,
        "reasons": reasons,
        "token_present": token_length > 0,
        "token_length": token_length,
        "cf_turnstile_present": bool(evaluated.get("cf_turnstile")),
        "next_step": next_step,
        "body_excerpt": body_excerpt[:700],
        "tree_excerpt": tree_excerpt[:700],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True, help="Top-level WebBridge session name")
    parser.add_argument(
        "--server-url",
        default="http://127.0.0.1:10086/command",
        help="Daemon command endpoint",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main() -> int:
    ns = build_parser().parse_args()
    result = probe_session(ns.session, ns.server_url)
    if ns.pretty:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
