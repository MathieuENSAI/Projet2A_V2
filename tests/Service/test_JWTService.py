import datetime
import pytest
from jwt.exceptions import ExpiredSignatureError
from freezegun import freeze_time
from src.Service.JWTService import JwtService

jwt_service = JwtService("mysecret")

@freeze_time("2024-11-16 12:00:00")
def test_encode_jwt():
    user_id = 5
    jwtResponse = jwt_service.encode_jwt(user_id=user_id)
    assert (
        jwtResponse.access_token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1LCJleHBpcnlfdGltZXN0YW1wIjoxNzMxNzYyMDAwLjB9.i7ArehK9XwEMYF_4QaVISIpFJJWld_jh1RffgUOf1hg"
        )


@freeze_time("2024-11-16 12:00:00")
def test_decode_jwt():
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1LCJleHBpcnlfdGltZXN0YW1wIjoxNzMxNzYyMDAwLjB9.i7ArehK9XwEMYF_4QaVISIpFJJWld_jh1RffgUOf1hg"
    decoded_jwt = jwt_service.decode_jwt(jwt)
    assert decoded_jwt.get("user_id") == 5
    assert datetime.datetime.fromtimestamp(decoded_jwt.get("expiry_timestamp")) == datetime.datetime.fromisoformat(
        "2024-11-16 13:00:00"
    )
    
@freeze_time("2024-11-16 12:00:00")
def test_validate_user_jwt():
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1LCJleHBpcnlfdGltZXN0YW1wIjoxNzMxNzYyMDAwLjB9.i7ArehK9XwEMYF_4QaVISIpFJJWld_jh1RffgUOf1hg"
    validate_user_jw = jwt_service.validate_user_jwt(jwt)
    assert validate_user_jw==5

@freeze_time("2024-11-16 12:00:00")
def test_validate_user_jwt_expired():
    expired_token = jwt_service.encode_jwt(user_id=5).access_token
    with freeze_time("2024-11-16 13:01:00"):
        with pytest.raises(ExpiredSignatureError, match="Expired JWT"):
            jwt_service.validate_user_jwt(expired_token)
