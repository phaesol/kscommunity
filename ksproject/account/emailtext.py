# 이메일 발송 메시지
def message(domain, uidb64, token):
    return "아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://54.146.176.46//account/activate/{}/{}\n\n환영합니다!".format(uidb64, token)