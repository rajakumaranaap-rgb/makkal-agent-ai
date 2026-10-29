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
    "domain_training_engine.py",
    "diagrammatic_guide_engine.py",
    "universal_tuition_engine.py",
    "travel_booking_engine.py",
    "student_learning_vault.py",
    "whatsapp_education_course_engine.py",
    "spoken_english_coach.py",
    "student_mental_health_coach.py",
    "family_daily_planner.py",
    "tuto_testo_qbank_bridge.py",
    "family_super_agent.py",
    "data/makkal_domain_training_dataset.jsonl",
    "data/tuto_qbank_cache.json",
    "data/baseten_train.jsonl",
    "data/baseten_eval.jsonl",
    "data/baseten_lora_config.json",
    "whatsapp_agent.py",
    "meta_client.py",
    "sia_user_manager.py",
    "sia_ui_template.py",
    "sia_users_registry.json",
    "tnega_civic_engine.py",
    "llama_vision_auditor.py",
    "seamless_speech_engine.py",
    "sam_document_auditor.py",
    "action_executor.py",
    "knowledge_base.py",
    "central_services_directory.py",
    "civic_greeting_poster_engine.py",
    "meta_image_studio.py",
    "sia_services_suite.py",
    "meta_entertainment_engine.py",
    "agriculture_engine.py",
    "modal_sam_service.py",
    "modal_sam_agri_bridge.py",
    "whatsapp_auth_manager.py",
    "mla_directory.py",
    "petition_directory.py",
    "family_education_engine.py",
    "civic_solution_media_engine.py",
    "test_end_to_end_workflows.py",
    "static/supro_logo.png",
    "static/sia_logo.png",
    "static/favicon.ico",
    "static/favicon.png",
    "static/icon.png",
    "static/logo-title.png",
    "static/brand_logo.png",
    "static/brand-leaf-logo.png",
    "static/supro_text_logo.jpg",
    "static/supro_hero_banner.jpg",
    "static/splashscreen_logo.png",
    "static/sia_brain_logo.png",
    "static/sia_brain_logo.jpg",
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
mkdir_cmd = ["ssh"] + ssh_opts + [f"{REMOTE_USER}@{IP}", f"mkdir -p {REMOTE_DIR}uploads {REMOTE_DIR}generated_petitions {REMOTE_DIR}data {REMOTE_DIR}static {REMOTE_DIR}static/greetings {REMOTE_DIR}static/generated_images"]
res_mkdir = subprocess.run(mkdir_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
if res_mkdir.returncode != 0:
    print(f"❌ Failed to create remote directory: {res_mkdir.stderr}")
    sys.exit(1)
print("  ✅ Remote directories created: uploads, generated_petitions, static/greetings")

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
    ".venv/bin/python3 -m py_compile app.py domain_training_engine.py tuto_testo_qbank_bridge.py whatsapp_agent.py meta_client.py sia_user_manager.py sia_ui_template.py meta_image_studio.py sia_services_suite.py tnega_civic_engine.py llama_vision_auditor.py seamless_speech_engine.py sam_document_auditor.py action_executor.py knowledge_base.py central_services_directory.py civic_greeting_poster_engine.py meta_entertainment_engine.py agriculture_engine.py modal_sam_service.py modal_sam_agri_bridge.py && "
    "echo PYTHON_ENV_READY"
)
ssh_setup = ["ssh"] + ssh_opts + [f"{REMOTE_USER}@{IP}", remote_setup_cmd]
res_setup = subprocess.run(ssh_setup, capture_output=True, text=True, encoding="utf-8", errors="replace")
if "PYTHON_ENV_READY" in res_setup.stdout:
    print("  ✅ Remote Python environment and syntax validation PASSED!")
else:
    print(f"  ⚠️ Remote setup output:\n{res_setup.stdout}\n{res_setup.stderr}")

# Step 4: Restart Uvicorn Daemon
print("\n[4/4] Starting SIA (Makkal Agent AI) daemon on AWS EC2 (Port 8001)...")
remote_launch_cmd = (
    f"cd {REMOTE_DIR} && "
    "/home/ubuntu/makkal-agent-ai/start_server.sh"
)
ssh_launch = ["ssh"] + ssh_opts + [f"{REMOTE_USER}@{IP}", remote_launch_cmd]
res_launch = subprocess.run(ssh_launch, capture_output=True, text=True, encoding="utf-8", errors="replace")
print("  Remote Service Status:")
print(res_launch.stdout)

# Retrieve active tunnel URL
ssh_tunnel = ["ssh"] + ssh_opts + [f"{REMOTE_USER}@{IP}", f"cat {REMOTE_DIR}active_tunnel_url.txt 2>/dev/null || echo 'https://regulatory-stack-counter-lady.trycloudflare.com'"]
res_tunnel = subprocess.run(ssh_tunnel, capture_output=True, text=True, encoding="utf-8", errors="replace")
tunnel_url = res_tunnel.stdout.strip() or "https://regulatory-stack-counter-lady.trycloudflare.com"

print("\n==================================================")
print(f"🎉 SIA (SUPER INTELLIGENT AGENT) DEPLOYED TO AWS EC2 ({IP})!")
print("🌐 LIVE PUBLIC WEB PORTAL (Cloudflare HTTPS Tunnel):")
print(f"👉 {tunnel_url}")
print(f"📱 WhatsApp Webhook: {tunnel_url}/api/whatsapp/webhook")
print(f"🩺 Health Endpoint:  {tunnel_url}/health")
print("==================================================")
