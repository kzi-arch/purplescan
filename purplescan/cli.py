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
        description="PurpleScan v0.2 - Nmap + Nikto untuk Purple Team",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Contoh:\n  python run.py -t 192.168.1.100\n  python run.py -t 192.168.56.0/24 --evasion"
    )
    
    parser.add_argument("-t", "--target", 
                        required=True,
                        help="Target: IP, hostname, atau CIDR")
    
    parser.add_argument("-p", "--ports",
                        help="Port khusus (contoh: 80,443,8080)")
    
    parser.add_argument("-o", "--output",
                        help="Folder output")
    
    parser.add_argument("--profile",
                        choices=["default", "quick", "deep", "purple-stealth"],
                        default="default",
                        help="Pilih profile konfigurasi (default, quick, deep, purple-stealth)")
    
    parser.add_argument("--evasion", 
                        action="store_true",
                        help="Aktifkan mode evasion (delay antar scan)")
    
    parser.add_argument("--os", 
                        action="store_true",
                        help="Aktifkan OS detection (-O) - butuh sudo")
    
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Mode verbose")

    args = parser.parse_args()

    # Validasi target
    if not validate_target(args.target):
        console.print("[bold red]Error: Target tidak valid![/bold red]")
        sys.exit(1)

    # Load profile jika bukan default
    if args.profile != "default":
    # Load profile
            try:
                config.load_config(args.profile)
            except Exception as e:
                console.print(f"[yellow]Warning: Gagal load profile {args.profile}. Menggunakan default.[/yellow]")
                config.load_config("default")

    # Override konfigurasi dari argument
    if args.output:
        config.config.setdefault("reporting", {})["output_dir"] = args.output

    if args.evasion:
        config.config.setdefault("evasion", {})["enabled"] = True

    if args.ports:
        config.config.setdefault("scan", {})["default_ports"] = args.ports

    console.print("[bold magenta]=== PurpleScan v0.2 Starting ===[/bold magenta]\n")

    # Jalankan scan
    core = PurpleScanCore()
    core.start_scan(target=args.target, enable_os=args.os)


if __name__ == "__main__":
    main()