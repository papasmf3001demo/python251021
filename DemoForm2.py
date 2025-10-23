# DemoForm2.py 
# DemoForm2.ui(화면단) + DemoForm2.py(로직단) 구성된 예제
import sys 
from PyQt5.QtWidgets import * 
from PyQt5 import uic
#웹사이트 요청
import urllib.request
#크롤링 
from bs4 import BeautifulSoup
#정규표현식: 특정 문자열 패턴 찾기
import re


#디자인 파일을 로딩(파일명을 수정) 
form_class = uic.loadUiType("DemoForm2.ui")[0]

#폼 클래스를 정의(QMainWindow 상속)
class DemoForm(QMainWindow, form_class): 
    def __init__(self): 
        super().__init__() 
        self.setupUi(self) 
    #슬롯메서드 추가
    def firstClick(self):
        #파일에 저장
        f = open("clien.txt", "wt", encoding="utf-8")
        for n in range(0,10):
            url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(n)
            print(url)
            #페이지 실행 결과 
            data = urllib.request.urlopen(url).read()
            #검색이 용이한 객체 
            soup = BeautifulSoup(data, 'html.parser')
            list = soup.find_all("span", attrs={"data-role":"list-title-text"})
            for item in list:
                title = item.text.strip()
                print(title)
                f.write(title + "\n")
        f.close()
        self.label.setText("클리앙 중고장터 크롤링 완료")
    def secondClick(self):
        self.label.setText("두번째 버튼을 클릭함")
    def thirdClick(self):
        self.label.setText("세번째 버튼 클릭했음~~")

#진입점을 체크 
if __name__ == "__main__": 
    #먼저 실행 프로세스를 만들고 
    app = QApplication(sys.argv) 
    #위에서 정의한 폼을 생성
    demoForm = DemoForm() 
    #화면에 보여주기 
    demoForm.show() 
    #대기하면서 이벤트 처리하기 
    sys.exit(app.exec_())
