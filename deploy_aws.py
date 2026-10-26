"""
==============================================================================
Makkal Agent AI - AWS EC2 Deployment Pipeline
==============================================================================
Deploys and synchronizes Makkal Agent AI directly to production AWS EC2 instance:
Host: 52.66.255.113
Port: 8001
Engine: FastAPI + Uvicorn + Meta Model API + SAM 3.1 + WhatsApp Cloud API
Target Track: Meta AI Developer Hackathon 2026 ($150,000 Indie Developer Track)
==============================================================================
"""

import os
import sys
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

IP = "52.66.255.113"
KEY_PATH = r"D:\Downloads\aws-bot-key.pem"
REMOTE_USER = "ubuntu"
REMOTE_DIR = f"/home/ubuntu/makkal-agent-ai/"

FILES_TO_DEPLOY = [
    "app.py",
    "whatsapp_agent.py",
    "meta_client.py",
    "sam_document_auditor.py",
    "action_executor.py",
    "knowledge_base.py",
    "requirements.txt",
    ".env",
    "README.md"
]

print("==================================================")
print(f"🚀 Deploying Makkal Agent AI to AWS EC2 ({IP})...")
print("==================================================")

if not os.path.exists(KEY_PATH):
    print(f"❌ Error: AWS SSH key not found at {KEY_PATH}")
    sys.exit(1)

ssh_opts = ["-o", "StrictHostKeyChecking=no", "-i", KEY_PATH]

# Step 1: Ensure Remote Directories Exist
print("\n[1/4] Preparing remote deployment directory on EC2...")
mkdir_cmd = ["ssh"] + ssh_opts + [f"{REMOTE_USER}@{IP}", f"mkdir -p {REMOTE_DIR}uploads {REMOTE_DIR}generated_petitions"]
res_mkdir = subprocess.run(mkdir_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
if res_mkdir.returncode != 0:
    print(f"❌ Failed to create remote directory: {res_mkdir.stderr}")
    sys.exit(1)
print("  ✅ Remote directory created: /home/ubuntu/makkal-agent-ai/")

# Step 2: Upload Files via SCP
print("\n[2/4] Uploading agent core files to AWS EC2...")
local_base = os.path.dirname(os.path.abspath(__file__))
for fname in FILES_TO_DEPLOY:
    fpath = os.path.join(local_base, fname)
    if not os.path.exists(fpath):
        print(f"  ⚠️ Warning: {fname} not found locally, skipping.")
        continue
    sz = os.path.getsize(fpath) / 1024.0
    print(f"  • Uploading {fname} ({sz:.1f} KB)...")
    scp_cmd = ["scp"] + ssh_opts + [fpath, f"{REMOTE_USER}@{IP}:{REMOTE_DIR}{fname}"]
    res_scp = subprocess.run(scp_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res_scp.returncode != 0:
        print(f"  ❌ Failed to upload {fname}: {res_scp.stderr}")
        sys.exit(1)
print("  ✅ All application files uploaded successfully!")

# Step 3: Setup Virtualenv and Install Dependencies
print("\n[3/4] Configuring Python environment and dependencies on EC2...")
remote_setup_cmd = (
    f"cd {REMOTE_DIR} && "
    "python3 -m venv .venv && "
    ".venv/bin/pip install --upgrade pip && "
    ".venv/bin/pip install -r requirements.txt && "
    ".venv/bin/python3 -m py_compile app.py whatsapp_agent.py meta_client.py sam_document_auditor.py action_executor.py knowledge_base.py && "
    "echo PYTHON_ENV_READY"
)
ssh_setup = ["ssh"] + ssh_opts + [f"{REMOTE_USER}@{IP}", remote_setup_cmd]
res_setup = subprocess.run(ssh_setup, capture_output=True, text=True, encoding="utf-8", errors="replace")
if "PYTHON_ENV_READY" in res_setup.stdout:
    print("  ✅ Remote Python environment and syntax validation PASSED!")
else:
    print(f"  ⚠️ Remote setup output:\n{res_setup.stdout}\n{res_setup.stderr}")

# Step 4: Launch Service in Dedicated Tmux Window
print("\n[4/4] Starting Makkal Agent AI daemon on AWS EC2 (Port 8001)...")
remote_launch_cmd = (
    f"cd {REMOTE_DIR} && "
    "tmux kill-session -t makkal_agent 2>/dev/null || true; "
    "tmux new-session -d -s makkal_agent '.venv/bin/uvicorn app:app --host 0.0.0.0 --port 8001 --workers 2 > server.log 2>&1'; "
    "sleep 2; "
    "tmux ls; "
    "curl -s http://127.0.0.1:8001/health || echo HEALTH_CHECK_FAILED"
)
ssh_launch = ["ssh"] + ssh_opts + [f"{REMOTE_USER}@{IP}", remote_launch_cmd]
res_launch = subprocess.run(ssh_launch, capture_output=True, text=True, encoding="utf-8", errors="replace")
print("  Remote Service Status:")
print(res_launch.stdout)

print("\n==================================================")
print(f"🎉 MAKKAL AGENT AI DEPLOYED TO AWS EC2 ({IP})!")
print(f"🌐 Public Web Portal: http://{IP}:8001")
print(f"📱 WhatsApp Webhook: http://{IP}:8001/api/whatsapp/webhook")
print(f"🩺 Health Endpoint:  http://{IP}:8001/health")
print("==================================================")
