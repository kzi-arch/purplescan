# PurpleScan

**PurpleScan** adalah tools automation untuk Purple Team yang menggabungkan beberapa scanner terbaik dalam satu command.

Menggabungkan kekuatan **Nmap**, **Nikto**, **Nuclei**, dan **ffuf** untuk reconnaissance dan vulnerability scanning yang efisien.

## Fitur Utama

- **Nmap** - Port scanning + service version detection
- **Nikto** - Web server vulnerability scanning (parallel)
- **Nuclei** - Modern template-based vulnerability scanner (CVE, misconfig, etc)
- **ffuf** - Fast directory and file brute-forcing
- **Professional Reporting** - HTML, TXT, dan JSON report
- **Multiple Scan Profiles**:
  - `default` - Seimbang
  - `quick` - Recon cepat
  - `deep` - Scan mendalam
  - `purple-stealth` - Mode evasion untuk testing detection
- **Evasion Support** - Random User-Agent + random delay
- **Parallel Scanning** - Mempercepat proses Nikto dan ffuf

## Persyaratan

- Python 3.8+
- Nmap
- Nikto
- Nuclei
- ffuf

### Install Dependencies Arch Linux

```bash
sudo pacman -S nmap nikto go
paru -S nuclei-bin ffuf
pip install -r requirements.txt