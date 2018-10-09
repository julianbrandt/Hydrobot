#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from random import randint
#import matplotlib.pyplot as plt
import numpy as np
import ast
from numpy import cos, sin, tan, arccos, arcsin, arctan
from scipy.optimize import fmin
from math import sqrt, pi, e



def input_auth(string):
    accepted_list = ['x', 'e', 'pi', 'PI', 'sqrt', 'cos', 'sin', 'tan', 'arccos', 'arcsin', 'arctan']
    characters = ['a', 'b', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_', '#', '&']
    for i in range(0, len(string)):
        checkword = ""
        if string[i] in characters:
            checkword += string[i]
            for j in range(1, 6, 1):
                try:
                    if j <= len(string)-i:
                        if string[i+j] in characters:
                            checkword += string[i+j]
                        else:
                            break
                except:
                    break
            for j in range(1, 6, 1):
                try:
                    if j <= i:
                        if string[i-j] in characters:
                            checkword = string[i-j] + checkword
                        else:
                            break
                    else:
                        break
                except:
                    break

        if checkword not in accepted_list and checkword != "":
            return False
    return True

"""
def input_func(func, minrange, maxrange):
    auth = input_auth(func)
    if not auth:
        return "error"

    minrange = int(minrange)
    maxrange = int(maxrange)

    plt.cla()
    plt.clf()

    outputfunc = ""
    for i in func:
        if i == "^":
            outputfunc += "**"
        else:
            outputfunc += i

    def mathfunction(x):
        return eval(outputfunc)

    try:
        scaling = (maxrange/minrange)/100
        if scaling < 0:
            scaling = -scaling
    except:
        return "error"

    x1 = np.arange(minrange, maxrange, scaling)
    plt.plot(x1, mathfunction(x1), color="red", linestyle="solid")

    imagename = "imagesaving/" + str(randint(1000000000, 9999999999)) + ".png"
    plt.savefig(imagename)
    return imagename


    if minrange is None:
        minrange = -5
        maxrange = 5

    try:
        if maxrange is None and minrange is not None:
            minrange = -int(minrange)
            maxrange = -minrange
    except:
        return "error"
"""