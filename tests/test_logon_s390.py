



class TestLogonS390:
    

    def test_logon_s390(self, emulator_factory):
        emulator = emulator_factory.get_emulator()
        assert emulator is not None
        assert emulator.is_connected()
        # Adicione mais verificações específicas do logon S390 aqui
        # Por exemplo, verificar se a tela inicial está correta
        screen_content = emulator.string_get(1, 1, 80)
        assert "IBM" in screen_content  # Exemplo de verificação
