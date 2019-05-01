"""
Module for checking command line arguments
"""

import os


def is_valid_file(parser, arg):
    """
    Check that arg is file
    :param parser: parser command line arguments
    :param arg: command line argument
    :return: correct argument
    """
    if not os.path.isfile(arg):
        parser.error("The file {} does not exists!".format(arg))
    else:
        return arg


def is_valid_dir(parser, arg):
    """
    Check that arg is directory
    :param parser: parser command line arguments
    :param arg: command line argument
    :return: correct argument
    """
    if not os.path.isdir(arg):
        parser.error("The dir {} does not exists!".format(arg))
    else:
        return arg


def is_positive_int(parser, arg):
    """
    Check that arg is positive integer
    :param parser: parser command line arguments
    :param arg: command line argument
    :return: correct argument
    """
    if not arg.isdigit() or not int(arg) > 0:
        parser.error("N must be positive integer!")
    else:
        return int(arg)
