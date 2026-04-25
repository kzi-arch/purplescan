#!/usr/bin/env python3
"""
Module untuk logic scanning dengan Nikto
"""

import subprocess
from pathlib import Path
from rich.console import Console
from typing import Dict

console = Console()

class NiktoScanner:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir / "nikto"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def scan(self, url: str, timeout: int = 600) -> bool:
        """Jalankan Nikto pada satu URL"""
        console.print(f"[bold green]Menjalankan Nikto pada: {url}[/bold green]")
        
        output_file = self.output_dir / f"nikto_{url.replace('://', '_').replace(':', '_').replace('/', '_')}.txt"
        
        try:
            cmd = [
                'nikto',
                '-h', url,
                '-output', str(output_file),
                '-Tuning', 'x',           # Hanya check penting
                '-maxtime', '10m'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode in [0, 1]:
                console.print(f"[green]✓ Nikto selesai untuk {url}[/green]")
                return True
            else:
                console.print(f"[yellow]Nikto keluar dengan kode {result.returncode} untuk {url}[/yellow]")
                return False
                
        except subprocess.TimeoutExpired:
            console.print(f"[red]Nikto timeout pada {url}[/red]")
            return False
        except FileNotFoundError:
            console.print("[bold red]Error: Nikto tidak terinstall. Jalankan: sudo apt install nikto[/bold red]")
            return False
        except Exception as e:
            console.print(f"[red]Error Nikto: {e}[/red]")
            return False