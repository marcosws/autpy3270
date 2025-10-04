
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo base para automação de teste em terminal 3270 usando py3270.
Implementa o padrão Page Object Model para organizar os elementos e ações do terminal.

Este módulo fornece:
    - Classe base para Pages Objects (BasePage)
    - Utilitários para manipulação do terminal (Utils)
    - Tratamento de exceções específicas
    - Logging de operações
    - Integração com pytest

Exemplo:
    from base_page import BasePage
    
    class LoginPage(BasePage):
        def login(self, username, password):
            self.input_text("Username:", username)
            self.input_text("Password:", password)
            self.input_key(Key.ENTER)

Created on: October 3, 2025
Author: Marcos WS
Version: 1.0.0
"""

from time import time
from py3270 import Emulator
from base_page import Utils
from enums import Key
from terminal_config import TerminalConfig
import logging
import pytest
import time
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class TerminalError(Exception):
    """Exceção base para erros de terminal"""
    def __init__(self, message: str, screen_content: Optional[str] = None):
        self.screen_content = screen_content
        error_msg = message
        if screen_content:
            error_msg = f"{message}\nConteúdo da tela:\n{screen_content}"
        super().__init__(error_msg)
        logger.error(error_msg)
        pytest.fail(error_msg)

class FieldNotFoundError(TerminalError):
    """Exceção lançada quando um campo não é encontrado na tela"""
    def __init__(self, field: str, emulator: Optional[Emulator] = None):
        screen_content = None
        if emulator:
            screen_content = '\n'.join(Utils.get_screen(emulator))
        super().__init__(
            f'Campo "{field}" não encontrado na tela',
            screen_content
        )

class InputError(TerminalError):
    """Exceção lançada quando há erro ao inserir dados"""
    def __init__(self, field: str, value: str, error: str, emulator: Optional[Emulator] = None):
        screen_content = None
        if emulator:
            screen_content = '\n'.join(Utils.get_screen(emulator))
        super().__init__(
            f'Erro ao inserir "{value}" no campo "{field}": {error}',
            screen_content
        )

class KeyError(TerminalError):
    """Exceção lançada quando há erro ao enviar teclas"""
    def __init__(self, key: Key, error: str, emulator: Optional[Emulator] = None):
        screen_content = None
        if emulator:
            screen_content = '\n'.join(Utils.get_screen(emulator))
        super().__init__(
            f'Erro ao enviar tecla {key.name}: {error}',
            screen_content
        )

class ScreenError(TerminalError):
    """Exceção lançada quando há erro ao capturar/manipular a tela"""
    def __init__(self, error: str, operation: str, emulator: Optional[Emulator] = None):
        screen_content = None
        if emulator:
            try:
                screen_lines = Utils.get_screen(emulator)
                if screen_lines:
                    screen_content = '\n'.join(screen_lines)
            except Exception as e:
                screen_content = f"Não foi possível capturar o conteúdo da tela: {str(e)}"
        super().__init__(
            f'Erro ao {operation}: {error}',
            screen_content
        )

class BasePage:
    def __init__(self, emulator: Emulator):
        self.emulator = emulator

    def input_text(self, field: str, value: str, offset: int=0) -> bool:
        """Insere texto em um campo específico da tela
        
        Args:
            field: Texto para localizar o campo
            value: Valor a ser inserido
            offset: Deslocamento após o campo
            
        Returns:
            bool: True se o texto foi inserido com sucesso
            
        Raises:
            FieldNotFoundError: Se o campo não for encontrado
            InputError: Se houver erro ao inserir o texto
        """
        logger.info(f'Inserindo texto "{value}" no campo "{field}"')
        try:
            ret = Utils.find_and_send_text(self.emulator, field, value, offset)
            if not ret:
                raise FieldNotFoundError(field, self.emulator)
            return ret
        except Exception as e:
            if not isinstance(e, TerminalError):
                raise InputError(field, value, str(e), self.emulator)
    
    def input_key(self, key: Key, wait: bool = True) -> None:
        """Envia uma tecla para o terminal
        
        Args:
            key: Tecla a ser enviada
            wait: Se deve aguardar após enviar a tecla
            
        Raises:
            KeyError: Se houver erro ao enviar a tecla
        """
        logger.info(f'Enviando tecla {key.name}')
        try:
            Utils.send_key(self.emulator, key, wait)
        except Exception as e:
            if not isinstance(e, TerminalError):
                raise KeyError(key, str(e), self.emulator)
    
    def input_string(self, value: str) -> None:
        """Insere uma string caractere por caractere
        
        Args:
            value: String a ser inserida
            
        Raises:
            InputError: Se houver erro ao inserir a string
        """
        logger.info(f'Inserindo string "{value}"')
        try:
            Utils.send_text(self.emulator, value)
        except Exception as e:
            if not isinstance(e, TerminalError):
                raise InputError('', value, str(e), self.emulator)
    
    def get_value(self, field: str, offset: int=0, length: int=20) -> Optional[str]:
        """Obtém o valor de um campo específico da tela
        
        Args:
            field: Texto para localizar o campo
            offset: Deslocamento após o campo
            length: Tamanho do valor a ser lido
            
        Returns:
            str: Valor lido do campo ou None se não encontrado
            
        Raises:
            FieldNotFoundError: Se o campo não for encontrado
        """
        logger.info(f'Obtendo valor do campo "{field}"')
        try:
            value = Utils.get_value_from_field(self.emulator, field, offset, length)
            if value is None:
                raise FieldNotFoundError(field, self.emulator)
            return value
        except Exception as e:
            if not isinstance(e, TerminalError):
                raise FieldNotFoundError(field, self.emulator)
        
    def print_screen(self) -> None:
        """Imprime a tela atual do terminal
        
        Raises:
            ScreenError: Se houver erro ao capturar ou imprimir a tela
        """
        logger.info('Imprimindo tela atual do terminal')
        try:
            screen = Utils.get_screen(self.emulator)
            if not screen:
                raise ScreenError("Tela vazia ou inválida", "imprimir tela", self.emulator)
            
            print("=" * 80)
            for line in screen:
                print(line)
            print("=" * 80)
        except Exception as e:
            if not isinstance(e, TerminalError):
                raise ScreenError(str(e), "imprimir tela", self.emulator)

    def get_screen(self) -> list[str]:
        """Retorna a tela atual como uma lista de strings
        
        Returns:
            list[str]: Lista com as linhas da tela
            
        Raises:
            ScreenError: Se houver erro ao capturar a tela
        """
        logger.info('Obtendo tela atual do terminal')
        try:
            screen = Utils.get_screen(self.emulator)
            if not screen:
                raise ScreenError("Tela vazia ou inválida", "capturar tela", self.emulator)
            return screen
        except Exception as e:
            if not isinstance(e, TerminalError):
                raise ScreenError(str(e), "capturar tela", self.emulator)        


class Utils:
    config = TerminalConfig()

    @classmethod
    def configure(cls, **kwargs):
        """Configura parâmetros globais do terminal"""
        for key, value in kwargs.items():
            if hasattr(cls.config, key):
                setattr(cls.config, key, value)

    @staticmethod
    def wait(seconds):
        time.sleep(seconds)      

    @staticmethod
    def find_and_send_text(emulator: Emulator, field: str, value: str, offset: int=0):
        # Procura o campo na tela
        rows = Utils.config.SCREEN_ROWS
        cols = Utils.config.SCREEN_COLS
        for row in range(1, rows + 1):
            line = emulator.string_get(row, 1, cols)
            idx = line.find(field)
            if idx != -1:
                # Move o cursor para o campo (após o texto)
                col = idx + len(field) + offset
                emulator.move_to(row, col)
                emulator.send_string(value)
                return True
        return False     

    @staticmethod
    def find_text_position(emulator: Emulator, field: str, offset: int=0):
        rows = Utils.config.SCREEN_ROWS
        cols = Utils.config.SCREEN_COLS
        for row in range(1, rows + 1):
            line = emulator.string_get(row, 1, cols)
            idx = line.find(field)
            if idx != -1:
                if offset >= 0:
                    col = idx + len(field) + offset  # Colunas começam em 1
                else:
                    col = idx - abs(offset) + 1  # Colunas começam em 1
                return (row, col)
        return None 
    
    @staticmethod
    def get_screen(emulator: Emulator):
        rows = Utils.config.SCREEN_ROWS
        cols = Utils.config.SCREEN_COLS
        screen = []
        for row in range(1, rows + 1):
            line = emulator.string_get(row, 1, cols)
            screen.append(line)
        return screen
    
    @staticmethod
    def get_value_from_field(emulator: Emulator, field: str, offset: int=0, length: int=20):
        position = Utils.find_text_position(emulator, field, offset)
        if position:
            row, col = position
            value = emulator.string_get(row, col, length)
            return value.strip()
        return None
    
    @staticmethod
    def send_key(em: Emulator, key: Key, wait: bool = True):
        """
        Envia uma tecla especial para o mainframe
        
        Args:
            em: Emulator object
            key: Enum Key com a tecla a ser enviada (Key.ENTER, Key.PF1, Key.PA1, etc)
            wait: Se deve aguardar após enviar a tecla
        """
        # Dicionário com os métodos correspondentes do emulador
        key_methods = {
            Key.ENTER: em.send_enter,
            Key.TAB: em.exec_command(b'Tab'),
            Key.CLEAR: em.exec_command(b'Clear'),
            Key.RESET: em.exec_command(b'Reset'),
            Key.BACKSPACE: em.exec_command(b'Backspace'),
            Key.DELETE: em.exec_command(b'Delete'),
            Key.NEWLINE: em.exec_command(b'Newline'),
            # PF Keys
            Key.PF1: em.send_pf('1'),
            Key.PF2: em.send_pf('2'),
            Key.PF3: em.send_pf2,
            Key.PF4: em.send_pf4,
            Key.PF5: em.send_pf5,
            Key.PF6: em.send_pf6,
            Key.PF7: em.send_pf7,
            Key.PF8: em.send_pf8,
            Key.PF9: em.send_pf('9'),
            Key.PF10: em.send_pf('10'),
            Key.PF11: em.send_pf('11'),
            Key.PF12: em.send_pf('12'),
            Key.PF13: em.send_pf('13'), # Shift+F1
            Key.PF14: em.send_pf('14'), # Shift+F2
            Key.PF15: em.send_pf('15'), # Shift+F3
            Key.PF16: em.send_pf('16'), # Shift+F4
            Key.PF17: em.send_pf('17'), # Shift+F5
            Key.PF18: em.send_pf('18'), # Shift+F6
            Key.PF19: em.send_pf('19'), # Shift+F7
            Key.PF20: em.send_pf('20'), # Shift+F8
            Key.PF21: em.send_pf('21'), # Shift+F9
            Key.PF22: em.send_pf('22'), # Shift+F10
            Key.PF23: em.send_pf('23'), # Shift+F11
            Key.PF24: em.send_pf('24'), # Shift+F12
            # PA Keys
            Key.PA1: em.exec_command(b'PA1'),
            Key.PA2: em.exec_command(b'PA2'),
            Key.PA3: em.exec_command(b'PA3')
        }

        # Envia a tecla se existir no dicionário
        if key in key_methods:
            key_methods[key]()
            if wait:
                time.sleep(1)
                em.wait_for_field()
        else:
            raise ValueError(f"Tecla {key} não suportada")

    @staticmethod    
    def send_text(emulator: Emulator, value: str):
        for char in value:
            emulator.send_string(char)
            time.sleep(Utils.config.CHAR_DELAY)  # Pausa configurável entre caracteres
        emulator.wait_for_field()