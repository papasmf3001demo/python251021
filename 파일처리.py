# 파일처리.py 

#파일 쓰기 
f = open("demo.txt", "wt", encoding="utf-8")  # 쓰기 모드로 파일 열기
f.write("첫번째\n두번째\n세번째\n")  # 파일에 내용 쓰기
f.close()  # 파일 닫기

#파일 읽기
f = open("demo.txt", "rt", encoding="utf-8")  # 읽기 모드로 파일 열기
result = f.read()  # 파일 내용 읽기
print(result)  # 읽은 내용 출력
f.close()  # 파일 닫기

