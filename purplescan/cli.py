#!/usr/bin/env python3
"""
CLI - Command Line Interface untuk PurpleScan
"""

import argparse
import sys
from rich.console import Console

from .core import PurpleScanCore
from .config import config
from .utils.helpers import validate_target

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="PurpleScan - Gabungan Nmap & Nikto untuk Purple Team",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("-t", "--target", 
                        required=True,
                        help="Target scan: IP, hostname, atau CIDR (contoh: 192.168.1.10 atau 192.168.1.0/24)")
    
    parser.add_argument("-p", "--ports",
                        help="Port yang akan discan (override default)")
    
    parser.add_argument("-o", "--output",
                        help="Folder output (default: output/)")
    
    parser.add_argument("--profile",
                        choices=["quick", "deep", "purple-stealth"],
                        default="default",
                        help="Gunakan profile konfigurasi tertentu")
    
    parser.add_argument("--evasion", 
                        action="store_true",
                        help="Aktifkan mode evasion (delay antar scan)")
    
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Mode verbose")

    parser.add_argument("--os", 
                        action="store_true",
                        help="Aktifkan OS detection (-O). Harus dijalankan dengan sudo.")

    args = parser.parse_args()

    # Validasi target
    if not validate_target(args.target):
        console.print("[bold red]Error: Target tidak valid. Gunakan IP, hostname, atau CIDR yang benar.[/bold red]")
        sys.exit(1)

    # Load konfigurasi tambahan jika ada profile
    if args.profile != "default":
        try:
            config.load_config(f"config/{args.profile}.yaml")
            console.print(f"[blue]Menggunakan profile: {args.profile}[/blue]")
        except Exception as e:
            console.print(f"[yellow]Warning: Gagal load profile {args.profile}. Menggunakan default.[/yellow]")

    # Override evasion jika flag digunakan
    if args.evasion:
        config.config.setdefault("evasion", {})["enabled"] = True

    # Override output directory jika diberikan
    if args.output:
        config.config.setdefault("reporting", {})["output_dir"] = args.output

    console.print("[bold magenta]=== PurpleScan Starting ===[/bold magenta]\n")

    # Jalankan core scan
    core = PurpleScanCore()
    core.start_scan(args.target)


if __name__ == "__main__":
    main()