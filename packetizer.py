from enum import Enum

class Parser():

    def __init__(self) -> None:
        self.carryover = bytearray()

    def process_data(self, data: bytearray) -> [bytearray]:

        class State(Enum):
            (HEADER, LEN_1, LEN_2, DATA, FOOTER) = range(5)

        state = State.HEADER
        buf = bytearray()
        data_len = None
        packets = []
        for _, val in enumerate(self.carryover + data):
            byte = val.to_bytes()
            if state == State.HEADER:
                if byte == b'<':
                    buf.extend(byte)
                    state = State.LEN_1
                continue
            if state == State.LEN_1:
                buf.extend(byte)
                state = State.LEN_2
                continue
            if state == State.LEN_2:
                buf.extend(byte)
                state = State.DATA
                data_len = int.from_bytes(buf[1:3])
                continue
            if state == State.DATA:
                buf.extend(byte)
                if len(buf) - 3 == data_len:
                    state = State.FOOTER
                if len(buf) - 3 > data_len:
                    raise AssertionError('should not reach this point.  check logic.')
                continue
            if state == State.FOOTER:
                buf.extend(byte)
                if buf[0] != ord('<') or buf[-1] != ord('>'):
                    raise AssertionError('wrong packet header or footer.  check logic.')
                if int.from_bytes(buf[1:3]) != len(buf[3:-1]):
                    raise AssertionError('packet data length does not match.  check logic.')
                packets.append(buf[3:-1])
                state = State.HEADER
                self.carryover = bytearray()
                buf = bytearray()
                data_len = None
                continue
        self.carryover.extend(buf)
        return packets