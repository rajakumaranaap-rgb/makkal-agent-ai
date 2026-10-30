# -*- coding: utf-8 -*-
"""
Test Client Helper providing transparent fallback to FastAPI TestClient
when local port 8001 or Cloudflare tunnel is not running.
"""
import sys
import os
import requests
from pathlib import Path
from urllib.parse import urlparse

repo_dir = str(Path(__file__).parent.resolve())
if repo_dir not in sys.path:
    sys.path.insert(0, repo_dir)

def get_test_client(base_url="http://127.0.0.1:8001"):
    """
    Returns (request_client, base_url).
    If base_url is reachable, returns (requests, base_url).
    Otherwise returns (FastAPITestClientAdapter, base_url).
    """
    try:
        r = requests.get(f"{base_url}/health", timeout=1.5)
        if r.status_code == 200:
            return requests, base_url
    except Exception:
        pass

    # Fallback to local FastAPI TestClient
    from fastapi.testclient import TestClient
    from app import app
    _client = TestClient(app)

    class Adapter:
        def __init__(self, c, base):
            self.c = c
            self.base = base

        def _clean_path(self, url):
            if url.startswith(self.base):
                return url[len(self.base):]
            if "trycloudflare.com" in url or "127.0.0.1" in url or "localhost" in url or "http" in url:
                p = urlparse(url)
                path = p.path or "/"
                if p.query:
                    path += "?" + p.query
                return path
            return url

        def get(self, url, *args, **kwargs):
            path = self._clean_path(url)
            kwargs.pop("timeout", None)
            return self.c.get(path, *args, **kwargs)

        def post(self, url, *args, **kwargs):
            path = self._clean_path(url)
            kwargs.pop("timeout", None)
            return self.c.post(path, *args, **kwargs)

        def put(self, url, *args, **kwargs):
            path = self._clean_path(url)
            kwargs.pop("timeout", None)
            return self.c.put(path, *args, **kwargs)

        def delete(self, url, *args, **kwargs):
            path = self._clean_path(url)
            kwargs.pop("timeout", None)
            return self.c.delete(path, *args, **kwargs)

    return Adapter(_client, base_url), base_url
