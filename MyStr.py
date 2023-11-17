#!/usr/local/bin/python

import string


def atoi(src):
    print("Atoi ", src)
    if src.isdigit():
        return string.atoi(src)
    else :
        print("Atoi Error no number")
        return 0


def atof(src):
    print("Atof ", src)
    return string.atof(src)
