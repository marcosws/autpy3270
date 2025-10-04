from enum import Enum
from typing import NamedTuple

class ScreenSize(NamedTuple):
    rows: int
    cols: int

class Screen(Enum):
    R24_C80 = ScreenSize(24, 80)    # Tela padrão 3270
    R32_C80 = ScreenSize(32, 80)    # Tela extendida
    R43_C80 = ScreenSize(43, 80)    # Tela extra grande
    R27_C132 = ScreenSize(27, 132)  # Tela wide

# Modifique a função print_full_screen para usar o novo Enum
def print_full_screen(em, screen_size: Screen = Screen.R24_C80):
    print("=" * 80)
    for row in range(1, screen_size.value.rows + 1):
        line = em.string_get(row, 1, screen_size.value.cols)
        print(line)
    print("=" * 80)

# Modifique a função find_and_send_text para usar o novo Enum
def find_and_send_text(em, field, value, offset=0, screen_size: Screen = Screen.R24_C80):
    for row in range(1, screen_size.value.rows + 1):
        line = em.string_get(row, 1, screen_size.value.cols)
        idx = line.find(field)
        if idx != -1:
            col = idx + len(field) + offset
            em.move_to(row, col)
            em.send_string(value)
            send_key(em, Key.ENTER)
            return True
    return False


# Exemplo de uso:
rows, cols = Screen.R24_C80.value
print(f"Linhas: {rows}, Colunas: {cols}")

# Ou passar direto para as funções
print_full_screen(em, Screen.R24_C80)
find_and_send_text(em, "Password  ===>", "sys1", offset=2, screen_size=Screen.R24_C80)

# Ou desempacotar os valores
rows, cols = Screen.R32_C80.value
print(f"Tela grande: {rows}x{cols}")