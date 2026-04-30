#!/usr/bin/env python3
"""
Nuclei Scanner Module untuk PurpleScan
"""

import subprocess
import time
from pathlib import Path
from rich.console import Console
from typing import List

from ..config import config
from ..utils.evasion import get_random_user_agent

console = Console()

class NucleiScanner:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir / "nuclei"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def scan(self, urls: List[str]) -> bool:
        """Jalankan Nuclei scan pada list URL"""
        if not urls:
            console.print("[yellow]Tidak ada URL untuk discan dengan Nuclei.[/yellow]")
            return True

        console.print("[bold cyan]🚀 Menjalankan Nuclei Vulnerability Scan...[/bold cyan]")

        output_file = self.output_dir / f"nuclei_results_{int(time.time())}.json"
        targets_file = self.output_dir / "targets.txt"

        # Simpan list target ke file
        with open(targets_file, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")

        # Bangun command Nuclei
        cmd = [
            "nuclei",
            "-l", str(targets_file),
            "-json",
            "-o", str(output_file),
            "-rl", str(config.get("nuclei.rate_limit", 150)),
            "-timeout", str(config.get("nuclei.timeout", 600)),
            "-severity", config.get("nuclei.severity", "critical,high,medium"),
            "-silent"
        ]

        # Tambahkan random User-Agent jika evasion aktif
        if config.get("evasion.enabled", False):
            ua = get_random_user_agent()
            cmd.extend(["-H", f"User-Agent: {ua}"])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)

            if result.returncode in [0, 1]:  # 0 = no findings, 1 = findings found (normal)
                console.print(f"[green]✅ Nuclei scan selesai. Hasil: {output_file}[/green]")
                return True
            else:
                console.print(f"[yellow]Nuclei keluar dengan kode {result.returncode}[/yellow]")
                return False

        except FileNotFoundError:
            console.print("[bold red]❌ Nuclei tidak ditemukan!")
            console.print("   Install dengan: paru -S nuclei-bin  (atau yay -S nuclei-bin)")
            return False
        except subprocess.TimeoutExpired:
            console.print("[red]❌ Nuclei timeout (terlalu lama).[/red]")
            return False
        except Exception as e:
            console.print(f"[red]❌ Error saat menjalankan Nuclei: {e}[/red]")
            return False