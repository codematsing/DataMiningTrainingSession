from sys import argv
def sum(a,b):
    return a+b

def difference(a,b):
    return a-b

def product(a,b):
    return a*b

def quotient(a,b):
    return a/b

def print_result(a,b):
    print('sum ', sum(a,b))
    print('difference ', difference(a,b))
    print('product ', product(a,b))
    print('quotient ', quotient(a,b))
    
script, a, b = argv
a = int(a)
b = int(b)
print_result(a,b)