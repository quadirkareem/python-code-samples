#!/usr/bin/env python 
# -*- coding: utf-8 -*-

def psychologist():
    print('Please tell me your problems')
    while True:
        answer = (yield)
        if answer is None:
            print("Speak up!!!")
        else:
            if answer.endswith('?'):
                print("Don't ask yourself too much questions")
            elif 'good' in answer:
                print("Ahh that's good, go on")
            elif 'bad' in answer:
                print("Don't be so negative")

"""
free = psychologist()

next(free)
next(free)
next(free)
"""