#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
#  War Lab • Linux Attack-Node  MINIMAL installer
#  Save as:  install_linux.sh      (chmod +x not required)
#  Run with: sudo bash install_linux.sh --adapters alfa,netgear
# ─────────────────────────────────────────────────────────

set -e  # exit on first error

REPO_URL="https://github.com/<YOUR-USERNAME>/warlab.git"  # ← replace!
INSTALL_DIR="/opt/warlab"
ADAPTERS="${1:-}"   # optional: alfa,netgear

echo "=== War Lab Attack-Node installer (minimal) ==="

# 1) refresh apt & upgrade
apt update -y && apt upgrade -y

# 2) core packages
apt install -y python3 git python3-venv aircrack-ng bettercap nmap ufw

# 3) clone (or pull) repo
if [ -d "$INSTALL_DIR" ]; then
  git -C "$INSTALL_DIR" pull
else
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 4) Python v-env & deps (only the very basics)
python3 -m venv "$INSTALL_DIR/.venv"
source "$INSTALL_DIR/.venv/bin/activate"
pip install -U pip wheel colorama  # add more later if needed

# 5) optional Alfa driver
if [[ "$ADAPTERS" == *"alfa"* ]]; then
  apt install -y realtek-rtl88xxau-dkms
fi

# 6) simple firewall opening gRPC port 5571
ufw allow OpenSSH
ufw allow 5571/tcp
ufw --force enable

echo -e "\n✅  Done.  Activate with:\n  source $INSTALL_DIR/.venv/bin/activate"
