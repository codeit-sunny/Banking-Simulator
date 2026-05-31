import gmail

email = " "  # please enter your email hear
password = " " # please enter your email password here

def openacn_mail(to,text):
    con=gmail.GMail(email,password)
    msg=gmail.Message(to=to, subject = "Account Opend in ABC Bank",text=text)
    con.send(msg)

def closeotp_mail(to,text):
    con=gmail.GMail(email,password)
    msg=gmail.Message(to=to, subject = "OTP to close account",text=text)
    con.send(msg)

def forgototp_mail(to,text):
    con=gmail.GMail(email,password)
    msg=gmail.Message(to=to, subject = "OTP to recover password",text=text)
    con.send(msg)