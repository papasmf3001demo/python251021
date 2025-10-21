# 이메일 검사 예제 (Python)
import re

# 로컬파트 정규식 설명:
# - (?!\.)                          : 문자열 시작 직후 마침표가 오지 않도록 막음 (선행 점 금지)
# - ( (?!.*\.\.) ... )              : 내부에서 연속된 마침표("..")가 없도록 하는 전방부정탐색 포함
# - [A-Za-z0-9!#$%&'*+/=?^_`{|}~.-] : 로컬파트에서 허용하는 문자들(영숫자, 일부 특수문자, 점 포함)
# - {1,64}                          : 로컬파트 길이 제한 (최대 64자; RFC 권장에 근거한 실무 제한)
# - (?<!\.)                         : 로컬파트 끝이 마침표가 아닌지 확인 (후행 점 금지)
# 전체: 선행점/후행점 금지, 연속점 금지, 허용 문자 및 길이 제한 적용
_local = r"(?!\.)((?!.*\.\.)[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]{1,64})(?<!\.)"

# 도메인 정규식 설명:
# 기본 아이디어: 도메인은 라벨( label1.label2...TLD ) 구조
# 각 라벨 규칙:
# - [A-Za-z0-9]                              : 라벨은 알파뉴메릭으로 시작
# - (?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?       : 라벨의 중간(최대 61자)에는 하이픈 허용, 마지막은 알파뉴메릭 (라벨 길이 최대 63)
# 도메인 전체:
# - (?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)* : 추가 하위 라벨들(점으로 구분, 0개 이상)
# - \.[A-Za-z]{2,}                               : 최종 최상위 도메인(TLD)은 점 다음에 최소 2글자의 알파벳
# 주의: 이 패턴은 국제화 도메인(ACE/유니코드)과 인용된 로컬파트 등은 처리하지 않음
_domain = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*\.[A-Za-z]{2,}"

# 전체 패턴: 로컬파트@도메인 으로 전체 매치
EMAIL_RE = re.compile(rf"^{_local}@{_domain}$", re.IGNORECASE)

def is_valid_email(email: str) -> bool:
    """이메일 형식 검사
    - 반환값: 형식이 맞으면 True, 아니면 False
    - 주의: RFC의 모든 특수 케이스(예: 큰따옴표로 묶인 로컬파트, 공백/주석, IDN)는 이 간단한 검사로 모두 판별되지 않음.
    """
    return bool(EMAIL_RE.match(email))

# 샘플 이메일 (10개)
samples = [
    "simple@example.com",
    "very.common@example.com",
    "disposable.style.email.with+symbol@example.com",
    "user_name-100@example.co.uk",
    "user.name+tag+sorting@example.com",
    "plainaddress",
    "@missing-local.org",
    "username@example,com",
    "username@.com",
    "username@-example.com"
]

if __name__ == "__main__":
    for e in samples:
        print(f"{e:40} -> {is_valid_email(e)}")