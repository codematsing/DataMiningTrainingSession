P = 1500
Y = 3
R = 0.5

n = 12*Y
r = R/(12*100)

Payment = (P*r)/(1-((1+r)**-n))
print(Payment)