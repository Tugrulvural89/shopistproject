# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('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'))
from_email = Email("tugrulv89@gmail.com")
to_email = Email("tugrulv89@gmail.com")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)