x_list = [11, 6, 5, 7, 10]
for index,x in enumerate(x_list):
    if x % 2 == 0:
        x_list[index] = x+1
print(x_list)