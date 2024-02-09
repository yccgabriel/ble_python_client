import unittest
from packetizer import Parser

x1 = bytearray(b'<\x00\x05hello>')
y1 = [bytearray(b'hello')]
x2 = bytearray(b'<\x00\x07<hello>>')
y2 = [bytearray(b'<hello>')]
x3 = bytearray(b'<\x00\x0cfirst_packet><\x00\x0dsecond_packet>')
y3 = [bytearray(b'first_packet'), bytearray(b'second_packet')]
x4 = bytearray(b'<<\x00\x05hello>')
y4 = []
x5 = bytearray(b'xxxx<\x00\x05hello>xxxx')
y5 = [bytearray(b'hello')]
x6 = bytearray(b'<\x00\x05hello>>')
y6 = [bytearray(b'hello')]
x7a = bytearray(b'<\x00\x0cfirst_pac')
x7b = bytearray(b'ket><\x00\x0dsecond_packet>')
y7a = []
y7b = [bytearray(b'first_packet'), bytearray(b'second_packet')]
x8a = bytearray(b'<\x00\x0cfirst_packet><\x00\x0dsec')
x8b = bytearray(b'ond_packet>')
y8a = [bytearray(b'first_packet')]
y8b = [bytearray(b'second_packet')]
x9 = bytearray(b'A><SD><ASD><SA><F><AS>F<SA><D><SA><D><S>G<DS><VD<#R><#><@G#@#RF<>#><V<>@##')
y9 = []
x10a = bytearray(b'!@<>R@<#T>G!<F!>#<>!@#D<F><\x00\x0cfirs')
x10b = bytearray(b't_packe')
x10c = bytearray(b't>@!<$><@!>$@!><#>!@<FEDD><\x00')
x10d = bytearray(b'\x0dsecond_packet>@!#@!<>@!<#>!@R#F>D<>...')
y10a = []
y10b = []
y10c = [bytearray(b'first_packet')]
y10d = [bytearray(b'second_packet')]

class TestPacketizer(unittest.TestCase):

    def test_hello(self):
        p = Parser()
        self.assertEqual(y1, p.process_data(x1))

    def test_bracket_hello(self):
        p = Parser()
        self.assertEqual(y2, p.process_data(x2))

    def test_two_packets(self):
        p = Parser()
        self.assertEqual(y3, p.process_data(x3))

    def test_double_header(self):
        p = Parser()
        self.assertEqual(y4, p.process_data(x4))

    def test_nonsense_before_and_after_packet(self):
        p = Parser()
        self.assertEqual(y5, p.process_data(x5))

    def test_double_footer(self):
        p = Parser()
        self.assertEqual(y6, p.process_data(x6))

    def test_shift_data_to_later(self):
        p = Parser()
        self.assertEqual(y7a, p.process_data(x7a))
        self.assertEqual(y7b, p.process_data(x7b))

    def test_shift_data_to_earlier(self):
        p = Parser()
        self.assertEqual(y8a, p.process_data(x8a))
        self.assertEqual(y8b, p.process_data(x8b))

    def test_rubbish(self):
        p = Parser()
        self.assertEqual(y9, p.process_data(x9))

    def test_packets_in_rubbish(self):
        p = Parser()
        self.assertEqual(y10a, p.process_data(x10a))
        self.assertEqual(y10b, p.process_data(x10b))
        self.assertEqual(y10c, p.process_data(x10c))
        self.assertEqual(y10d, p.process_data(x10d))

if __name__ == '__main__':
    unittest.main()