#!/usr/bin/env python3

import sys
import math
import numpy as np

class InvalidFile(Exception):
    def __init__(self, msg):
        print(msg, file=sys.stderr)
        Exception.__init__(self, msg)
        sys.exit(84)

def man_help():
    print(
        """USAGE
        ./109titration file

           DESCRIPTION
        file    a csv file containing "vol;ph" lines
        """
    )

def check_args():
    if ("--help" in sys.argv or "-h" in sys.argv):
        man_help()
        sys.exit(0)
    if (len(sys.argv) != 2):
        print("See -h or --help for help", file=sys.stderr)
        sys.exit(84)

def my_math(tab):
    pns = 0.0
    derv = [0] * len(tab)
    k = 0
    s = 1
    print("Derivative:")
    for i in range(1, len(tab) - 1):
        derv[i] = (tab[i + 1][1] - tab[i - 1][1]) / (tab[i + 1][0] - tab[i - 1][0])
        print("%.1f ml -> %.2f" % (tab[i][0], derv[i]))
        if pns < derv[i]:
            pns = derv[i]
            s = tab[i][0]
            k = i
    print("\nEquivalence point at %.1f ml\n" % s)
    print("Second derivative:")
    for i in range(1, len(derv) - 3):
        p = (derv[i + 2] - derv[i]) / (tab[i + 2][0] - tab[i][0])
        print("%.1f ml -> %.2f" % (tab[i + 1][0], p))
    print("\nSecond derivative estimated:")
    r = s
    e = 0
    if k - 2 < 0:
        i = tab[k - 1][0]
        p = v1 = 0
    else:
        i = tab[k - 1][0]
        p = v1 = (derv[k] - derv[k - 2]) / (tab[k][0] - tab[k - 2][0])
    v2 = (derv[k + 1] - derv[k - 1]) / (tab[k + 1][0] - tab[k - 1][0])
    z = (v2 - v1) / (10 * (tab[k][0] - tab[k - 1][0]))
    while i - 0.05 < tab[k][0]:
        print("%.1f ml -> %.2f" % (i, v1))
        if math.fabs(p) > math.fabs(v1) and k - 1 > 0:
            p = v1
            r = i
        v1 += z
        i += 0.1
    if k + 3 >= len(derv):
        z = -v2 / 10
    else:
        v1 = (derv[k + 2] - derv[k]) / (tab[k + 2][0] - tab[k][0])
        z = (v1 - v2) / (10 * (tab[k + 1][0] - tab[k][0]))
    v2 += z
    while i - 0.05 < tab[k + 1][0]:
        print("%.1f ml -> %.2f" % (i, v2))
        v2 += z
        i += 0.1
        if math.fabs(p) > math.fabs(v2) and k + 3 < len(tab):
            p = v2
            r = i
    print("\nEquivalence point at %.1f ml" % r)
    return derv

def file_in_tab(fd):
    tab = []
    for line in fd:
        try:
            x, y = map(float, line.strip().split(';'))
            tab.append([x, y])
        except ValueError:
            print(f"Invalid line: {line.strip()}", file=sys.stderr)
            sys.exit(84)
    if len(tab) <= 4:
        raise InvalidFile("Not enough data in file")
    return tab

def main():
    check_args()
    try:
        with open(sys.argv[1]) as fd:
            tab = file_in_tab(fd)
        if (len(tab) <= 4):
            raise InvalidFile("Not enough data in file")
    except (PermissionError, FileNotFoundError) as e:
        print(e, file=sys.stderr)
        sys.exit(84)
    else:
        tab = np.array(tab)
        my_math(tab)

if __name__ == '__main__':
    main()
    sys.exit(0)
