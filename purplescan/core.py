#!/usr/bin/env python3
"""
Core Logic PurpleScan
"""

from .scanner.chainer import ScanChainer
from rich.console import Console

console = Console()

class PurpleScanCore:
    def __init__(self):
        self.chainer = ScanChainer()

    def start_scan(self, target: str, enable_os: bool = False):
        try:
            self.chainer.run_full_scan(target=target, enable_os=enable_os)
        except KeyboardInterrupt:
            console.print("\n[bold red]Scan dibatalkan oleh user.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error tidak terduga: {e}[/bold red]")