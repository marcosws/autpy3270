# Exemplo de navegação no terminal 3270 usando py3270
# Certifique-se de instalar py3270: pip install py3270
import os
import time
os.environ['S3270_PATH'] = r'C:\opt\wc3270\s3270.exe'
from py3270 import Emulator

def print_full_screen(em, rows=24, cols=80):
    print("============================================ TELA INTEIRA ============================================")
    for row in range(1, rows + 1):
        line = em.string_get(row, 1, cols)
        print(line)

def find_and_send_text(em, field, value, offset=0 ,rows=24, cols=80):
    # Procura o campo "Password  ===>" na tela
    for row in range(1, rows + 1):
        line = em.string_get(row, 1, cols)
        idx = line.find(field)
        if idx != -1:
            # Move o cursor para o campo de senha (após o texto)
            col = idx + len(field) + offset
            em.move_to(row, col)
            em.send_string(value)
            em.send_enter()
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
em.send_enter()
time.sleep(2) # espera 2 segundos
em.wait_for_field()
print_full_screen(em)

em.send_string('ibmuser')
print_full_screen(em)
em.send_enter()
time.sleep(2) # espera 2 segundos
em.wait_for_field()
print_full_screen(em)


em.wait_for_field()
if find_and_send_text(em, "Password  ===>", "sys1" , offset=2):
    print("Senha enviada!")
else:
    print("Campo de senha não encontrado.")
time.sleep(2)
em.wait_for_field()
print_full_screen(em)

em.send_pf8()
time.sleep(2)
em.wait_for_field()
print_full_screen(em)

em.send_enter()
time.sleep(2)
em.wait_for_field()
print_full_screen(em)

# Fecha a conexão
em.terminate()




