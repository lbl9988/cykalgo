# !/usr/bin/env python2

import ast
import sys
import itertools
import os.path
from sets import Set
from string import punctuation


def read_grammar(filename):

    # construct terminal set T and production rules R
    T = Set([])
    R = {}
    if(os.path.isfile(filename)):
        grammar_file = open(filename, 'r')
        for line in grammar_file:
            content_line = line[:-1]  # trim the newline character
            if content_line[-1] == ' ':
                words = content_line.split()
                T.add(words[-1])

            words = line.split()
            key = words[0]
            value = words[-1]
            if key in R.keys():
                R[key].append(value)
            else:
                R[key] = [value]
    else:
        print 'File ', filename, 'not found.'
    #print T, R
    return [T, R]


def compute_V1(V2, V3):

    V1 = []
    #print V2, V3
    if not V2:
        V1 = V3
    elif not V3:
        V1 = V2
    else:
        #print "computing....", V2, V3
        for i in range(len(V2)):
            for j in range(len(V3)):
                v2 = V2[i]
                v3 = V3[j]
                #print v2, v3
                v1 = v2+v3
                V1.append(v1)

    #print "compute_V1 =", V1
    return V1


def lookup_leftside(rhs, rules):

    lhs = []
    for item in rhs:
        for key in rules.keys():
            if item in rules[key]:
                lhs.append(key)
    return lhs


def print_table(M):

    rowNum = len(M)
    colNum = len(M[0])
    for i in range(rowNum):
        for j in range(colNum):
            if not M[i][j]:
                sys.stdout.write('Empty ')
            else:
                sys.stdout.write(str(M[i][j]) + '  ')
        sys.stdout.write('\n')


def process_terminals(input_string, Terminals, rules):

    words = input_string.split()
    for word in words:
        if word not in Terminals:
            return False

    variables = []
    for i in range(len(words)):
        variable = []
        for key in rules.keys():
            if words[i] in rules[key]:
                variable.append(key)
        variables.append(variable)

    perm = [' '.join(s) for s in itertools.product(*variables)]
    return perm


def cyk(rules, words):

    ret = False
    items = words.split()

    # initialize a nxn table
    n = len(items)
    Matrix = [[[] for x in xrange(n)] for x in xrange(n)]

    for j in range(n):
        Matrix[0][j] = items[j]

    #print_table(Matrix)

    for i in range(1, n):
        for j in range(0, n-i):
            #print 'inspecting entry (', i, ',', j, ')'
            entry = []
            k = 0
            while k < i:
                V2 = Matrix[k][j]
                V3 = Matrix[i-k-1][j+k+1]
                V1 = compute_V1(V2, V3)
                lhs = lookup_leftside(V1, rules)
                #print 'lhs =', lhs
                entry = entry + lhs
                k = k + 1
            #print 'entry=', entry
            Matrix[i][j] = entry

    print_table(Matrix)

    finalEntry = Matrix[n-1][0]
    if finalEntry:
        ret = True

    return ret


if __name__ == '__main__':

    grammar_file = sys.argv[1]
    [terminal_set, rules] = read_grammar(grammar_file)

    input_string = sys.argv[2]
    input_string = input_string.lower()
    for p in list(punctuation):
        input_string = input_string.replace(p, '')
    #print input_string

    tokens = process_terminals(input_string, terminal_set, rules)
    #print tokens
    if not tokens:
        print 'no'
    else:
        result = False
        for i in range(len(tokens)):
            #print cyk(rules, tokens[i])
            result = result or cyk(rules, tokens[i])
        if result:
            print 'yes'
        else:
            print 'no'
