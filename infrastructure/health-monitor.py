#!/usr/bin/env python3
"""
OSMX 24x7 Health Monitor — slot health checks and auto-recovery
Runs as a background watchdog. Usage:
  python3 health-monitor.py [--interval 300] [--once]
Part of: OSMX 24x7 Infrastructure
"""

import argparse
import json
import os
import subprocess
import sys
import time
import yaml
from datetime import datetime, timezone
from pathlib import Path

INFRA_DIR = Path(__file__).parent
POOL_CONFIG = INFRA_DIR / "agent-pool.yaml"
TASK_QUEUE = INFRA_DIR / "task-queue.yaml"
SLOTS_DIR = INFRA_DIR / "slots"
SLOT_MANAGER = INFRA_DIR / "slot-manager.sh"
LOG_FILE = INFRA_DIR / "logs" / "health-monitor.log"

def log(msg):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def save_yaml(path, data):
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def run_cmd(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, '', 'TIMEOUT'

def check_slot(slot_name, slot_config):
    """Check a single slot's health. Returns (healthy, details)."""
    session = slot_config.get('tmux_session', f'osmx-{slot_name}')
    state_file = SLOTS_DIR / f"{slot_name}.state"
    
    details = {
        'slot': slot_name,
        'session': session,
        'tmux_alive': False,
        'state_exists': state_file.exists(),
        'status': 'unknown',
        'issues': []
    }
    
    # Check tmux session
    rc, out, err = run_cmd(f"tmux has-session -t {session} 2>/dev/null")
    details['tmux_alive'] = (rc == 0)
    
    # Check state file
    if state_file.exists():
        state = {}
        for line in state_file.read_text().strip().splitlines():
            if '=' in line:
                k, v = line.split('=', 1)
                state[k] = v
        details['status'] = state.get('status', 'unknown')
        details['task_id'] = state.get('task_id', 'none')
        details['started_at'] = state.get('started_at', 'unknown')
        
        # If state says running but tmux dead
        if state.get('status') == 'running' and not details['tmux_alive']:
            details['issues'].append('SESSION_DIED')
        
        # Check duration — if running > 30min, might be stuck
        if state.get('started_at') and state.get('status') == 'running':
            try:
                started = datetime.fromisoformat(state['started_at'].replace('Z', '+00:00'))
                elapsed = (datetime.now(timezone.utc) - started).total_seconds()
                details['elapsed_seconds'] = int(elapsed)
                if elapsed > 1800:  # 30 min
                    details['issues'].append('LONG_RUNNING')
                if elapsed > 3600:  # 60 min
                    details['issues'].append('POSSIBLY_STUCK')
            except Exception:
                pass
    
    healthy = len(details['issues']) == 0
    return healthy, details

def check_system():
    """System-level health checks."""
    issues = []
    
    # Disk space
    rc, out, err = run_cmd("df -h /Users/apple | tail -1 | awk '{print $5}' | tr -d '%'")
    if rc == 0 and out:
        disk_pct = int(out)
        if disk_pct > 90:
            issues.append(f"DISK_CRITICAL: {disk_pct}% used")
        elif disk_pct > 80:
            issues.append(f"DISK_WARNING: {disk_pct}% used")
    
    # Memory pressure
    rc, out, err = run_cmd("memory_pressure 2>/dev/null || echo 'unknown'")
    
    # Check Go/AI/Frontend services
    for port, name in [(8080, 'go'), (5001, 'ai'), (25174, 'frontend')]:
        rc, out, err = run_cmd(f"curl -sf http://127.0.0.1:{port}/api/v1/health -o /dev/null && echo OK || echo DOWN")
        if 'DOWN' in out:
            issues.append(f"SERVICE_DOWN: {name} on port {port}")
    
    return issues

def auto_recover(slot_name, details):
    """Attempt automatic recovery for a failed slot."""
    issues = details.get('issues', [])
    
    if 'SESSION_DIED' in issues:
        log(f"  → Auto-recovering {slot_name}: restarting from last state")
        rc, out, err = run_cmd(f"bash {SLOT_MANAGER} restart {slot_name}")
        if rc == 0:
            log(f"  ✓ {slot_name} recovered")
            return True
        else:
            log(f"  ✗ {slot_name} recovery failed: {err}")
            return False
    
    if 'POSSIBLY_STUCK' in issues:
        log(f"  → {slot_name} possibly stuck (running >60min), logging but NOT auto-killing")
        # Could add auto-kill with max_attempts check here
        return False
    
    return False

def run_health_check(auto_recover_flag=False):
    """Run full health check."""
    pool = load_yaml(POOL_CONFIG)
    
    log("=== Health Check ===")
    
    # System checks
    sys_issues = check_system()
    if sys_issues:
        for issue in sys_issues:
            log(f"  ⚠ SYSTEM: {issue}")
    else:
        log("  ✓ System healthy")
    
    # Slot checks
    total_healthy = 0
    total_slots = 0
    for slot_name, slot_config in pool.get('slots', {}).items():
        total_slots += 1
        healthy, details = check_slot(slot_name, slot_config)
        
        if healthy:
            total_healthy += 1
            status = details.get('status', 'idle')
            task = details.get('task_id', 'none')
            log(f"  ✓ {slot_name}: {status} task={task}")
        else:
            issues_str = ', '.join(details['issues'])
            log(f"  ✗ {slot_name}: ISSUES=[{issues_str}]")
            if auto_recover_flag:
                auto_recover(slot_name, details)
    
    log(f"  Slots: {total_healthy}/{total_slots} healthy")
    return total_healthy == total_slots

def main():
    parser = argparse.ArgumentParser(description='OSMX 24x7 Health Monitor')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--auto-recover', action='store_true', help='Auto-recover failed slots')
    args = parser.parse_args()
    
    if args.once:
        healthy = run_health_check(auto_recover_flag=args.auto_recover)
        sys.exit(0 if healthy else 1)
    
    log(f"Starting health monitor (interval={args.interval}s)")
    while True:
        try:
            run_health_check(auto_recover_flag=args.auto_recover)
        except Exception as e:
            log(f"ERROR: {e}")
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
