import sendgrid
from agents import Agent, function_tool
from sendgrid.helpers.mail import Content, Email, Mail, To

from src.config import load_settings
from src.prompts import EMAIL_AGENT_INSTRUCTIONS

settings = load_settings()


@function_tool
def send_email(subject: str, html_body: str) -> str:
    """Send an email with the given subject and HTML body."""
    sg = sendgrid.SendGridAPIClient(api_key=settings.sendgrid_api_key)
    from_email = Email(settings.sender_email)
    to_email = To(settings.recipient_email)
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    return "success"


email_agent = Agent(
    name="Email Agent",
    instructions=EMAIL_AGENT_INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
