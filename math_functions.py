#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from random import randint
#import matplotlib.pyplot as plt
from math import sqrt, pi, e

"""
def plot_dataset(style="point", set1="", set2=""):
    plt.cla()
    plt.clf()
    set1 = set1.split()
    set2 = set2.split()
    for i in range(0, len(set1)):
        set1[i] = int(set1[i])
    for i in range(0, len(set2)):
        set2[i] = int(set2[i])
    if len(set1) != len(set2):
        return "length"

    for i in set1:
        if type(i) is not int:
            return "datatype"
    for i in set2:
        if type(i) is not int:
            return "datatype"

    if style == "point":
        plt.plot(set1, set2, 'ro')

    elif style == "line":
        plt.plot(set1, set2, color="red", linestyle="solid")

    elif style == "dash":
        plt.plot(set2, set2, 'r--')

    imagename = "imagesaving/" + str(randint(1000000000, 9999999999)) + ".png"
    plt.savefig(imagename)
    return imagename
"""

def cosdeg(number):
    return round(math.cos(math.radians(number)), 6)


def cos(number):
    return round(math.cos(number), 6)


def sindeg(number):
    return round(math.sin(math.radians(number)), 6)


def sin(number):
    return round(math.sin(number), 6)


def tandeg(number):
    return round(math.tan(math.radians(int(number))), 6)


def tan(number):
    return round(math.tan(number), 6)


def acosdeg(number):
    return round(math.acos(number) * (180/math.pi), 6)


def acos(number):
    return round(math.acos(number), 6)


def asindeg(number):
    return round(math.asin(number) * (180/math.pi), 6)


def asin(number):
    return round(math.asin(number), 6)


def atandeg(number):
    return round(math.atan(number) * (180/math.pi), 6)


def atan(number):
    return round(math.atan(number), 6)


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)


def math_function(*args):
    inputtext = ""
    outputtext = ""
    for i in args:
        inputtext += i
    for i in inputtext:
        if i == "^":
            outputtext += "**"
        else:
            outputtext += i
    try:
        outputtext = eval(outputtext)
        outputtext = str(outputtext)
    except:
        return None
    if outputtext[-2:] == ".0":
        outputtext = outputtext[:-2]
    return outputtext
