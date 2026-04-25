#!/usr/bin/env python3
"""
Helper functions untuk PurpleScan
"""

import ipaddress
import re
from pathlib import Path
from typing import List, Union


def validate_target(target: str) -> bool:
    """Validasi target IP, hostname, atau CIDR"""
    if not target:
        return False
    
    # Cek apakah CIDR
    try:
        ipaddress.ip_network(target, strict=False)
        return True
    except ValueError:
        pass
    
    # Cek IP tunggal
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass
    
    # Cek hostname sederhana
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\.-]*$', target):
        return True
    
    return False


def create_output_dirs(base_dir: str = "output") -> Path:
    """Buat folder output jika belum ada"""
    output_path = Path(base_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Buat subfolder
    (output_path / "nmap").mkdir(exist_ok=True)
    (output_path / "nikto").mkdir(exist_ok=True)
    
    return output_path


def get_web_url(host: str, port: int, service_name: str) -> str:
    """Generate URL web berdasarkan port dan service"""
    if port in [443, 8443] or "https" in service_name.lower():
        return f"https://{host}:{port}"
    else:
        return f"http://{host}:{port}"


def print_banner():
    """Tampilkan banner PurpleScan"""
    banner = """
    ╔══════════════════════════════════════════════╗
    ║              PURPLESCAN v0.1                 ║
    ║     Nmap + Nikto for Purple Team             ║
    ╚══════════════════════════════════════════════╝
    """
    print(banner)