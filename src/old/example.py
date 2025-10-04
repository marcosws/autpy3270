# Exemplo de navegação no terminal 3270 usando py3270
# Certifique-se de instalar py3270: pip install py3270
import os
import time
from enum import Enum
from typing import NamedTuple
os.environ['S3270_PATH'] = r'C:\opt\wc3270\s3270.exe'
from py3270 import Emulator

class ScreenSize(NamedTuple):
    rows: int
    cols: int

class Screen(Enum):
    R24_C80 = ScreenSize(24, 80)    # Tela padrão 3270
    R32_C80 = ScreenSize(32, 80)    # Tela extendida
    R43_C80 = ScreenSize(43, 80)    # Tela extra grande
    R27_C132 = ScreenSize(27, 132)  # Tela wide

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

def print_full_screen(em, screen_size: Screen = Screen.R24_C80):
    print("=" * screen_size.value.cols)
    for row in range(1, screen_size.value.rows + 1):
        line = em.string_get(row, 1, screen_size.value.cols)
        print(line)
    print("=" * screen_size.value.cols)

def send_key(em, key: Key, wait=True):
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

def find_and_send_text(em, field, value, offset=0, screen_size: Screen = Screen.R24_C80):
    # Procura o campo na tela
    for row in range(1, screen_size.value.rows + 1):
        line = em.string_get(row, 1, screen_size.value.cols)
        idx = line.find(field)
        if idx != -1:
            # Move o cursor para o campo (após o texto)
            col = idx + len(field) + offset
            em.move_to(row, col)
            em.send_string(value)
            send_key(em, Key.ENTER)
            return True
    return False


# Inicializa o emulador (mude o caminho do x3270 se necessário)
em = Emulator(visible=False, timeout=30)

# Conecta ao host mainframe
em.connect('192.168.15.23:23')

# Aguarda tela inicial
em.wait_for_field()

# Captura e imprime a tela inteira como texto
print_full_screen(em)

# Envia usuário
em.send_string('l tso')
print_full_screen(em)
send_key(em, Key.ENTER)
print_full_screen(em)

em.send_string('ibmuser')
print_full_screen(em)
send_key(em, Key.ENTER)
print_full_screen(em)


em.wait_for_field()
if find_and_send_text(em, "Password  ===>", "sys1" , offset=2):
    print("Senha enviada!")
else:
    print("Campo de senha não encontrado.")
time.sleep(2)
em.wait_for_field()
print_full_screen(em)

send_key(em, Key.PF8)
print_full_screen(em)

send_key(em, Key.ENTER)
print_full_screen(em)

# Fecha a conexão
em.terminate()




