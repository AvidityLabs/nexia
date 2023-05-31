import firebase_admin
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError, ExpiredIdTokenError

import os
import firebase_admin
from firebase_admin import credentials

# This is just for tesing purposes 
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "andika-16cf6",
    "private_key_id": "fc5f034bea9b8196d73e062127495b9b55bfe21d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMN5HCoz2wCDhx\n7YsNDiam6pMROGpqu3pGa7pVlENyvMaRPZwTmzN638KSb+sSJBY0BpVbGfDSIsLP\nwEYYgNb8TLJLr7toA0/oSjdTOrpRe2K5zFmDaB/bXFdZDJl7L01QXZ8tNPnN3Q9B\n8HGoqzJP7KRXllHbK3y/HWht5JvyX6gOZQkCTLjzmbntD398tuItjbaHgRK+96wU\n5Xp0y5IfQkFaIqzh0A8EMvjnwhgxbcyyx5oYYcmlQGkPd0MzOz0Ui8a6D4CPKaN4\nqTwJG7LABq+u0RM73CnoILYOpSBpnhgiELKXEJ7W2aBYMUnwjLo+EhK3rnAnJT1u\n5aUjKNRTAgMBAAECggEAEb+FZ8ZavtKprF99LyH7ApTh02RoSnHHUDLeBScECTo8\nnA3TMGVtWKRbjoqy6HPOopatFbeDVV5XbC/LlI1jlPzJ0a5Q2fRqIu5XfZPEJcwh\nfRoavQ/Or17vA0Dtkj+lQ/+tYFC5olMWfhNHOLLCn7ozLdHu6xHaxYKCrp5O97lO\nj7K3iDqnzV0RfJrHHp69lTI3GiLwf+fwh6ElDUuKu2WoPdnmUYewmLl1uKG89Sag\nQNxFF5mXkkq0Uu9I+2gFiFXIEkjLjlGh7baCndD76QR8v0g7TbWZR0JSVdN1yihK\n+sIPk4nUl0cAmQpx5/zU4Tqq3tJuI4sw2x//ZEzdgQKBgQDrN242EwZQSZlgnmUw\nuRlm3uvFXYbn3Are1qCdesq53RvEF6FE2FUfhAdxsCRBF36xcFE1EJCcz8FcE2q7\nUXCuSkNLmomOUnu8j7Le713YFHaEeLLNsRTnQBqIoA/sC4y9ptL3RYkUW1eT3MD4\nCxb6fAEBzHx2vDPBlTzIxKQ9gQKBgQDeQu9TWS2EKCPBVPtXDomqLg0aUsgws06o\nLpfJBe6q1FxcLK2CSxMF9IPj7ZnbxY6pJ8SUpwIZsAe9iAwDXhb6YBRDHgKSOzk7\nqJNAY0KUPnFjASVHhuGk83iGe1D4lpahdm9Aewco6tulRlnTpBodPlBT7xi1Ebpw\nLnYwDyGj0wKBgQCFIRFy75+iL5Xs9pmlUw6Kh9+ADKh/cK6CY43ys/4r5naBrTIs\nyhibxtmDwkMyyD5/5WdBFogTCQ+Ssra1IKobK5MdJnF2qT65gcemoGpIE4TlA3+I\nJhMDs+eQrq90VTEqYlKDe8rTR8Owv8BEY9p0mVzkjL1hYrIUfggyRgIDgQKBgCBN\nkCUIAAKGJvQxWrpDZaSzPrpFr8zMMrFk3DCeSRrQ9H99Cta1/JTP/d9BqCv14Y8a\nNYr5XufG2skkHcLbiPFox2kd0nfYXbAbBxPDmWicTrR59SYZJ3Bm5mx9Pb5zfH8J\nDJBNkTPUNool2GZXImh/pwMb6/ZdFkC5r/m6KUR7AoGAVbD3mRc0GGl/CnHXdxGr\nzTIb9Cr5Z1tBsNVbJ3SWlcLo9wG0EceHjodaSwF6UZ6OKpZViEO6hNYjCPfTc6LM\ncCmFi6DeBQHwFlFtofCjjIZednWmMNGG3u2fIs07jdk9jWMSOJG+/nFSziWBqt9Y\nQzu94Tkrl5VOHv/pfoxyJiU=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-c1hdv@andika-16cf6.iam.gserviceaccount.com",
    "client_id": "101959690551443820822",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-c1hdv%40andika-16cf6.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
)

default_app = firebase_admin.initialize_app(cred)


def firebase_validation(id_token):
    """
    This function receives id token sent by Firebase and
    validate the id token then check if the user exist on
    Firebase or not if exist it returns True else False
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        provider = decoded_token['firebase']['sign_in_provider']
        image = None
        name = None
        sub = None
        aud = None
        email_verified = None

        if "name" in decoded_token:
            name = decoded_token['name']
        if "picture" in decoded_token:
            image = decoded_token['picture']
        if "sub" in decoded_token:
            sub = decoded_token['sub']
        if "aud" in decoded_token:
            aud = decoded_token['aud']
        if "email_verified" in decoded_token:
            email_verified = decoded_token['email_verified']
        try:
            user = auth.get_user(uid)
            email = user.email
            if user:
                return {
                    "is_verified": email_verified,
                    "uid": uid,
                    "sub": sub,
                    "aud": str(aud.replace(' ', '')),
                    "email": email,
                    "display_name": name,
                    "auth_provider": provider,
                    "photo_url": image
                }
            else:
                return False
        except UserNotFoundError:
            print("user not exist")
    except ExpiredIdTokenError:
        print("invalid token")
