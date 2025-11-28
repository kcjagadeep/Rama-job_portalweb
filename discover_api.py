#!/usr/bin/env python3
import requests

base_url = "http://34.232.76.115:8021"
endpoints = ["/", "/tts", "/synthesize", "/v1/tts", "/v2/tts", "/api/tts", "/generate"]

print("🔍 Discovering IndicF5 API endpoints...")
for endpoint in endpoints:
    try:
        url = f"{base_url}{endpoint}"
        response = requests.get(url, timeout=5)
        print(f"✅ {endpoint}: {response.status_code}")
        if response.status_code == 200:
            print(f"   Content: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ {endpoint}: {str(e)[:50]}...")