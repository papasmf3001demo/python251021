# 랜덤모듈.py 
import random

print(random.random())
print(random.random())
print(random.uniform(2, 5))
print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])
print(random.sample(range(20), 10))
print(random.sample(range(20), 10))
#로또번호 
print(random.sample(range(1, 46), 5))



