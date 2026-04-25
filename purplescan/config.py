#!/usr/bin/env python3
"""
Module untuk load dan manage konfigurasi YAML
"""

import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    def __init__(self, config_path: str = None):
        self.config: Dict[str, Any] = {}
        self.load_config(config_path)

    def load_config(self, config_path: str = None):
        """Load konfigurasi dari file YAML"""
        if config_path is None:
            config_path = Path("config/default.yaml")
        else:
            config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Config file tidak ditemukan: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Ambil nilai dari config dengan dot notation (contoh: scan.default_ports)"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value if value is not None else default

    def get_scan_config(self) -> Dict:
        """Ambil seluruh konfigurasi scan"""
        return self.get("scan", {})

    def get_reporting_config(self) -> Dict:
        """Ambil konfigurasi reporting"""
        return self.get("reporting", {})


# Instance global config
config = Config()