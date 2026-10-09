from app.algorithms.crc import compute_crc, verify_crc
from app.algorithms.framing import bit_stuffing

def test_crc_computation_and_verification():
    res = compute_crc("1101011011", "CRC-16")
    frame = res["transmitted_frame"]
    assert verify_crc(frame, "CRC-16") is True

def test_bit_stuffing():
    res = bit_stuffing("111111")
    assert "1111101" in res["stuffed_bits"]