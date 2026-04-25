#!/usr/bin/env python3
"""
Config Manager - Mendukung multiple profile
"""

import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.current_profile = "default"
        self.load_config("default")

    def load_config(self, profile_name: str = "default"):
        """Load konfigurasi berdasarkan profile"""
        self.current_profile = profile_name
        
        if profile_name == "default":
            config_path = Path("config/default.yaml")
        else:
            config_path = Path(f"config/{profile_name}.yaml")

        if not config_path.exists():
            raise FileNotFoundError(f"Config profile '{profile_name}' tidak ditemukan!")

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f) or {}

        print(f"[blue]Loaded profile:[/blue] {profile_name}")

    def get(self, key: str, default: Any = None) -> Any:
        """Ambil nilai config dengan dot notation (scan.default_ports)"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value if value is not None else default

    def get_scan_config(self) -> Dict:
        return self.get("scan", {})

    def get_evasion_config(self) -> Dict:
        return self.get("evasion", {})


# Global config instance
config = Config()