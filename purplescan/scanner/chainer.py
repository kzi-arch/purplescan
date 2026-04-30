#!/usr/bin/env python3
"""
Chainer - Core logic dengan Parallel Nikto Scanning
"""

from pathlib import Path
from rich.console import Console
from rich.progress import Progress
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

from .nmap_scanner import NmapScanner, extract_web_services
from .nikto_scanner import NiktoScanner
from ..utils.helpers import create_output_dirs, print_banner
from ..reporter.report_generator import ReportGenerator
from ..config import config
from .nuclei_scanner import NucleiScanner
from .ffuf_scanner import FfufScanner

console = Console()

class ScanChainer:
    def __init__(self):
        self.output_dir = create_output_dirs(config.get("reporting.output_dir", "output"))
        self.nmap_scanner = NmapScanner()
        self.nikto_scanner = NiktoScanner(self.output_dir)
        self.reporter = ReportGenerator(self.output_dir)
        self.nuclei_scanner = NucleiScanner(self.output_dir)
        self.ffuf_scanner = FfufScanner(self.output_dir)
        self.max_workers = 5   # Maksimal parallel Nikto (bisa di-config nanti)

    def run_full_scan(self, target: str, enable_os: bool = False) -> None:
        """Jalankan scan lengkap dengan parallel Nikto"""
        print_banner()
        console.print(f"[bold magenta]Target  :[/bold magenta] {target}")
        console.print(f"[bold magenta]Output  :[/bold magenta] {self.output_dir}\n")
        console.print(f"[blue]Mode Parallel Nikto diaktifkan (max {self.max_workers} workers)[/blue]\n")

        start_time = time.time()

        try:
            # Tahap 1: Nmap Scan
            with Progress() as progress:
                task = progress.add_task("[cyan]Menjalankan Nmap scan...", total=None)
                nm_result = self.nmap_scanner.scan(
                    target=target,
                    ports=config.get("scan.default_ports"),
                    timing=config.get("scan.nmap_timing"),
                    enable_os=enable_os
                )
                progress.update(task, completed=100)

            # Tahap 2: Ekstrak web services
            web_targets = extract_web_services(nm_result)
            console.print(f"\n[bold green]Ditemukan {len(web_targets)} web service[/bold green]")

            if not web_targets:
                console.print("[yellow]Tidak ditemukan service web.[/yellow]")
                self.reporter.generate_summary(target, [], time.time() - start_time)
                return

            # Tahap 3: Parallel Nikto Scan
            console.print("[bold cyan]Memulai Parallel Nikto Scan...[/bold cyan]")
            asyncio.run(self._run_parallel_nikto(web_targets))

            elapsed = time.time() - start_time
            
            # Generate Professional Report
            console.print("[bold cyan]Membuat laporan hasil scan...[/bold cyan]")
            self.reporter.generate_summary(target, web_targets, elapsed)

            console.print(f"\n[bold green]✅ Scan selesai dalam {elapsed:.2f} detik.[/bold green]")
            console.print(f"[bold]Semua hasil & report ada di folder:[/bold] reports/")

                        # Tahap 5: ffuf Directory Brute-Force (jika diaktifkan)
        # Tahap 5: ffuf Directory Brute-Force (jika diaktifkan)
            if config.get("ffuf.enabled", True) and web_targets:
                console.print("[bold magenta]Memulai Directory Brute-Force dengan ffuf...[/bold magenta]")
                for web in web_targets:
                    self.ffuf_scanner.scan(web['url'])
                    # Delay kecil antar target jika stealth mode
                    if config.get("evasion.enabled", False):
                        time.sleep(2)

        except Exception as e:
            console.print(f"[bold red]❌ Error selama scanning: {e}[/bold red]")
            raise

    async def _run_parallel_nikto(self, web_targets: list):
        """Jalankan Nikto secara parallel dengan evasion support"""
        from ..utils.evasion import random_delay, print_stealth_info
        from ..config import config

        if config.get("evasion.enabled", False):
            print_stealth_info()

        tasks = []
        for web in web_targets:
            task = self.nikto_scanner.scan_async(
                web['url'], 
                timeout=config.get("scan.nikto_timeout", 600)
            )
            tasks.append(task)

        # Jalankan parallel
        await asyncio.gather(*tasks, return_exceptions=True)

        # Tambahkan random delay setelah batch jika stealth mode
        if config.get("evasion.enabled", False):
            delay = random_delay(2.0, 5.0)
            console.print(f"[dim]Random delay setelah batch: {delay:.2f} detik[/dim]")