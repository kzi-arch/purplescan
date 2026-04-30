#!/usr/bin/env python3
"""
Nuclei Scanner Module - Versi Debug & Improved
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
        """Jalankan Nuclei dengan output yang lebih jelas"""
        if not urls:
            console.print("[yellow]Tidak ada URL untuk discan dengan Nuclei.[/yellow]")
            return True

        console.print("[bold cyan]🚀 Menjalankan Nuclei Vulnerability Scan...[/bold cyan]")
        timestamp = int(time.time())
        output_file = self.output_dir / f"nuclei_results_{timestamp}.json"
        targets_file = self.output_dir / f"targets_{timestamp}.txt"

        # Simpan target ke file
        with open(targets_file, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")

        cmd = [
            "nuclei",
            "-l", str(targets_file),
            "-json",                      # Output JSON
            "-o", str(output_file),       # Simpan hasil
            "-rl", str(config.get("nuclei.rate_limit", 150)),
            "-timeout", str(config.get("nuclei.timeout", 600)),
            "-severity", config.get("nuclei.severity", "critical,high,medium"),
            "-stats",                     # Tampilkan statistik
            "-silent"                     # Kurangi noise
        ]

        # Tambahkan User-Agent jika evasion aktif
        if config.get("evasion.enabled", False):
            ua = get_random_user_agent()
            cmd.extend(["-H", f"User-Agent: {ua}"])

        console.print(f"[dim]Menjalankan: {' '.join(cmd[:6])} ...[/dim]")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)

            # Cek apakah file hasil dibuat
            if output_file.exists() and output_file.stat().st_size > 0:
                console.print(f"[green]✅ Nuclei selesai! Hasil disimpan di:[/green]")
                console.print(f"   → {output_file}")
                
                # Tampilkan jumlah findings
                try:
                    with open(output_file, 'r') as f:
                        lines = f.readlines()
                    console.print(f"[green]   → Ditemukan {len(lines)} vulnerability findings[/green]")
                except:
                    pass
                return True

            elif output_file.exists():
                console.print("[yellow]Nuclei selesai, tapi tidak menemukan vulnerability (hasil kosong).[/yellow]")
                return True
            else:
                console.print("[yellow]Nuclei selesai tanpa menghasilkan file output.[/yellow]")
                if result.stderr:
                    console.print(f"[dim]Error log: {result.stderr.strip()[:200]}[/dim]")
                return False

        except FileNotFoundError:
            console.print("[bold red]❌ Nuclei tidak terdeteksi!")
            console.print("   Pastikan sudah install dengan: `paru -S nuclei-bin`")
            return False
        except subprocess.TimeoutExpired:
            console.print("[red]❌ Nuclei timeout (terlalu lama).[/red]")
            return False
        except Exception as e:
            console.print(f"[red]❌ Error Nuclei: {e}[/red]")
            return False