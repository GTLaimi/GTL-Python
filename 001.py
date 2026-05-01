a=int(input('a=' ))
for n in range(2, a):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x,end='\n')
            break
    else:
        print(n, 'is a prime number', end='\n')
