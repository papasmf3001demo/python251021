# demoIndexing.py 

strA = '파이썬은 강력해'
strB = "python is very powerful"
strC = """이 문자열은
다중 라인으로
저장되어있음"""

print(strA)
print(strB)
print(strC)

#슬라이싱
print(strA[0])
print(strA[1])
print(strA[0:3])
print(strA[:3])
print(strA[-2:])

print("---리스트 연습---")
colors = ["red", "blue", "green"]
print(len(colors))
print(colors[0])
colors.append("white")
colors.insert(1, "pink")
print(colors)
#삭제 
colors.remove("red")
#정렬
colors.sort() 
print(colors)
colors.reverse()
print(colors)
