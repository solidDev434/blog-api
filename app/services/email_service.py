from fastapi import status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse
from app.core.settings import settings
from app.schemas.email_schema import EmailSchema

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USER,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_SERVER=settings.MAIL_HOST,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS
)


async def send_mail(to_email: EmailSchema, body: str, subject: str):
    message = MessageSchema(
        subject=subject,
        recipients=to_email,
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": [f"Email has been sent to {x}" for x in to_email]})


async def send_verify_mail(email: str, token):
    html = f"""
        <a href='{settings.SERVER_URL}/{token}'>{settings.SERVER_URL}/{token}</a>
        <p>{token}</p>
    """

    subject = "Verify your mail"

    return await send_mail([email], html, subject)
