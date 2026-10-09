from typing import Dict

def compute_crc(data_bits: str, polynomial_bits: str) -> Dict[str, str]:
    """
    Computes Cyclic Redundancy Check (CRC) remainder from scratch via polynomial modulo-2 division.
    Supports CRC-12, CRC-16, CRC-CCITT polynomials.
    """
    # Polynomial presets if string key passed
    poly_map = {
        "CRC-12": "1100000001111",
        "CRC-16": "11000000000000101",
        "CRC-CCITT": "10001000000100001"
    }

    poly = poly_map.get(polynomial_bits, polynomial_bits)
    m = len(poly) - 1

    # Append m zeros to data
    padded_data = data_bits + "0" * m
    data_list = list(padded_data)
    poly_list = list(poly)

    for i in range(len(data_bits)):
        if data_list[i] == '1':
            for j in range(len(poly)):
                data_list[i + j] = '0' if data_list[i + j] == poly_list[j] else '1'

    remainder = "".join(data_list[-m:])
    transmitted_frame = data_bits + remainder

    return {
        "data_bits": data_bits,
        "polynomial": poly,
        "crc_remainder": remainder,
        "transmitted_frame": transmitted_frame,
        "explanation": "CRC is an error-detecting code for accidental transmission errors, NOT a cryptographic security hash."
    }


def verify_crc(received_frame: str, polynomial_bits: str) -> bool:
    """Verifies CRC for a received binary frame."""
    poly_map = {
        "CRC-12": "1100000001111",
        "CRC-16": "11000000000000101",
        "CRC-CCITT": "10001000000100001"
    }
    poly = poly_map.get(polynomial_bits, polynomial_bits)
    m = len(poly) - 1

    frame_list = list(received_frame)
    poly_list = list(poly)

    for i in range(len(received_frame) - m):
        if frame_list[i] == '1':
            for j in range(len(poly)):
                frame_list[i + j] = '0' if frame_list[i + j] == poly_list[j] else '1'

    remainder = "".join(frame_list[-m:])
    return remainder == "0" * m