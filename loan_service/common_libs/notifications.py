import os

USE_MOCK = os.getenv("USE_MOCK_EMAILS", "true").lower() == "true"

def send_email(to: str, subject: str, body: str):
    if USE_MOCK:
        print(f"📧 [MOCK EMAIL] To: {to}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
    else:
        # Later: real implementation using boto3 or SMTP
        raise NotImplementedError("Real email sending not implemented")

