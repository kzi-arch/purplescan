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
    if not target or not isinstance(target, str):
        return False
    
    # Cek CIDR
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


def create_output_dirs(base_dir: str = "output", clean: bool = True) -> Path:
    """Buat folder output, dengan opsi hapus isi lama"""
    base_path = Path(base_dir).resolve()
    
    if clean and base_path.exists():
        # Hapus isi folder lama (tapi biarkan folder tetap ada)
        for item in base_path.iterdir():
            if item.is_dir():
                import shutil
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)
    
    base_path.mkdir(parents=True, exist_ok=True, mode=0o755)
    
    # Buat subfolder
    subfolders = ["nmap", "nikto", "nuclei", "ffuf"]
    for folder in subfolders:
        (base_path / folder).mkdir(parents=True, exist_ok=True, mode=0o755)
    
    return base_path


def get_web_url(host: str, port: int, service_name: str) -> str:
    """Generate URL web berdasarkan port"""
    if port in [443, 8443] or 'https' in service_name.lower():
        return f"https://{host}:{port}"
    return f"http://{host}:{port}"


def print_banner():
    """Tampilkan banner PurpleScan"""
    banner = r"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    PURPLESCAN v0.5                           ║
    ║           Nmap + Nikto for Purple Team                       ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)