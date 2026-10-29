#!/usr/bin/env python3
"""Fail if anything that looks sensitive is about to be published.

Generic checks are built in (IPv4 addresses, private keys, tokens, home
paths, SSH port flags...). Personal values that must never leak (real IPs,
usernames, hostnames) are NOT written here, because this repo is public:
put them, one regex per line, in the `SENSITIVE_PATTERNS` repository secret
(or a local, git-ignored `.sensitive-patterns` file).
"""

from __future__ import annotations

import ipaddress
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN = [ROOT / "docs", ROOT / "data", ROOT / "mkdocs.yml", ROOT / "README.md"]
EXTENSIONS = {".md", ".yml", ".yaml", ".json", ".html", ".svg", ".txt"}

# Addresses that are fine to show (documentation / loopback / Docker defaults).
ALLOWED_NETS = [ipaddress.ip_network(n) for n in ("127.0.0.0/8", "0.0.0.0/32", "192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24")]
IPV4 = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,3}){3})(?:/\d{1,2})?(?![\d.])")

GENERIC = {
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{20,}",
    "AWS key": r"\bAKIA[0-9A-Z]{16}\b",
    "secret assignment": r"(?i)\b(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_\-]{8,}",
    "home path": r"/home/[a-z_][a-z0-9_-]*/",
    "ssh port flag": r"\bssh\b[^\n]*\s-p\s*\d+",
    "mount path": r"/mnt/[A-Za-z0-9_-]+",
}


def load_private_patterns() -> list[str]:
    raw = os.environ.get("SENSITIVE_PATTERNS", "")
    local = ROOT / ".sensitive-patterns"
    if local.exists():
        raw += "\n" + local.read_text(encoding="utf-8")
    return [l.strip() for l in raw.splitlines() if l.strip() and not l.strip().startswith("#")]


def files() -> list[Path]:
    result = []
    for target in SCAN:
        if target.is_file():
            result.append(target)
        elif target.is_dir():
            result += [p for p in target.rglob("*") if p.is_file() and p.suffix in EXTENSIONS]
    return result


def main() -> int:
    checks = [(name, re.compile(rx)) for name, rx in GENERIC.items()]
    checks += [(f"private pattern #{i + 1}", re.compile(rx, re.I)) for i, rx in enumerate(load_private_patterns())]
    problems = []
    for path in files():
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for match in IPV4.finditer(line):
                try:
                    ip = ipaddress.ip_address(match.group(1))
                except ValueError:
                    continue
                if not any(ip in net for net in ALLOWED_NETS):
                    problems.append(f"{rel}:{lineno}: IPv4 address {ip}")
            for name, rx in checks:
                if rx.search(line):
                    problems.append(f"{rel}:{lineno}: {name}")
    if problems:
        print("Possible sensitive data found:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    print(f"No sensitive data found in {len(files())} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
