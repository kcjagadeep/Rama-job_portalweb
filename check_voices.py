#!/usr/bin/env python3
"""
Check available voices from TTS API
"""
import requests

def get_available_voices():
    """Get list of available voices"""
    api_key = "sk_jWLTvSRsgUBU0tc-itmrlBwUCQzyz-mw_aiudQphfpg"
    
    headers = {
        'accept': 'application/json',
        'xi-api-key': api_key
    }
    
    try:
        response = requests.get("http://34.232.76.115/v1/voices", headers=headers, timeout=10)
        
        if response.status_code == 200:
            voices = response.json()
            print("Available Voices:")
            print("=" * 40)
            
            if isinstance(voices, dict) and 'voices' in voices:
                voices = voices['voices']
            
            for voice in voices:
                voice_id = voice.get('voice_id', voice.get('id', 'Unknown'))
                name = voice.get('name', 'Unknown')
                gender = voice.get('gender', voice.get('labels', {}).get('gender', 'Unknown'))
                print(f"ID: {voice_id}")
                print(f"Name: {name}")
                print(f"Gender: {gender}")
                print("-" * 20)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_available_voices()