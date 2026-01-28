"""
Landau Audio Looper

Takes an audio sample of n seconds, splits it according to the optimal
Landau partition, loops each segment, and stacks them to create a new
audio clip of g(n) seconds.
"""

from math import lcm
from functools import reduce
import numpy as np


def lcm_list(lst):
    """Calculate LCM of a list of integers."""
    return reduce(lcm, lst, 1)


def partitions(n, max_val=None):
    """Generate all integer partitions of n with parts <= max_val."""
    if max_val is None:
        max_val = n
    if n == 0:
        yield []
        return
    for i in range(min(n, max_val), 0, -1):
        for p in partitions(n - i, i):
            yield [i] + p


def landau(n):
    """
    Find g(n), and an optimal partition.
    g(n) is the Landau function of n,
    which finds the max lcm of any integer partition of n.

    Returns:
        tuple: (g(n), optimal_partition)
        e.g.
            5 -> (6, (3, 2))
            12 -> (60, (5, 4, 3))
    """
    best_lcm = 0
    best_partition = []
    for p in partitions(n):
        l = lcm_list(p)
        if l > best_lcm:
            best_lcm = l
            best_partition = p
    return best_lcm, best_partition


def landau_audio_loop(audio, sample_rate, partition=None):
    """
    Take an audio sample of n seconds, split it according to the Landau
    partition, loop each segment to g(n) seconds, and mix them together.

    Args:
        audio: numpy array of audio samples (mono or stereo)
        sample_rate: sample rate in Hz
        partition: optional pre-computed partition (list of ints).
                   If None, will compute optimal Landau partition.

    Returns:
        tuple: (output_audio, g_n, partition_used)
    """
    # Handle mono vs stereo
    if audio.ndim == 1:
        audio = audio.reshape(-1, 1)

    n_samples, n_channels = audio.shape
    duration_seconds = n_samples / sample_rate
    n = int(round(duration_seconds))

    if abs(duration_seconds - n) > 0.1:
        print(
            f"Warning: Audio duration ({duration_seconds:.2f}s) is not close to an integer. "
            f"Using n={n}"
        )

    # Get Landau partition
    if partition is None:
        g_n, partition = landau(n)
    else:
        g_n = lcm_list(partition)
        if sum(partition) != n:
            raise ValueError(f"Partition {partition} sums to {sum(partition)}, not {n}")

    print(f"Audio duration: {duration_seconds:.2f}s (using n={n})")
    print(f"Landau partition: {partition}")
    print(f"g({n}) = {g_n}")
    print(f"Output duration: {g_n} seconds")

    # Calculate output size
    output_samples = g_n * sample_rate
    output = np.zeros((output_samples, n_channels), dtype=np.float64)

    # Split audio according to partition and loop each segment
    current_pos = 0
    for i, part_length in enumerate(partition):
        # Extract segment (in samples)
        start_sample = current_pos
        end_sample = current_pos + part_length * sample_rate
        segment = audio[start_sample:end_sample]

        # Calculate how many times to loop
        n_loops = g_n // part_length

        print(f"  Segment {i+1}: {part_length}s × {n_loops} loops = {g_n}s")

        # Loop and add to output
        for loop in range(n_loops):
            loop_start = loop * len(segment)
            loop_end = loop_start + len(segment)
            output[loop_start:loop_end] += segment

        current_pos = end_sample

    # Normalize to prevent clipping
    max_val = np.max(np.abs(output))
    if max_val > 0:
        output = output / max_val

    # Squeeze back to mono if input was mono
    if n_channels == 1:
        output = output.squeeze()

    return output, g_n, partition


def landau_audio_loop_from_file(input_path, output_path=None):
    """
    Convenience function to process an audio file directly.

    Args:
        input_path: path to input audio file
        output_path: path for output file (default: adds '_landau' suffix)

    Returns:
        tuple: (output_audio, sample_rate, g_n, partition)
    """
    try:
        import soundfile as sf
    except ImportError:
        raise ImportError("Please install soundfile: pip install soundfile")

    # Load audio
    audio, sample_rate = sf.read(input_path)

    # Process
    output, g_n, partition = landau_audio_loop(audio, sample_rate)

    # Save if output path provided
    if output_path is None:
        import os

        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_landau{ext}"

    sf.write(output_path, output, sample_rate)
    print(f"Saved to: {output_path}")

    return output, sample_rate, g_n, partition


# Example usage and demo with synthetic audio
if __name__ == "__main__":
    # Demo with a synthetic 5-second audio clip
    sample_rate = 44100
    n_seconds = 10

    # Create a simple test signal: different frequencies for each "section"
    # This will help us hear the looping effect
    t = np.linspace(0, n_seconds, n_seconds * sample_rate, endpoint=False)

    # Create audio that changes character over time so we can hear the splits
    audio = np.zeros_like(t)
    audio += 0.3 * np.sin(2 * np.pi * 220 * t)  # Base A3
    audio += 0.3 * np.sin(2 * np.pi * 440 * t) * (t / n_seconds)  # Rising A4
    audio += (
        0.2 * np.sin(2 * np.pi * 330 * t) * ((n_seconds - t) / n_seconds)
    )  # Falling E4

    print("=" * 50)
    print("LANDAU AUDIO LOOPER DEMO")
    print("=" * 50)
    print()

    output, g_n, partition = landau_audio_loop(audio, sample_rate)

    print()
    print(f"Input: {len(audio)} samples ({n_seconds}s)")
    print(f"Output: {len(output)} samples ({g_n}s)")

    # Save demo files
    try:
        import soundfile as sf

        fname_input = f"demo_input_{n_seconds}s.wav"
        fname_output = f"demo_output_landau_{g_n}s.wav"
        sf.write(f"/Users/oisin/{fname_input}", audio, sample_rate)
        sf.write(f"/Users/oisin/{fname_output}", output, sample_rate)
        print()
        print("Demo files saved:")
        print(f"  - {fname_input} ({n_seconds} seconds)")
        print(f"  - {fname_output} ({g_n} seconds)")
    except ImportError:
        print()
        print("Install soundfile to save demo: pip install soundfile")
