import os
import requests
from dotenv import load_dotenv
from rest_framework import status

load_dotenv()

# OTP Settings
api_url = "http://api.greenweb.com.bd/api.php"
token = os.getenv("OTP_TOKEN")


def send_otp(receiver, otp_num):
    try:
        response = requests.post(
            api_url,
            data={
                "token": token,
                "to": receiver,
                "message": f"{otp_num} is your Password Reset Code",
            },
        )
        return {
            "status": response.status_code,
            "message": response.text
        }
    except Exception as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }
