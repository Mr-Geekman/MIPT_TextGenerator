"""
This module creates model for generating new texts.
To view command line arguments start program with --help
"""

import argparse
import sys
import re
import pickle
import collections
import codecs
import fileinput
from check_args import *


def collect_files(input_dir):
    """
    Collect all valid .txt utf-8 files in input_dir (recursively)
    :param input_dir: directory with files for training
    :return: list of files
    """
    files = []
    for dir in os.walk(input_dir):
        for file in os.listdir(dir[0]):
            file_path = os.path.join(dir[0], file)
            if os.path.isfile(file_path) and file.endswith('txt') and \
                    is_file_in_utf_8(file_path):
                files.append(file_path)
    return files


def read_source(source, frequencies, is_lowercase, chain_len):
    """
    Read source file and update frequencies dictionary
    :param source: file or stdin
    :param frequencies: dictionary with word's frequencies
    :param is_lowercase: if it is true all words become lowercase
    :param chain_len: length of Markov chain
    """
    additional_line = ""
    for line in source:
        line = additional_line + line
        if is_lowercase:
            line = line.lower()
        words = tuple(re.findall(r'\w+', line))
        if len(words) < chain_len:
            additional_line = line
        else:
            chain_len_grams = (words[i: i + chain_len]
                               for i in range(len(words) - chain_len + 1))
            for chain_len_gram in chain_len_grams:
                frequencies[chain_len_gram[:-1]][chain_len_gram[-1]] += 1
            additional_line = line[-(chain_len - 1):]


def is_file_in_utf_8(file_path):
    """
    Check that I can open file with utf-8
    :param file_path: file path in file system
    :return: can or can't
    """
    try:
        with codecs.open(file_path, 'r', 'utf-8') as source:
            source.readline()
        return True
    except UnicodeDecodeError:
        return False


def parse_command_line_arguments():
    """
    Create a parser for parsing command line arguments and parse it
    :return: command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Create a model for generation new texts')
    parser.add_argument('--input-dir',
                        type=lambda x: is_valid_dir(parser, x),
                        help='Directory with *.txt utf-8 documents '
                             '(default: stdin)',
                        dest='input_dir')
    parser.add_argument('--model', type=lambda x: is_valid_file(parser, x),
                        required=True, help='File for saving model')
    parser.add_argument('--lc', action='store_true', default=False,
                        help='Do lowercase', dest='is_lowercase')
    parser.add_argument('--N', type=lambda x: is_positive_int(parser, x),
                        default=2,
                        help='Choice count of elements in Markov chain \
                        (default: 2)')
    args = parser.parse_args()
    return args


def main():
    args = parse_command_line_arguments()
    input_dir = args.input_dir
    model_file = args.model
    is_lowercase = args.is_lowercase
    chain_len = args.N
    # Read files from input-dir (or from stdin) and create dictionary
    frequencies = collections.defaultdict(collections.Counter)
    if input_dir is None:
        source = sys.stdin
        read_source(source, frequencies, is_lowercase, chain_len)
    else:
        files = collect_files(input_dir)
        read_source(fileinput.input(files), frequencies, is_lowercase, chain_len)
    # Save result dictionary and chain_len in file
    with open(model_file, 'wb') as ouf:
        pickle.dump([chain_len, frequencies], ouf)


if __name__ == "__main__":
    main()
