import json
import smtplib
import glob

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from icu.models import User


def send_email():
    try:
        cred = json.load(open("camera/cred.json", "r"))
    except IOError:
        print("[ERROR] Credentials file not found. No mail sent.")
        return
    users = User.objects.all()
    fromaddr = "server.eng.soft@gmail.com"
    for user in users:
        toaddrs = user.email
        print("[INFO] Emailing to {}".format(user.email))
        text = 'Hey'+user.first_name+', Someone in Your House!!!!'
        subject = 'Security Alert!!'
        message = 'Subject: {}\n\n{}'.format(subject, text)

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddrs
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))

        # set attachments
        files = glob.glob("/tmp/talkingraspi*")
        print("[INFO] Number of images attached to email: {}".format(len(files)))
        for f in files:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)

        # Credentials (if needed) : EDIT THIS
        username = cred["login"]
        password = cred["pass"]

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()
