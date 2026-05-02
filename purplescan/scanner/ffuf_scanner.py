#!/usr/bin/env python3
"""
ffuf Directory Brute-Force Scanner - Versi Stabil dengan Force Save
"""

import subprocess
import time
from pathlib import Path
from rich.console import Console

from ..config import config
from ..utils.evasion import get_random_user_agent

console = Console()

class FfufScanner:
    def __init__(self, output_dir: Path):
        self.base_output = Path(output_dir).resolve()
        self.output_dir = self.base_output / "ffuf"
        self.output_dir.mkdir(parents=True, exist_ok=True, mode=0o755)

    def scan(self, url: str) -> bool:
        """Jalankan ffuf dengan multiple wordlist + force save"""
        console.print(f"[bold magenta]🔍 Brute-force directory pada: {url}[/bold magenta]")

        timestamp = int(time.time())
        safe_name = url.replace('://', '_').replace(':', '_').replace('/', '_').replace('.', '_')
        
        wordlists = config.get("ffuf.wordlists", ["/usr/share/wordlists/dirb/common.txt"])

        for i, wordlist in enumerate(wordlists):
            output_file = self.output_dir / f"ffuf_{timestamp}_wl{i+1}_{safe_name}.json"

            cmd = [
                "ffuf",
                "-u", f"{url}/FUZZ",
                "-w", wordlist,
                "-o", str(output_file),
                "-of", "json",
                "-t", str(config.get("ffuf.threads", 50)),
                "-timeout", str(config.get("ffuf.timeout", 600)),
                "-mc", "200,204,301,302,307,401,403",
                "-silent"
            ]

            if config.get("ffuf.extensions"):
                cmd.extend(["-e", config.get("ffuf.extensions")])

            if config.get("ffuf.follow_redirect", True):
                cmd.append("-r")

            if config.get("evasion.enabled", False):
                ua = get_random_user_agent()
                cmd.extend(["-H", f"User-Agent: {ua}"])

            try:
                console.print(f"[dim]   Wordlist {i+1}: {wordlist}[/dim]")
                
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=config.get("ffuf.max_time_per_target", 240)
                )

                # Force save jika file tidak ada atau kosong
                if not output_file.exists() or output_file.stat().st_size == 0:
                    content = result.stdout or result.stderr or f"ffuf scan completed for {url} with wordlist {wordlist}\nNo findings detected.\n"
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(str(content))
                    console.print(f"[yellow]ffuf force saved (no findings or empty) → {output_file.name}[/yellow]")
                else:
                    console.print(f"[green]✓ ffuf selesai (wordlist {i+1}) → {output_file.name}[/green]")

            except subprocess.TimeoutExpired:
                console.print(f"[red]ffuf timeout pada wordlist {i+1}[/red]")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"ffuf timeout for {url} using wordlist {wordlist}\n")
            except FileNotFoundError:
                console.print("[bold red]❌ ffuf tidak terinstall. Jalankan: paru -S ffuf[/bold red]")
                return False
            except Exception as e:
                console.print(f"[red]Error ffuf wordlist {i+1}: {e}[/red]")

        return True