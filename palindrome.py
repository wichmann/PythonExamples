#!/usr/bin/env python3

"""
Erkennung von Palindromen

@author: Christian Wichmann
"""

def stripDown(string):
    return "".join(filter(str.isalnum, string.lower()))

if __name__ == "__main__":
    
    print("Palindromerkennung...")
    text = str(input("Bitte Text eingeben: "))
    
    if stripDown(text) == stripDown(text[::-1]):
        print("Palindrom")
    else:
        print("Kein Palindrom")

