#!/usr/bin/env python3
"""
Module untuk logic scanning dengan Nikto
"""

import subprocess
import asyncio
import time
from pathlib import Path
from rich.console import Console

from ..config import config
from ..utils.evasion import get_random_user_agent

console = Console()

class NiktoScanner:
    def __init__(self, output_dir: Path):
        self.base_output = Path(output_dir).resolve()
        self.output_dir = self.base_output / "nikto"
        self.output_dir.mkdir(parents=True, exist_ok=True, mode=0o755)

    async def scan_async(self, url: str, timeout: int = 600) -> bool:
        """Jalankan Nikto dengan force save output"""
        console.print(f"[bold green]→ Nikto: {url}[/bold green]")
        
        timestamp = int(time.time())
        safe_name = url.replace('://', '_').replace(':', '_').replace('/', '_').replace('.', '_')
        output_file = self.output_dir / f"nikto_{timestamp}_{safe_name}.txt"
        
        cmd = [
            'nikto',
            '-h', url,
            '-output', str(output_file),
            '-Tuning', 'x',
            '-Format', 'txt'
        ]

        # Tambahkan User-Agent jika evasion aktif
        if config.get("evasion.enabled", False):
            ua = get_random_user_agent()
            cmd.extend(['-useragent', ua])

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            
            # Force save output
            if not output_file.exists() or output_file.stat().st_size == 0:
                content = stdout.decode('utf-8', errors='ignore') if stdout else ""
                if not content and stderr:
                    content = stderr.decode('utf-8', errors='ignore')
                if not content:
                    content = f"Nikto scan completed for {url} at {time.ctime()}\nNo detailed output.\n"
                
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(content)
            
            size = output_file.stat().st_size if output_file.exists() else 0
            console.print(f"[green]✓ Nikto selesai → {output_file.name} ({size} bytes)[/green]")
            return True

        except asyncio.TimeoutError:
            console.print(f"[red]Nikto timeout pada {url}[/red]")
            # Force save timeout message
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"Nikto timeout after {timeout} seconds for {url}\n")
            return False
        except FileNotFoundError:
            console.print("[bold red]Nikto tidak terinstall. Jalankan: sudo pacman -S nikto[/bold red]")
            return False
        except Exception as e:
            console.print(f"[red]Nikto error pada {url}: {e}[/red]")
            return False

    # Method lama untuk backward compatibility
    def scan(self, url: str, timeout: int = 600) -> bool:
        try:
            return asyncio.run(self.scan_async(url, timeout))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.scan_async(url, timeout))
            loop.close()
            return result