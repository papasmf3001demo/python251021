# 문자열처리.py 

strA = "python is very powerful"
strB = "파이썬은 강력해"

print(len(strA))  # 영문 문자열 길이 출력
print(len(strB))  # 한글 문자열 길이 출력
print(strA.upper())  # 영문 문자열 대문자로 변환
print(strA.capitalize())  # 영문 문자열 첫 글자만 대문자로 변환
print(strB.replace("강력해", "매우 강력해"))  

data = "<<<< spam and ham >>>" 
result = data.strip("<> ")  # 문자열 양쪽의 특정 문자 제거
print(data)
print(result)  # 결과 출력

#문자열을 리스트로 변환 
lst = result.split()
print(lst)  # 리스트 출력
#다시 하나로 합치기 
print(":)".join(lst))  # 리스트를 문자열로 합쳐 출력

#정규표현식: 특정한 문자열 패턴 검색 
import re

result = re.search("apple", "apple and banana")
print(result)  # 검색 결과 출력
print(result.group())  # 매치된 문자열 출력

result = re.search("\d{4}", "올해는 2025년입니다.")
print(result)  # 검색 결과 출력
print(result.group())  # 매치된 문자열 출력

result = re.search("\d{5}", "우리 동네는 51000입니다.")
print(result)  # 검색 결과 출력
print(result.group())  # 매치된 문자열 출력

