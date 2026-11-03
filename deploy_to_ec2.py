# -*- coding: utf-8 -*-
"""
deploy_to_ec2.py
Deploys updated sia_user_manager.py, datasets, and test suite to EC2 (52.66.255.113),
restarts the ASGI server, and executes the 12-service verification suite on production.
"""

import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EC2_HOST = "ubuntu@52.66.255.113"
SSH_KEY = r"D:\Downloads\aws-bot-key.pem"
REMOTE_DIR = "/home/ubuntu/makkal-agent-ai"

FILES_TO_SCP = [
    r"D:\api\makkal-agent-ai\sia_user_manager.py",
    r"D:\api\makkal-agent-ai\data\makkal_domain_training_dataset.jsonl",
    r"D:\api\makkal-agent-ai\data\baseten_train.jsonl",
    r"D:\api\makkal-agent-ai\data\baseten_eval.jsonl",
    r"D:\api\makkal-agent-ai\test_all_12_services_3step_workflow.py",
]

def run_cmd(cmd, desc):
    print(f"\n[+] {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(f"[-] Command failed with code {res.returncode}:\n{res.stderr}\n{res.stdout}")
    else:
        print(f"[✓] {desc} successful.")
        if res.stdout.strip():
            print(res.stdout.strip()[:300])
    return res

def deploy():
    print("=" * 70)
    print("DEPLOYING 12-SERVICE 3-STEP DIRECT ACTION FLOW & DATASETS TO EC2")
    print("=" * 70)

    # 1. SCP main python files
    scp_cmd = [
        "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
        r"D:\api\makkal-agent-ai\sia_user_manager.py",
        r"D:\api\makkal-agent-ai\test_all_12_services_3step_workflow.py",
        f"{EC2_HOST}:{REMOTE_DIR}/"
    ]
    run_cmd(scp_cmd, "SCP sia_user_manager.py & test_all_12_services_3step_workflow.py")

    # 2. SCP data files
    scp_data_cmd = [
        "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
        r"D:\api\makkal-agent-ai\data\makkal_domain_training_dataset.jsonl",
        r"D:\api\makkal-agent-ai\data\baseten_train.jsonl",
        r"D:\api\makkal-agent-ai\data\baseten_eval.jsonl",
        f"{EC2_HOST}:{REMOTE_DIR}/data/"
    ]
    run_cmd(scp_data_cmd, "SCP training datasets to data/")

    # 3. Restart server on EC2
    restart_cmd = [
        "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
        EC2_HOST,
        f"cd {REMOTE_DIR} && ./start_server.sh"
    ]
    run_cmd(restart_cmd, "Restart ASGI server on EC2")

    # 4. Run test suite on EC2
    test_cmd = [
        "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
        EC2_HOST,
        f"cd {REMOTE_DIR} && python3 test_all_12_services_3step_workflow.py"
    ]
    run_cmd(test_cmd, "Execute 12-service 3-step test suite on EC2 production")

if __name__ == "__main__":
    deploy()
