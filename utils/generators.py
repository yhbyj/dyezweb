# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/1 7:47'

from random import choice


def generate_code(digits=4):
    """随机生成digits位数字码"""
    seeds = '1234567890'
    numbers = []
    for i in range(digits):
        numbers.append(choice(seeds))
    return ''.join(numbers)
