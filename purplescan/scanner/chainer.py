#!/usr/bin/env python3
"""
Chainer - Menggabungkan Nmap + Nikto (Core Logic)
"""

from pathlib import Path
from rich.console import Console
from rich.progress import Progress
import time

from .nmap_scanner import NmapScanner, extract_web_services
from .nikto_scanner import NiktoScanner
from ..utils.helpers import create_output_dirs, print_banner
from ..config import config

console = Console()

class ScanChainer:
    def __init__(self):
        self.output_dir = create_output_dirs(config.get("reporting.output_dir", "output"))
        self.nmap_scanner = NmapScanner()
        self.nikto_scanner = NiktoScanner(self.output_dir)

    def run_full_scan(self, target: str) -> None:
        """Jalankan scan lengkap: Nmap → Extract Web → Nikto"""
        print_banner()
        console.print(f"[bold magenta]Target Scan :[/bold magenta] {target}")
        console.print(f"[bold magenta]Output Dir  :[/bold magenta] {self.output_dir}\n")

        start_time = time.time()

        try:
            # Tahap 1: Nmap Scan
            with Progress() as progress:
                task = progress.add_task("[cyan]Menjalankan Nmap scan...", total=None)
                nm_result = self.nmap_scanner.scan(
                    target=target,
                    ports=config.get("scan.default_ports"),
                    timing=config.get("scan.nmap_timing"),
                    enable_os=False
                )
                progress.update(task, completed=100)

            # Tahap 2: Ekstrak web services
            web_targets = extract_web_services(nm_result)
            
            console.print(f"\n[bold green]Ditemukan {len(web_targets)} web service[/bold green]")

            if not web_targets:
                console.print("[yellow]Tidak ditemukan service web. Scan selesai.[/yellow]")
                return

            # Tahap 3: Nikto Scan
            with Progress() as progress:
                task = progress.add_task("[green]Menjalankan Nikto scan...", total=len(web_targets))
                
                for i, web in enumerate(web_targets):
                    self.nikto_scanner.scan(
                        url=web['url'],
                        timeout=config.get("scan.nikto_timeout", 600)
                    )
                    progress.update(task, advance=1)
                    
                    # Delay kecil jika evasion aktif
                    if config.get("evasion.enabled", False):
                        time.sleep(config.get("evasion.delay_between_targets", 1.5))

            elapsed = time.time() - start_time
            console.print(f"\n[bold green]✅ Scan selesai dalam {elapsed:.2f} detik.[/bold green]")
            console.print(f"[bold]Hasil tersimpan di:[/bold] {self.output_dir}")

        except Exception as e:
            console.print(f"[bold red]❌ Error selama scanning: {e}[/bold red]")
            raise