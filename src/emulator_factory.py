

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fábrica para criar e gerenciar instâncias do emulador 3270.
Fornece métodos para criar, conectar e gerenciar o ciclo de vida do emulador.

Created on: October 3, 2025
Author: Marcos WS
Version: 1.0.0
"""

from typing import Optional, ClassVar
import logging
from py3270 import Emulator
from base_page import TerminalError

logger = logging.getLogger(__name__)

class EmulatorError(TerminalError):
    """Exceção base para erros relacionados ao emulador"""
    pass

class ConnectionError(EmulatorError):
    """Exceção para erros de conexão"""
    pass

class TimeoutError(EmulatorError):
    """Exceção para erros de timeout"""
    pass

class InitializationError(EmulatorError):
    """Exceção para erros de inicialização"""
    pass

class EmulatorFactory:
    """Fábrica responsável por criar e gerenciar instâncias do emulador 3270.

    Esta classe combina funcionalidades de fábrica e singleton para criar,
    gerenciar e fornecer acesso global ao emulador 3270, facilitando
    a automação de terminais mainframe.

    Attributes:
        _instance (ClassVar[Optional[Emulator]]): Instância global do emulador.
        emulador: Instância local do emulador 3270 gerenciada pela fábrica.
    """

    # Atributo estático para armazenar a instância global do emulador
    _instance: ClassVar[Optional[Emulator]] = None

    def __init__(self):
        """Inicializa uma nova instância da fábrica de emuladores.

        A instância é criada sem um emulador ativo, que deve ser criado
        posteriormente usando o método create_emulator().
        """
        self.emulator = None

    @classmethod
    def get_instance(cls) -> Optional[Emulator]:
        """Retorna a instância global do emulador.

        Returns:
            Optional[Emulator]: A instância global do emulador ou None se não inicializado.

        Examples:
            >>> emulator = EmulatorFactory.get_instance()
            >>> if emulator:
            ...     emulator.send_string('comando')
        """
        return cls._instance

    @classmethod
    def set_instance(cls, emulator: Optional[Emulator]) -> None:
        """Define a instância global do emulador.

        Args:
            emulator: Nova instância do emulador ou None para limpar

        Examples:
            >>> EmulatorFactory.set_instance(my_emulator)
            >>> # Limpando a instância global
            >>> EmulatorFactory.set_instance(None)
        """
        cls._instance = emulator
        logger.info(f"Instância global do emulador {'definida' if emulator else 'removida'}")

    def create_emulator(self, host: str, visible: bool = False):
        """Cria e inicializa uma nova instância do emulador 3270.

        Args:
            host (str): Endereço do host mainframe para conexão
                (ex: 'hostname.com:23' ou 'ip:porta').
            visible (bool, optional): Se True, exibe a interface gráfica do
                emulador. Padrão é False para execução em background.

        Raises:
            InitializationError: Se houver falha na criação ou conexão do emulador.

        Examples:
            >>> factory = EmulatorFactory()
            >>> factory.create_emulator('mainframe.company.com:23')
        """
        try:
            logger.info(f"Criando emulador para host: {host} (visible: {visible})")
            self.emulador = Emulator(visible=visible)
            self.emulador.connect(host)
            self.emulador.wait_for_field()
            # Define a instância global
            self.set_instance(self.emulador)
            logger.info("Emulador criado e conectado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar emulador: {str(e)}")
            self.emulador = None
            raise InitializationError(f"Falha ao criar emulador: {str(e)}")

    def terminate_emulator(self):
        """Encerra a conexão e finaliza a instância atual do emulador.

        Este método desconecta do host mainframe e libera os recursos do emulador.
        Se não houver emulador ativo, a operação é ignorada silenciosamente.

        Raises:
            EmulatorError: Se houver erro ao tentar finalizar o emulador.

        Examples:
            >>> factory = EmulatorFactory()
            >>> factory.create_emulator('host.com:23')
            >>> factory.terminate_emulator()  # Finaliza o emulador
        """
        try:
            if self.emulador:
                logger.info("Terminando conexão do emulador")
                self.emulador.terminate()
                self.emulador = None
                # Limpa a instância global
                self.set_instance(None)
                logger.info("Emulador terminado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao terminar emulador: {str(e)}")
            raise EmulatorError(f"Falha ao terminar emulador: {str(e)}")

    def get_emulator(self):
        """Retorna a instância atual do emulador 3270.

        Returns:
            Emulator: A instância atual do emulador 3270.

        Raises:
            EmulatorError: Se o emulador não estiver inicializado ou
                houver erro ao acessá-lo.

        Examples:
            >>> factory = EmulatorFactory()
            >>> factory.create_emulator('host.com:23')
            >>> emulator = factory.get_emulator()
            >>> emulator.send_string('usuario')
        """
        try:
            if not self.emulador:
                logger.warning("Tentativa de obter emulador não inicializado")
                raise EmulatorError("Emulador não foi inicializado")
            return self.emulador
        except Exception as e:
            logger.error(f"Erro ao obter emulador: {str(e)}")
            raise EmulatorError(f"Falha ao obter emulador: {str(e)}")

    def is_connected(self) -> bool:
        """Verifica se existe uma conexão ativa com o emulador.

        Returns:
            bool: True se houver um emulador inicializado e conectado,
                False caso contrário.

        Raises:
            EmulatorError: Se houver erro ao verificar o status da conexão.

        Examples:
            >>> factory = EmulatorFactory()
            >>> factory.is_connected()
            False
            >>> factory.create_emulator('host.com:23')
            >>> factory.is_connected()
            True
        """
        try:
            is_connected = self.emulador is not None
            logger.debug(f"Status de conexão do emulador: {is_connected}")
            return is_connected
        except Exception as e:
            logger.error(f"Erro ao verificar status de conexão: {str(e)}")
            raise EmulatorError(f"Falha ao verificar status de conexão: {str(e)}")




