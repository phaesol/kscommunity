import six
from six import text_type  # pip install six -- django 3.x.x 버전부터 지원 안해줘서 설치 필요
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# user 의 pk + time + is_active (활성화 상태) 가지고 합쳐서 token 생성
class AccountActivationsTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp)) + six.text_type(user.is_active)
        #text_type : 유니코드 정수로부터 유니코드 문자열 가져옴. 
account_activation_token = AccountActivationsTokenGenerator()

