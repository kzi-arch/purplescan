#!/usr/bin/env python3
"""
CLI Interface - PurpleScan
"""

import argparse
import sys
from rich.console import Console

from .core import PurpleScanCore
from .config import config
from .utils.helpers import validate_target, print_banner

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="PurpleScan v0.5.0 - Nmap + Nikto + Nuclei + ffuf",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh Penggunaan:
  python run.py -t 192.168.1.100
  python run.py -t 192.168.1.100 --profile purple-stealth
  python run.py -t 192.168.56.0/24 --evasion
        """
    )

    parser.add_argument("-t", "--target", required=True,
                        help="Target IP, hostname, atau CIDR")
    parser.add_argument("-p", "--ports", help="Custom ports")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("--profile", choices=["default", "quick", "deep", "purple-stealth"],
                        default="default", help="Scan profile")
    parser.add_argument("--evasion", action="store_true", help="Aktifkan evasion mode")
    parser.add_argument("--os", action="store_true", help="Aktifkan OS detection (butuh sudo)")

    args = parser.parse_args()

    # Validasi
    if not validate_target(args.target):
        console.print("[bold red]Error: Target tidak valid![/bold red]")
        sys.exit(1)

    # Load profile
    try:
        config.load_config(args.profile)
    except Exception as e:
        console.print(f"[yellow]Warning: {e}. Menggunakan default.[/yellow]")
        config.load_config("default")

    # Override config
    if args.output:
        config.config.setdefault("reporting", {})["output_dir"] = args.output
    if args.evasion:
        config.config.setdefault("evasion", {})["enabled"] = True
    if args.ports:
        config.config.setdefault("scan", {})["default_ports"] = args.ports

    print_banner()
    console.print(f"[bold magenta]Target : {args.target} | Profile : {args.profile}[/bold magenta]\n")

    # Jalankan scan
    core = PurpleScanCore()
    core.start_scan(target=args.target, enable_os=args.os)


if __name__ == "__main__":
    main()