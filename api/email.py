#  Radix Analytics Pvt. Ltd
#  Author: Ravi Vasu
#  Created On: 2023-12-27
#  Reviewed By:
#  Last Review Date:
#  Description: This file has Email class.
"""
Change Log
---------------------------------------------------------------------------
Date			Author			Comment
---------------------------------------------------------------------------

"""
# Import System Modules
import logging
import mimetypes
import os

# Import Third-party Python Modules
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string

# Import Project Modules

# Logger variables to be used for logging
info_logger = logging.getLogger('api_info_logger')
error_logger = logging.getLogger('api_db_error_logger')


class Email(object):

    def __init__(self, *args, **kwargs):
        pass

    def send(self, subject, template, data, recipient_email, from_email=None, attachment=None, buffer_attachment=None,
             bcc=None, body_message=None):
        res = 0
        try:
            message = render_to_string(template, data) if body_message is None else body_message
            connection = get_connection()
            messages = []
            if isinstance(recipient_email, str):
                recipient_email = [recipient_email]
            if bcc and isinstance(bcc, str):
                bcc = [bcc]

            for to_email in recipient_email:
                mail = EmailMessage(subject=subject, body=message, from_email=from_email, to=[to_email], bcc=bcc,
                                    connection=connection)
                mail.content_subtype = "html"
                if attachment and len(attachment) > 0 and isinstance(attachment, list):
                    for af in attachment:
                        file_name = os.path.basename(af)
                        file_content = open(af, 'rb').read()
                        mime_type = mimetypes.guess_type(af)[0]
                        mail.attach(file_name, file_content, mime_type)
                if buffer_attachment and isinstance(buffer_attachment, list):
                    for baf in buffer_attachment:
                        mail.attach(baf["file_name"], baf["data"].getvalue(), 'application/octet-stream')
                messages.append(mail)

            res = connection.send_messages(messages)
        except Exception as e:
            print("Error while sending email:", e)
            error_logger.error(e, exc_info=True)
        return res
