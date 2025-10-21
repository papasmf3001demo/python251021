#개발자 클래스를 정의 
class Developer:
    def __init__(self, name, language):
        self.name = name
        self.language = language

    def introduce(self):
        return f"안녕하세요, 저는 {self.name}이고 주로 {self.language}를 사용합니다."
    
class WebDeveloper(Developer):
    def __init__(self, name, language, framework):
        super().__init__(name, language)
        self.framework = framework

    def introduce(self):
        base_intro = super().introduce()
        return f"{base_intro} 그리고 저는 {self.framework} 프레임워크를 사용합니다."
    
#인스턴스를 생성
dev = WebDeveloper("철수", "Python", "Django")
print(dev.introduce())
dev2 = Developer("영희", "JavaScript")
print(dev2.introduce())
 

