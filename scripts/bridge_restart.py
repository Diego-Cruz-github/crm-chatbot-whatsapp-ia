#!/usr/bin/env python3
"""
bridge_restart.py - Procedimento seguro de restart da bridge WhatsApp
Limpa tokens, mata processos orfaos e reinicia a bridge com verificacao.
"""

import subprocess
import time
import sys
from datetime import datetime


BRIDGE_NAME = "yasmin-bridge"
TOKEN_PATH = "/var/www/yasmin/data/tokens/yasmin"


def run_cmd(cmd, check=False):
    """Executa comando shell e retorna resultado."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  [WARN] Command failed: {cmd}")
        print(f"         {result.stderr.strip()}")
    return result


def stop_bridge():
    """Para a bridge via PM2."""
    print("  [1/5] Stopping bridge...")
    run_cmd(f"pm2 stop {BRIDGE_NAME}")
    time.sleep(2)
    print("        Done")


def kill_orphan_processes():
    """Mata processos chromium orfaos."""
    print("  [2/5] Killing orphan chromium processes...")
    run_cmd("pkill -9 chromium")
    time.sleep(1)
    print("        Done")


def clean_tokens():
    """Remove tokens antigos da sessao."""
    print("  [3/5] Cleaning session tokens...")
    run_cmd(f"rm -rf {TOKEN_PATH}")
    print("        Done")


def start_bridge():
    """Inicia a bridge via PM2."""
    print("  [4/5] Starting bridge...")
    run_cmd(f"pm2 start {BRIDGE_NAME}")
    print("        Done")


def verify_bridge(wait_seconds=20):
    """Verifica se a bridge subiu corretamente."""
    print(f"  [5/5] Waiting {wait_seconds}s for QR generation...")
    time.sleep(wait_seconds)

    result = run_cmd(f"pm2 show {BRIDGE_NAME} --no-color")
    if "online" in result.stdout:
        print("        [OK] Bridge is ONLINE")
        return True
    print("        [FAIL] Bridge did not start properly")
    return False


def safe_restart():
    """Executa restart seguro completo."""
    print(f"\n[{datetime.utcnow().isoformat()}] WhatsApp Bridge Safe Restart")
    print("-" * 50)

    stop_bridge()
    kill_orphan_processes()
    clean_tokens()
    start_bridge()
    ok = verify_bridge()

    print("-" * 50)
    if ok:
        print("  [OK] Bridge restarted successfully")
        print("  [INFO] Scan QR code at /qr endpoint")
    else:
        print("  [FAIL] Bridge restart failed - check logs")
        print("  Run: pm2 logs yasmin-bridge --lines 50")

    return ok


if __name__ == "__main__":
    ok = safe_restart()
    sys.exit(0 if ok else 1)
