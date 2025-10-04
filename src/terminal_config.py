
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configurações do terminal 3270.
Created on: October 3, 2025
Author: Marcos WS
Version: 1.0.0
"""

from dataclasses import dataclass

@dataclass
class TerminalConfig:
    """Configurações do terminal 3270"""
    SCREEN_COLS: int = 80
    SCREEN_ROWS: int = 24
    DEFAULT_TIMEOUT: int = 30
    CHAR_DELAY: float = 0.05
    DEBUG: bool = False