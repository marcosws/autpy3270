
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Definições de enums para teclas especiais usadas na interação com o emulador 3270.
Inclui teclas de função (PF1-PF24) e teclas de ação (PA1-PA3).
Created on: October 3, 2025
Author: Marcos WS
Version: 1.0.0
"""

from enum import Enum


class Key(Enum):
    ENTER = 'enter'
    TAB = 'tab'
    CLEAR = 'clear'
    RESET = 'reset'
    BACKSPACE = 'backspace'
    DELETE = 'delete'
    NEWLINE = 'newline'
    # PF Keys
    PF1 = 'pf1'
    PF2 = 'pf2'
    PF3 = 'pf3'
    PF4 = 'pf4'
    PF5 = 'pf5'
    PF6 = 'pf6'
    PF7 = 'pf7'
    PF8 = 'pf8'
    PF9 = 'pf9'
    PF10 = 'pf10'
    PF11 = 'pf11'
    PF12 = 'pf12'
    PF13 = 'pf13'
    PF14 = 'pf14'
    PF15 = 'pf15'
    PF16 = 'pf16'
    PF17 = 'pf17'
    PF18 = 'pf18'
    PF19 = 'pf19'
    PF20 = 'pf20'
    PF21 = 'pf21'
    PF22 = 'pf22'
    PF23 = 'pf23'
    PF24 = 'pf24'
    # PA Keys
    PA1 = 'pa1'
    PA2 = 'pa2'
    PA3 = 'pa3'