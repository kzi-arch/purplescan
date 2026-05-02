#!/usr/bin/env python3
"""
Nuclei Scanner Module - Versi Stabil & Force Output
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
        self.base_output = Path(output_dir).resolve()
        self.output_dir = self.base_output / "nuclei"
        self.output_dir.mkdir(parents=True, exist_ok=True, mode=0o755)

    def scan(self, urls: List[str]) -> bool:
        """Jalankan Nuclei dengan force save output"""
        if not urls:
            console.print("[yellow]Tidak ada URL untuk discan dengan Nuclei.[/yellow]")
            return True

        console.print("[bold cyan]🚀 Menjalankan Nuclei Vulnerability Scan...[/bold cyan]")
        
        timestamp = int(time.time())
        output_file = self.output_dir / f"nuclei_results_{timestamp}.json"
        targets_file = self.output_dir / f"targets_{timestamp}.txt"

        # Simpan list target
        with open(targets_file, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")

        cmd = [
            "nuclei",
            "-l", str(targets_file),
            "-json",
            "-o", str(output_file),
            "-rl", str(config.get("nuclei.rate_limit", 150)),
            "-timeout", str(config.get("nuclei.timeout", 600)),
            "-severity", config.get("nuclei.severity", "critical,high,medium"),
            "-stats",
            "-silent"
        ]

        if config.get("evasion.enabled", False):
            ua = get_random_user_agent()
            cmd.extend(["-H", f"User-Agent: {ua}"])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)

            # Force save jika file tidak ada atau kosong
            if not output_file.exists() or output_file.stat().st_size == 0:
                content = result.stdout or result.stderr or f"Nuclei scan completed for {len(urls)} targets at {time.ctime()}\nNo findings or empty output.\n"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[yellow]Nuclei force saved (mungkin tidak ada findings) → {output_file.name}[/yellow]")
            else:
                console.print(f"[green]✅ Nuclei selesai! Hasil disimpan di: {output_file.name}[/green]")

                # Tampilkan jumlah findings
                try:
                    with open(output_file, 'r') as f:
                        lines = f.readlines()
                    console.print(f"[green]   → Ditemukan {len(lines)} vulnerability findings[/green]")
                except:
                    pass

            return True

        except FileNotFoundError:
            console.print("[bold red]❌ Nuclei tidak terdeteksi!")
            console.print("   Install dengan: paru -S nuclei-bin")
            return False
        except subprocess.TimeoutExpired:
            console.print("[red]❌ Nuclei timeout.[/red]")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("Nuclei scan timeout.\n")
            return False
        except Exception as e:
            console.print(f"[red]❌ Error Nuclei: {e}[/red]")
            return False