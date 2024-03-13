import unittest
from packetizer import Parser

class TestPacketizer(unittest.TestCase):

    def test_hello(self):
        x = bytearray(b'<\x00\x05\x1bhello>')
        y = [bytearray(b'hello')]
        p = Parser()
        self.assertEqual(y, p.process_data(x))

    def test_bracket_hello(self):
        x = bytearray(b'<\x00\x07\x15<hello>>')
        y = [bytearray(b'<hello>')]
        p = Parser()
        self.assertEqual(y, p.process_data(x))

    def test_two_packets(self):
        x = bytearray(b'<\x00\x0c\x24first_packet><\x00\x0d\x23second_packet>')
        y = [bytearray(b'first_packet'), bytearray(b'second_packet')]
        p = Parser()
        self.assertEqual(y, p.process_data(x))

    def test_double_header(self):
        x = bytearray(b'<<\x00\x05\x1bhello>')
        y = []
        p = Parser()
        self.assertEqual(y, p.process_data(x))

    def test_nonsense_before_and_after_packet(self):
        x = bytearray(b'xxxx<\x00\x05\x1bhello>xxxx')
        y = [bytearray(b'hello')]
        p = Parser()
        self.assertEqual(y, p.process_data(x))

    def test_double_footer(self):
        x = bytearray(b'<\x00\x05\x1bhello>>')
        y = [bytearray(b'hello')]
        p = Parser()
        self.assertEqual(y, p.process_data(x))

    def test_shift_data_to_later(self):
        x_a = bytearray(b'<\x00\x0c\x24first_pac')
        x_b = bytearray(b'ket><\x00\x0d\x23second_packet>')
        y_a = []
        y_b = [bytearray(b'first_packet'), bytearray(b'second_packet')]
        p = Parser()
        self.assertEqual(y_a, p.process_data(x_a))
        self.assertEqual(y_b, p.process_data(x_b))


    def test_shift_data_to_earlier(self):
        x_a = bytearray(b'<\x00\x0c\x24first_packet><\x00\x0d\x23sec')
        x_b = bytearray(b'ond_packet>')
        y_a = [bytearray(b'first_packet')]
        y_b = [bytearray(b'second_packet')]
        p = Parser()
        self.assertEqual(y_a, p.process_data(x_a))
        self.assertEqual(y_b, p.process_data(x_b))

    def test_rubbish(self):
        x = bytearray(b'A><SD><ASD><SA><F><AS>F<SA><D><SA><D><S>G<DS><VD<#R><#><@G#@#RF<>#><V<>@##')
        y = []
        p = Parser()
        self.assertEqual(y, p.process_data(x))

    def test_packets_in_rubbish(self):
        x_a = bytearray(b'!@<>R@<#T>G!<F!>#<>!@#!%(*&#@^(<\x00\x0c\x24firs')
        x_b = bytearray(b't_packe')
        x_c = bytearray(b't>@!<$><@!>$@#%!^%&*<F^&#*@%^#<\x00')
        x_d = bytearray(b'\x0d\x23second_packet>@!#@!<>@!<#>!@R#F>D<>...')
        y_a = []
        y_b = []
        y_c = [bytearray(b'first_packet')]
        y_d = [bytearray(b'second_packet')]
        p = Parser()
        self.assertEqual(y_a, p.process_data(x_a))
        self.assertEqual(y_b, p.process_data(x_b))
        self.assertEqual(y_c, p.process_data(x_c))
        self.assertEqual(y_d, p.process_data(x_d))

if __name__ == '__main__':
    unittest.main()
