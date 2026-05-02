# PurpleScan v0.5.0

Tools automation **Purple Team** yang menggabungkan Nmap, Nikto, Nuclei, dan ffuf dalam satu command.

## Fitur

- Port & Service Scanning (Nmap)
- Web Vulnerability Scanning (Nikto)
- CVE & Template Vulnerability (Nuclei)
- Directory & File Brute-Force (ffuf)
- Professional Report (HTML, TXT, JSON)
- Multiple Profile: `default`, `quick`, `deep`, `purple-stealth`
- Evasion Support (Random User-Agent + Delay)

## Cara Install (Arch Linux)

```bash
# Install tools
sudo pacman -S nmap nikto go
paru -S nuclei-bin ffuf

# Install Python dependencies
cd ~/purplescan
pip install -r requirements.txt