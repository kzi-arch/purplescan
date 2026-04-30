#!/usr/bin/env python3
"""
ffuf Directory Brute-Force Scanner
"""

import subprocess
from pathlib import Path
from rich.console import Console
import time
from ..config import config
from ..utils.evasion import get_random_user_agent

console = Console()

class FfufScanner:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir / "ffuf"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def scan(self, url: str) -> bool:
        """Jalankan ffuf pada satu URL"""
        console.print(f"[bold magenta]🔍 Menjalankan Directory Brute-Force pada: {url}[/bold magenta]")

        output_file = self.output_dir / f"ffuf_{url.replace('://', '_').replace(':', '_').replace('/', '_')}.json"

        cmd = [
            "ffuf",
            "-u", f"{url}/FUZZ",
            "-w", config.get("ffuf.wordlist"),
            "-o", str(output_file),
            "-of", "json",
            "-t", str(config.get("ffuf.threads", 50)),
            "-timeout", str(config.get("ffuf.timeout", 600)),
            "-mc", "200,204,301,302,307,401,403",   # status code yang dianggap interesting
            "-silent"
        ]

        # Tambahkan ekstensi
        extensions = config.get("ffuf.extensions")
        if extensions:
            cmd.extend(["-e", extensions])

        # Follow redirect jika diaktifkan
        if config.get("ffuf.follow_redirect", True):
            cmd.append("-r")

        # Random User-Agent jika evasion aktif
        if config.get("evasion.enabled", False):
            ua = get_random_user_agent()
            cmd.extend(["-H", f"User-Agent: {ua}"])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=config.get("ffuf.max_time_per_target", 300))

            if result.returncode in [0, 1]:
                console.print(f"[green]✓ ffuf selesai untuk {url}[/green]")
                return True
            else:
                console.print(f"[yellow]ffuf keluar dengan kode {result.returncode}[/yellow]")
                return False

        except subprocess.TimeoutExpired:
            console.print(f"[red]ffuf timeout pada {url}[/red]")
            return False
        except FileNotFoundError:
            console.print("[bold red]❌ ffuf tidak terinstall!")
            console.print("   Install dengan: paru -S ffuf")
            return False
        except Exception as e:
            console.print(f"[red]Error ffuf: {e}[/red]")
            return False