#!/usr/bin/env python3
"""
Module untuk logic scanning dengan Nikto
"""

import subprocess
from pathlib import Path
from rich.console import Console
from typing import Dict
import asyncio
import time
from .nuclei_scanner import NucleiScanner

console = Console()

class NiktoScanner:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir / "nikto"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def scan_async(self, url: str, timeout: int = 600) -> bool:
        """Jalankan Nikto secara async dengan evasion support"""
        from ..config import config
        from ..utils.evasion import get_random_user_agent

        console.print(f"[bold green]→ Menjalankan Nikto pada: {url}[/bold green]")
        
        output_file = self.output_dir / f"nikto_{url.replace('://', '_').replace(':', '_').replace('/', '_')}.txt"
        
        cmd = ['nikto', '-h', url, '-output', str(output_file), '-Tuning', 'x']
        
        # Tambahkan random user-agent jika evasion aktif
        if config.get("evasion.enabled", False) and config.get("evasion.randomize_user_agent", True):
            ua = get_random_user_agent()
            cmd.extend(['-useragent', ua])
            console.print(f"   [dim]User-Agent: {ua[:60]}...[/dim]")

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                await asyncio.wait_for(process.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                console.print(f"[red]Nikto timeout pada {url}[/red]")
                process.kill()
                return False
            
            if process.returncode in [0, 1]:
                console.print(f"[green]✓ Nikto selesai: {url}[/green]")
                return True
            else:
                console.print(f"[yellow]Nikto keluar dengan kode {process.returncode}[/yellow]")
                return False

            # Tahap 4: Nuclei Scan (jika diaktifkan)
            if config.get("nuclei.enabled", True):
                web_urls = [web['url'] for web in web_targets]
                self.nuclei_scanner.scan(web_urls)

            elapsed = time.time() - start_time
            console.print(f"[bold cyan]Membuat laporan hasil scan...[/bold cyan]")
            self.reporter.generate_summary(target, web_targets, elapsed)

            console.print(f"\n[bold green]✅ Scan lengkap selesai dalam {elapsed:.2f} detik.[/bold green]")
            console.print(f"[bold]Hasil ada di:[/bold] reports/ dan output/")
                
        except Exception as e:
            console.print(f"[red]Error Nikto pada {url}: {e}[/red]")
            return False

    # Method lama untuk backward compatibility
    def scan(self, url: str, timeout: int = 600) -> bool:
        """Method synchronous (untuk mode sequential)"""
        try:
            return asyncio.run(self.scan_async(url, timeout))
        except RuntimeError:
            # Jika sudah di dalam event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.scan_async(url, timeout))
            loop.close()
            return result