#!/usr/bin/env python

# Defines a "repeat" function that takes 2 arguments.
def repeat(s, exclaim):
    """
    Returns the string 's' repeated 3 times.
    If exclaim is true, add exclamation marks.
    """

    result = (s + " ") * 3 
    if exclaim:
        result += '	!!!'
    return result

def main():
    print(repeat('Yay', False))      ## YayYayYay
    print(repeat('Woo Hoo', True))   ## Woo HooWoo HooWoo Hoo!!!
	
    print("hello \
            there")    
    print("""hello 
            there""")
    print('''hello 
            there''')


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()