from typing import Dict, List, Any

def character_count_framing(frames: List[str]) -> List[str]:
    """Generates frames using Character Count framing technique."""
    result = []
    for f in frames:
        count = len(f) + 1  # includes length header
        result.append(f"{count}{f}")
    return result

def byte_stuffing(data: str, flag: str = "FLAG", esc: str = "ESC") -> str:
    """Demonstrates Byte/Character Stuffing."""
    stuffed = ""
    i = 0
    while i < len(data):
        if data[i:i+len(flag)] == flag:
            stuffed += esc + flag
            i += len(flag)
        elif data[i:i+len(esc)] == esc:
            stuffed += esc + esc
            i += len(esc)
        else:
            stuffed += data[i]
            i += 1
    return f"{flag}{stuffed}{flag}"

def bit_stuffing(bit_stream: str) -> Dict[str, str]:
    """Demonstrates Bit Stuffing (applies 0 after five consecutive 1s)."""
    count = 0
    stuffed = ""
    for bit in bit_stream:
        if bit == '1':
            count += 1
            stuffed += '1'
            if count == 5:
                stuffed += '0'
                count = 0
        else:
            count = 0
            stuffed += '0'

    flag = "01111110"
    return {
        "original_bits": bit_stream,
        "stuffed_bits": stuffed,
        "framed_stream": f"{flag}{stuffed}{flag}"
    }