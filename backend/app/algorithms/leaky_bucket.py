from typing import List, Dict, Any

def simulate_leaky_bucket(capacity: int, leak_rate: int, incoming_packets: List[int]) -> Dict[str, Any]:
    """Simulates the Leaky Bucket traffic shaping algorithm."""
    bucket_level = 0
    steps = []
    total_dropped = 0

    for step_num, packet_size in enumerate(incoming_packets, 1):
        # Arrive
        if bucket_level + packet_size <= capacity:
            bucket_level += packet_size
            dropped = 0
        else:
            overflow = (bucket_level + packet_size) - capacity
            bucket_level = capacity
            dropped = overflow
            total_dropped += dropped

        # Leak
        leaked = min(bucket_level, leak_rate)
        bucket_level -= leaked

        steps.append({
            "step": step_num,
            "incoming": packet_size,
            "bucket_after_arrival": bucket_level + leaked,
            "leaked": leaked,
            "dropped": dropped,
            "bucket_remaining": bucket_level
        })

    return {
        "capacity": capacity,
        "leak_rate": leak_rate,
        "total_dropped_packets": total_dropped,
        "simulation_steps": steps
    }