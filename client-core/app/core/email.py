from msal import ConfidentialClientApplication
import httpx
from app.core.config import settings

TENANT_ID = settings.MS_TENANT_ID
CLIENT_ID = settings.MS_CLIENT_ID
CLIENT_SECRET = settings.MS_CLIENT_SECRET
SENDER_EMAIL = settings.MS_SENDER_EMAIL

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]


def get_access_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    raise Exception("Could not get access token: " + str(result))


def get_otp_email_template(otp: str) -> str:
    return f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html dir="ltr" lang="en">
  <head>
    <link
      rel="preload"
      as="image"
      href="https://images.squarespace-cdn.com/content/v1/67a18576b339e24b3ee29e8b/90727173-89d2-4b90-9253-3ec9a8bf1146/STRATOS--CYBER+INC+LOGO.jpg" />
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <meta name="x-apple-disable-message-reformatting" />
    <!--$-->
  </head>
  <body
    style="background-color:#ffffff;font-family:HelveticaNeue,Helvetica,Arial,sans-serif">
    <table
      align="center"
      width="100%"
      border="0"
      cellpadding="0"
      cellspacing="0"
      role="presentation"
      style="max-width:360px;background-color:#ffffff;border:1px solid #eee;border-radius:5px;box-shadow:0 5px 10px rgba(20,50,70,.2);margin-top:20px;margin:0 auto;padding:68px 0 130px">
      <tbody>
        <tr style="width:100%">
          <td>
            <img
              alt="Metatron"
              height="88"
              src="https://images.squarespace-cdn.com/content/v1/67a18576b339e24b3ee29e8b/90727173-89d2-4b90-9253-3ec9a8bf1146/STRATOS--CYBER+INC+LOGO.jpg"
              style="display:block;outline:none;border:none;text-decoration:none;margin:0 auto"
              width="auto" />
            <p
              style="font-size:11px;line-height:16px;margin-bottom:16px;margin-top:16px;color:#437171;font-weight:700;font-family:HelveticaNeue,Helvetica,Arial,sans-serif;height:16px;letter-spacing:0;margin:16px 8px 8px 8px;text-transform:uppercase;text-align:center">
              Verify Your Identity
            </p>
            <h1
              style="color:#000;display:inline-block;font-family:HelveticaNeue-Medium,Helvetica,Arial,sans-serif;font-size:20px;font-weight:500;line-height:24px;margin-bottom:0;margin-top:0;text-align:center">
              Please use the code below for account verification
            </h1>
            <table
              align="center"
              width="100%"
              border="0"
              cellpadding="0"
              cellspacing="0"
              role="presentation"
              style="background:rgba(0,0,0,.05);border-radius:4px;margin:16px auto 14px;vertical-align:middle;width:280px">
              <tbody>
                <tr>
                  <td>
                    <p
                      style="font-size:32px;line-height:40px;margin-bottom:16px;margin-top:16px;color:#000;font-family:HelveticaNeue-Bold;font-weight:700;letter-spacing:6px;padding-bottom:8px;padding-top:8px;margin:0 auto;display:block;text-align:center">
                      {otp}
                    </p>
                  </td>
                </tr>
              </tbody>
            </table>
            <p
              style="font-size:15px;line-height:23px;margin-bottom:16px;margin-top:16px;color:#444;font-family:HelveticaNeue,Helvetica,Arial,sans-serif;letter-spacing:0;padding:0 40px;margin:0;text-align:center;font-weight:600">
              This code is valid for 3 minutes
            </p>
            <br>
            <p
              style="font-size:15px;line-height:23px;margin-bottom:16px;margin-top:16px;color:#444;font-family:HelveticaNeue,Helvetica,Arial,sans-serif;letter-spacing:0;padding:0 40px;margin:0;text-align:center">
              If you didn't request a code, you can ignore this email.
            </p>
          </td>
        </tr>
      </tbody>
    </table>
    <p
      style="font-size:12px;line-height:23px;margin-bottom:16px;margin-top:20px;color:#000;font-weight:800;letter-spacing:0;margin:0;font-family:HelveticaNeue,Helvetica,Arial,sans-serif;text-align:center;text-transform:uppercase">
      Metatron by Stratos Cyber Inc.
    </p>
    <!--/$-->
  </body>
</html>
"""

def get_reset_password_otp_email_template(otp: str) -> str:
    return f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html dir="ltr" lang="en">
  <head>
    <link
      rel="preload"
      as="image"
      href="https://images.squarespace-cdn.com/content/v1/67a18576b339e24b3ee29e8b/90727173-89d2-4b90-9253-3ec9a8bf1146/STRATOS--CYBER+INC+LOGO.jpg" />
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <meta name="x-apple-disable-message-reformatting" />
    <!--$-->
  </head>
  <body
    style="background-color:#ffffff;font-family:HelveticaNeue,Helvetica,Arial,sans-serif">
    <table
      align="center"
      width="100%"
      border="0"
      cellpadding="0"
      cellspacing="0"
      role="presentation"
      style="max-width:360px;background-color:#ffffff;border:1px solid #eee;border-radius:5px;box-shadow:0 5px 10px rgba(20,50,70,.2);margin-top:20px;margin:0 auto;padding:68px 0 130px">
      <tbody>
        <tr style="width:100%">
          <td>
            <img
              alt="Metatron"
              height="88"
              src="https://images.squarespace-cdn.com/content/v1/67a18576b339e24b3ee29e8b/90727173-89d2-4b90-9253-3ec9a8bf1146/STRATOS--CYBER+INC+LOGO.jpg"
              style="display:block;outline:none;border:none;text-decoration:none;margin:0 auto"
              width="auto" />
              
               <p
              style="font-size:11px;line-height:16px;margin-bottom:16px;margin-top:16px;color:#437171;font-weight:700;font-family:HelveticaNeue,Helvetica,Arial,sans-serif;height:16px;letter-spacing:0;margin:16px 8px 8px 8px;text-transform:uppercase;text-align:center">
              Verify Your Identity
            </p>
           
             <h1
              style="color:#000;display:inline-block;font-family:HelveticaNeue-Medium,Helvetica,Arial,sans-serif;font-size:20px;font-weight:500;line-height:24px;margin-bottom:0;margin-top:0;text-align:center; padding: 8px">
              Please use the code below for Email verification
            </h1>
            <table
              align="center"
              width="100%"
              border="0"
              cellpadding="0"
              cellspacing="0"
              role="presentation"
              style="background:rgba(0,0,0,.05);border-radius:4px;margin:16px auto 14px;vertical-align:middle;width:280px">
              <tbody>
                <tr>
                  <td>
                    <p
                      style="font-size:32px;line-height:40px;margin-bottom:16px;margin-top:16px;color:#000;font-family:HelveticaNeue-Bold;font-weight:700;letter-spacing:6px;padding-bottom:8px;padding-top:8px;margin:0 auto;display:block;text-align:center">
                      {otp}
                    </p>
                  </td>
                </tr>
              </tbody>
            </table>
            <p
              style="font-size:15px;line-height:23px;margin-bottom:16px;margin-top:16px;color:#444;font-family:HelveticaNeue,Helvetica,Arial,sans-serif;letter-spacing:0;padding:0 40px;margin:0;text-align:center;font-weight:600">
              This code is valid for 1 minutes
            </p>
            <br>
            <p
              style="font-size:15px;line-height:23px;margin-bottom:16px;margin-top:16px;color:#444;font-family:HelveticaNeue,Helvetica,Arial,sans-serif;letter-spacing:0;padding:0 40px;margin:0;text-align:center">
              If you didn't request a code, you can ignore this email.
            </p>
          </td>
        </tr>
      </tbody>
    </table>
    <p
      style="font-size:12px;line-height:23px;margin-bottom:16px;margin-top:20px;color:#000;font-weight:800;letter-spacing:0;margin:0;font-family:HelveticaNeue,Helvetica,Arial,sans-serif;text-align:center;text-transform:uppercase">
      Metatron by Stratos Cyber Inc.
    </p>
    <!--/$-->
  </body>
</html>
"""


async def send_email(recipient_email: str, subject: str, content: str):
    access_token = get_access_token()
    email_msg = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": content,
            },
            "from": {
                "emailAddress": {
                    "name": "Metatron Notification",
                    "address": SENDER_EMAIL,
                }
            },
            "toRecipients": [{"emailAddress": {"address": recipient_email}}],
        },
        "saveToSentItems": "false",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL}/sendMail",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json=email_msg,
        )

    if response.status_code >= 400:
        raise Exception(f"Failed to send email: {response.status_code} {response.text}")
    return True


async def send_otp_email(recipient_email: str, otp: str):
    subject = "Your Metatron account verification code"
    content = get_otp_email_template(otp)
    return await send_email(recipient_email, subject, content)


async def send_reset_password_otp_email(recipient_email: str, otp: str):
    subject = "Verification code to Reset Password"
    content = get_reset_password_otp_email_template(otp)
    return await send_email(recipient_email, subject, content)
