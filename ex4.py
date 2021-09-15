_list = [-25, 50, 25, 100]
for x in _list:
    print(x)
    if x > 0 and x < 50:
        print("Positive range")
    elif x < 0 and x > -50:
        print("Negative range")
    elif abs(x) > 50:
        print("Out of range")
    else:
        print("border")