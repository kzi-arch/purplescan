#!/usr/bin/env python3
"""
Evasion & Stealth utilities untuk Purple Team
"""

import random
import time
from typing import List

# Daftar User-Agent umum (bisa ditambah)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1"
]

def get_random_user_agent() -> str:
    """Return random user agent"""
    return random.choice(USER_AGENTS)

def random_delay(min_seconds: float = 1.0, max_seconds: float = 4.0):
    """Delay acak antara min dan max detik"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay

def print_stealth_info():
    """Tampilkan informasi stealth mode"""
    print("\n[bold yellow]🛡️  STEALTH MODE AKTIF[/bold yellow]")
    print("   • Random User-Agent digunakan")
    print("   • Random delay diterapkan antar request")
    print("   • Timing Nmap diatur pelan")
    print("   • Direkomendasikan untuk evasion testing\n")