# PurpleScan

Tools sederhana namun powerful untuk Purple Team yang menggabungkan **Nmap** dan **Nikto** dalam satu command.

## Fitur Saat Ini
- Scanning port dengan Nmap
- Auto detect web service (HTTP/HTTPS)
- Scanning vulnerability web dengan Nikto
- Output terorganisir

## Cara Penggunaan

```bash
python run.py -t 192.168.1.100
python run.py -t 192.168.56.0/24 --output output/lab_scan