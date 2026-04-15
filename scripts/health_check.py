#!/usr/bin/env python3
"""
health_check.py - Monitoramento do CRM e WhatsApp Bridge
Verifica API backend, bridge WhatsApp e providers de IA.
"""

import requests
import sys
from datetime import datetime


SERVICES = {
    "backend": {"port": 5000, "path": "/api/health"},
    "bridge": {"port": 3001, "path": "/status"},
}

AI_PROVIDERS = [
    {"name": "Groq", "url": "https://api.groq.com/openai/v1/models"},
    {"name": "Cloudflare", "url": "https://api.cloudflare.com/client/v4/user/tokens/verify"},
]


def check_local_service(name, port, path, timeout=10):
    """Verifica servico local."""
    url = f"http://localhost:{port}{path}"
    try:
        resp = requests.get(url, timeout=timeout)
        elapsed = int(resp.elapsed.total_seconds() * 1000)
        status = "OK" if resp.status_code == 200 else "WARN"
        print(f"  [{status}] {name}: HTTP {resp.status_code} ({elapsed}ms)")
        return resp.status_code == 200
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        return False


def check_ai_provider(name, url, timeout=10):
    """Verifica conectividade com provider de IA."""
    try:
        resp = requests.get(url, timeout=timeout)
        reachable = resp.status_code < 500
        status = "OK" if reachable else "WARN"
        print(f"  [{status}] {name}: reachable ({resp.status_code})")
        return reachable
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        return False


def run_checks():
    """Executa verificacao completa."""
    print(f"\n[{datetime.utcnow().isoformat()}] CRM + WhatsApp Health Check")
    print("-" * 50)

    print("\n  Local services:")
    local_ok = all(
        check_local_service(name, cfg["port"], cfg["path"])
        for name, cfg in SERVICES.items()
    )

    print("\n  AI providers:")
    ai_ok = any(
        check_ai_provider(p["name"], p["url"])
        for p in AI_PROVIDERS
    )

    all_ok = local_ok and ai_ok
    print("\n" + "-" * 50)
    print(f"  Result: {'ALL HEALTHY' if all_ok else 'ISSUES DETECTED'}")
    return all_ok


if __name__ == "__main__":
    ok = run_checks()
    sys.exit(0 if ok else 1)
