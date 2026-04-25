#!/usr/bin/env python3
"""
Module untuk logic scanning dengan Nmap
"""

import nmap
from rich.console import Console
from typing import Dict, List

console = Console()

class NmapScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()

    def scan(self, target: str, ports: str = None, timing: str = "T3", enable_os: bool = False):
        """Jalankan Nmap scan"""
        console.print(f"[bold blue]Menjalankan Nmap scan pada target: {target}[/bold blue]")
        
        if ports is None:
            ports = "80,443,8080,8443,8000-9000"
        
        arguments = f"-sV --script=http-title -p {ports} -{timing}"
        
        if enable_os:
            arguments += " -O"
            console.print("[yellow]OS detection (-O) diaktifkan → Membutuhkan hak root[/yellow]")
        
        try:
            self.nm.scan(hosts=target, arguments=arguments)
            console.print("[green]Nmap scan selesai.[/green]")
            return self.nm
        except nmap.PortScannerError as e:
            error_msg = str(e)
            if "requires root privileges" in error_msg.lower():
                console.print("[bold red]Error: OS detection memerlukan hak root.[/bold red]")
                console.print("[yellow]Jalankan dengan 'sudo' atau hilangkan flag --os[/yellow]")
            else:
                console.print(f"[bold red]Nmap Error: {error_msg}[/bold red]")
            raise
        except Exception as e:
            console.print(f"[bold red]Error saat menjalankan Nmap: {e}[/bold red]")
            raise


def extract_web_services(nm_result) -> List[Dict]:
    """Ekstrak hanya service web (HTTP/HTTPS) dari hasil Nmap"""
    web_targets = []
    
    for host in nm_result.all_hosts():
        if nm_result[host].state() != 'up':
            continue
            
        for proto in nm_result[host].all_protocols():
            if proto != 'tcp':
                continue
                
            for port in nm_result[host][proto]:
                port_data = nm_result[host][proto][port]
                if port_data.get('state') != 'open':
                    continue
                    
                service = port_data.get('name', '').lower()
                port_num = int(port)
                
                # Deteksi web service
                if (service in ['http', 'https', 'http-alt', 'https-alt'] or 
                    port_num in [80, 443, 8080, 8443, 8000, 8081, 8888]):
                    
                    scheme = 'https' if (port_num in [443, 8443] or 'https' in service) else 'http'
                    url = f"{scheme}://{host}:{port_num}"
                    
                    web_targets.append({
                        'host': host,
                        'port': port_num,
                        'url': url,
                        'service': service,
                        'version': f"{port_data.get('product', '')} {port_data.get('version', '')}".strip()
                    })
    
    return web_targets