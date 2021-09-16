from sys import argv

script, filepath = argv

input = open(filepath)
indata = input.read()

vowels_spaces = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U', ' ']

result = []
for char in indata:
    print(char)
    if char not in vowels_spaces:
        result.append(char)

input.close()

result.sort()
print(result)

# bonus
set_result = set(result)
result = list(set_result)
result.sort()
print(result)