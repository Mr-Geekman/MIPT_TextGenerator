"""
This module generates a sequence of words using model created by train.py
Generation based on Markov chains
To view command line arguments start program with --help
"""
import argparse
import sys
import pickle
import random
from check_args import is_valid_file, is_positive_int


def generate_seed(frequencies, seed=None):
    """
    Generate first chain_len - 1 words in generated sequence
    :param frequencies: dictionary with word's frequencies
    :param seed: first word in generated sequence
    :return: seed
    """
    if seed is not None:
        random.choice([x for x in frequencies.keys() if x[0] == seed])
    else:
        return random.choice(list(frequencies.keys()))


def generate_new_word(frequencies, body, chain_len):
    """
    Generate new word for generated sequence
    :param frequencies: dictionary with word's frequencies
    :param body: word sequence for generating new word
    :param chain_len: length of Markov chain
    :return: new word
    """
    if len(body) == chain_len - 1:
        words = list(frequencies[body].elements())
    elif len(body) > 0:
        words = [x[len(body)] for x in frequencies.keys()
                 if x[:len(body)] == body]
    else:
        words = [random.choice(list(frequencies.keys()))[0]]
    if not words:
        return generate_new_word(frequencies, body[1:], chain_len)
    return random.choice(words)


def generate_sequence(frequencies, seed, chain_len, length):
    """
    Generate word sequence
    :param frequencies: dictionary with word's frequencies
    :param seed: first word in generated sequence
    :param chain_len: length of Markov chain
    :param length: length of generated sequence
    :return: generated sequence
    """
    generated_sequence = []
    generated_sequence += generate_seed(frequencies, seed)
    while len(generated_sequence) < length:
        generated_sequence.append(
            generate_new_word(
                frequencies,
                tuple(generated_sequence[-chain_len + 1:]),
                chain_len)
        )
    return generated_sequence[:length]


def write_result(output, generated_sequence):
    """
    Write generated sequence in output
    :param output: file or stdout
    :param generated_sequence: generated word sequence
    """
    output.write(' '.join(generated_sequence))


def parse_command_line_arguments():
    """
    Create a parser for parsing command line arguments and parse it
    :return: command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Create a sequence of words by model')
    parser.add_argument('--model', type=lambda x: is_valid_file(parser, x),
                        required=True, help='File for loading model')
    parser.add_argument('--seed', help='First word in generated sequence')
    parser.add_argument('--length', type=lambda x: is_positive_int(parser, x),
                        required=True, help='Length of generated sequence')
    parser.add_argument('--output',
                        type=lambda x: is_valid_file(parser, x),
                        help='File for write generated sequence \
                        (default: stdout)')
    args = parser.parse_args()
    return args


def main():
    args = parse_command_line_arguments()
    model_file = args.model
    seed = args.seed
    length = args.length
    output_file = args.output
    # Load dictionary with chain length and frequencies
    with open(model_file, 'rb') as inf:
        chain_len, frequencies = pickle.load(inf)
    generated_sequence = generate_sequence(
        frequencies, seed, chain_len, length)
    # Write a result
    if output_file is None:
        write_result(sys.stdout, generated_sequence)
    else:
        with open(output_file, 'w') as ouf:
            write_result(ouf, generated_sequence)


if __name__ == "__main__":
    main()