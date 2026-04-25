#!/usr/bin/env python3
"""
Report Generator - TXT + JSON + HTML Professional Report
"""

from pathlib import Path
from rich.console import Console
from datetime import datetime
import json
from jinja2 import Environment, FileSystemLoader

console = Console()

class ReportGenerator:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.report_dir = Path("reports")
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja2 template
        template_dir = Path("purplescan/reporter/templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_summary(self, target: str, web_targets: list, scan_time: float):
        """Generate TXT, JSON, dan HTML Report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"purplescan_report_{target.replace('.', '_').replace('/', '_')}_{timestamp}"
        
        txt_file = self.report_dir / f"{base_name}.txt"
        json_file = self.report_dir / f"{base_name}.json"
        html_file = self.report_dir / f"{base_name}.html"

        report_data = {
            "tool": "PurpleScan",
            "version": "0.2.0",
            "target": target,
            "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scan_duration": round(scan_time, 2),
            "total_web_services": len(web_targets),
            "web_services": web_targets
        }

        try:
            # 1. TXT Report
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write("PURPLESCAN REPORT\n")
                f.write("=" * 60 + "\n")
                f.write(f"Target              : {target}\n")
                f.write(f"Scan Date           : {report_data['scan_date']}\n")
                f.write(f"Duration            : {scan_time:.2f} detik\n")
                f.write(f"Total Web Services  : {len(web_targets)}\n")
                f.write("=" * 60 + "\n\n")
                
                if web_targets:
                    for i, web in enumerate(web_targets, 1):
                        f.write(f"{i:2d}. {web['url']} | {web['service']} | {web['version'] or 'Unknown'}\n")
                else:
                    f.write("Tidak ditemukan service web.\n")
                
                f.write("\nDetail Nikto: output/nikto/\n")

            # 2. JSON Report
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)

            # 3. HTML Report (yang paling keren)
            template = self.env.get_template("report.html")
            html_content = template.render(**report_data)
            
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            console.print(f"[bold green]✅ Report berhasil dibuat:[/bold green]")
            console.print(f"   • TXT  → {txt_file.name}")
            console.print(f"   • JSON → {json_file.name}")
            console.print(f"   • HTML → {html_file.name}  ← (Paling direkomendasikan)")

        except Exception as e:
            console.print(f"[yellow]Warning: Gagal membuat salah satu report: {e}[/yellow]")