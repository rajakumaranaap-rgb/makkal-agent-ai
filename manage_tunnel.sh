#!/bin/bash
# ==============================================================================
# Makkal Agent AI - Cloudflare Tunnel & Agent Persistent Supervisor
# Ensures 24x7 High Availability on AWS EC2 (52.66.255.113)
# Built for Meta AI Developer Hackathon 2026
# ==============================================================================

DIR="/home/ubuntu/makkal-agent-ai"
cd "$DIR" || exit 1

# 1. Ensure FastAPI Uvicorn Server is running on port 8001
if ! pgrep -f "uvicorn app:app" > /dev/null; then
    echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] [RECOVER] Uvicorn server was down. Restarting..."
    nohup .venv/bin/uvicorn app:app --host 0.0.0.0 --port 8001 --workers 2 > "$DIR/server.log" 2>&1 &
    sleep 2
fi

# 2. Check if local server is responsive
if ! curl -s --connect-timeout 3 http://127.0.0.1:8001/health > /dev/null; then
    echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] [WARNING] Local health check failed on 127.0.0.1:8001."
fi

# 3. Check if cloudflared is running; preserve existing session if alive
if ! pgrep -f "cloudflared tunnel" > /dev/null; then
    echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] [RECOVER] Cloudflared tunnel process not found. Launching..."
    tmux kill-session -t makkal_tunnel 2>/dev/null || true
    tmux new-session -d -s makkal_tunnel "/home/ubuntu/cloudflared tunnel --url http://127.0.0.1:8001 > /home/ubuntu/makkal_tunnel.log 2>&1"
    sleep 6
fi

# 4. Extract active URL from log
ACTIVE_URL=$(grep -o 'https://[-a-z0-9]*\.trycloudflare\.com' /home/ubuntu/makkal_tunnel.log | tail -n 1)

if [ -n "$ACTIVE_URL" ]; then
    echo "$ACTIVE_URL" > "$DIR/active_tunnel_url.txt"
    # Check remote health
    HEALTH=$(curl -s --connect-timeout 5 "$ACTIVE_URL/health")
    if echo "$HEALTH" | grep -q '"status":"online"'; then
        echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] [OK] Tunnel Healthy: $ACTIVE_URL"
    else
        echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] [WARN] Tunnel URL responded but health check failed: $HEALTH"
    fi
else
    echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] [WARN] No active trycloudflare URL found in log."
fi
