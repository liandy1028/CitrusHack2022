import math as m


print('Hello World!')

x = 10

print(x)
print(type(x))

x = 'Hello'

print(x)
print(type(x))

x = x + 'world'

print(x) 

x = 5
y = 10

z = max(x, y)
print(z) 

def sayHello(name):
    print(f'Hello {name}!')

sayHello('Joe')    

li = [1, 2, 3]

print(li)

li = list(range(100))

print(li)

print(li[30:-2])

vec = [1, 2, 3, 'one', 'two']

i = 0
while i < 10: 
    print(i)
    i += 1

print()
for j in range(7,12):
    print(j)

# if condition == something:
#     code()

# elif condition2:
#     code()

# else:
#     more_code()

print()
print(m.factorial(5))