"""
Landau Audio Looper

Takes an audio sample of n seconds, splits it according to the optimal
Landau partition, loops each segment, and stacks them to create a new
audio clip of g(n) seconds.
"""

from math import lcm
from functools import reduce
import numpy as np
import argparse
import sys
import os


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


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog='landau-sampler',
        description='Process audio files using the Landau function to create maximally coprime polyrhythmic loops'
    )

    # Input file (required, positional)
    parser.add_argument('input', help='Input audio file path')

    # Output file (optional, supports both positional and flag syntax)
    parser.add_argument('output', nargs='?', help='Output audio file path (optional)')
    parser.add_argument('-o', '--output-file', dest='output_flag',
                        help='Output file path (alternative to positional argument)')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Check for soundfile library
    try:
        import soundfile
    except ImportError:
        print("Error: soundfile library required", file=sys.stderr)
        print("Install with: pip install soundfile", file=sys.stderr)
        sys.exit(1)

    # Validate input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Determine output path (priority: -o flag > positional > default)
    output_path = args.output_flag or args.output

    # Process the audio file
    try:
        landau_audio_loop_from_file(args.input, output_path)
    except Exception as e:
        print(f"Error processing audio: {e}", file=sys.stderr)
        sys.exit(1)
