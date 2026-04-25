#!/usr/bin/env python3
"""
Report Generator - Membuat laporan hasil scan
"""

from pathlib import Path
from rich.console import Console
import json
import os

console = Console()

class ReportGenerator:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.report_dir = self.output_dir.parent / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate_summary(self, target: str):
        """Buat summary sederhana hasil scan"""
        summary_file = self.report_dir / f"summary_{target.replace('.', '_')}.txt"
        
        try:
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(f"PurpleScan Report - {target}\n")
                f.write("=" * 50 + "\n")
                f.write(f"Scan Time : {os.popen('date').read()}")
                f.write(f"Output Dir: {self.output_dir}\n\n")
                f.write("Scan selesai menggunakan Nmap + Nikto.\n")
                f.write("Detail hasil ada di folder output/ dan reports/\n")
            
            console.print(f"[green]Summary report dibuat: {summary_file}[/green]")
        except Exception as e:
            console.print(f"[yellow]Gagal membuat summary report: {e}[/yellow]")