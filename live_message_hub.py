# -*- coding: utf-8 -*-
"""
SIA (Super Intelligent Agent) - Real-Time Universal Live Message Hub
Meta AI Developer Hackathon 2026

Coordinates live real-time bidirectional synchronization between WhatsApp and
the Web App Citizen Workstation via Server-Sent Events (SSE).
Tracks:
- Real WhatsApp messages (incoming from citizens & outgoing from SIA)
- Web-simulated WhatsApp interactions
- Meta multi-model reasoning traces (Muse Spark Open 816B, Muse Wonder 1.0, SAM 3.1)
- Latency & token telemetry
"""

import json
import time
import asyncio
import logging
from typing import Dict, Any, List, Optional, AsyncGenerator
from collections import deque

logger = logging.getLogger("sia.live_hub")

# Maximum historical events kept in memory ring-buffer
MAX_HISTORY = 100

class LiveMessageHub:
    def __init__(self):
        self._history: deque = deque(maxlen=MAX_HISTORY)
        self._subscribers: List[asyncio.Queue] = []
        self._event_id: int = 0

    def publish_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        sender: str = "6381029380",
        model: str = "muse-spark-open-1026"
    ) -> Dict[str, Any]:
        """
        Publishes a message or system event to all connected web clients and stores in history.
        """
        self._event_id += 1
        payload = {
            "id": self._event_id,
            "timestamp": time.time(),
            "time_str": time.strftime("%H:%M:%S"),
            "event_type": event_type,  # 'wa_incoming', 'wa_outgoing', 'meta_reasoning', 'system_alert'
            "sender": sender,
            "model": model,
            "data": data
        }

        # Save to memory buffer
        self._history.append(payload)

        # Broadcast to all SSE active queues
        dead_subscribers = []
        for q in self._subscribers:
            try:
                q.put_nowait(payload)
            except Exception:
                dead_subscribers.append(q)

        for d in dead_subscribers:
            if d in self._subscribers:
                self._subscribers.remove(d)

        logger.info(f"[LIVE HUB] Published event #{self._event_id} ({event_type}) to {len(self._subscribers)} listeners")
        return payload

    async def event_generator(self, client_id: str = "web_client") -> AsyncGenerator[str, None]:
        """
        Async generator yielding SSE formatted strings for FastAPI StreamingResponse.
        """
        q = asyncio.Queue(maxsize=50)
        self._subscribers.append(q)
        logger.info(f"[LIVE HUB] Client {client_id} connected. Total subscribers: {len(self._subscribers)}")

        try:
            # First send initial connection heartbeat
            init_event = {
                "id": 0,
                "timestamp": time.time(),
                "time_str": time.strftime("%H:%M:%S"),
                "event_type": "connected",
                "sender": "system",
                "model": "meta-models/muse-spark-open-1026",
                "data": {"status": "connected", "client_id": client_id, "history_count": len(self._history)}
            }
            yield f"id: 0\nevent: message\ndata: {json.dumps(init_event, ensure_ascii=False)}\n\n"

            while True:
                try:
                    # Wait for next event with a 15-second heartbeat timeout
                    payload = await asyncio.wait_for(q.get(), timeout=15.0)
                    yield f"id: {payload['id']}\nevent: message\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
                except asyncio.TimeoutError:
                    # Send keep-alive ping comment to prevent socket timeout
                    yield f": keepalive {time.time()}\n\n"
        except asyncio.CancelledError:
            logger.info(f"[LIVE HUB] Client {client_id} disconnected.")
        finally:
            if q in self._subscribers:
                self._subscribers.remove(q)
            logger.info(f"[LIVE HUB] Cleaned subscriber {client_id}. Remaining: {len(self._subscribers)}")

    def get_recent_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns the most recent events from the in-memory ring buffer."""
        items = list(self._history)
        return items[-limit:] if limit < len(items) else items

    def clear(self):
        """Clears event history (useful for judge demo resets)."""
        self._history.clear()
        self._event_id = 0


# Singleton global hub instance
live_hub = LiveMessageHub()
