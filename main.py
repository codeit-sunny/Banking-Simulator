from tkinter import Tk,Label,Frame,Entry, Button, simpledialog,messagebox
from tkinter.ttk import Combobox
import time
import generator
import tables
import mailing
from PIL import Image, ImageTk
import sqlite3
import dbmanager  # ✅ dbmanager import kiya

tables.create_tables()

# ye function clock ke liye jo ek sec pe call hogi 
def update_time():
    datetime = time.strftime("📅 %d-%b-%Y ⏰ %r")
    dt_lbl.configure(text = datetime)
    dt_lbl.after(1000, update_time)

# forgot button pe hit krne ke baad ye screen open hogi 
def forgot_screen():
    frm = Frame(
        root, 
        highlightbackground='black', 
        highlightthickness=1,
        )
    frm.configure(
        bg="pink"
        )
    frm.place(relx=0, rely=.15,relwidth=1,relheight=.78)
    # yaha current frame ko destory kr rhe of phir main screen pe jaa rhe bacause of memory management 
    def back():
        frm.destroy()
        main_screen()


    def send_forgot_otp():
        acn = acn_entry.get()
        email = email_entry.get()

        # ✅ dbmanager se get_name_email use kiya
        tup = dbmanager.get_name_email(acn)
        
        if tup != None:
            otp = generator.forgot_otp()
            text = f"""
            Hello {tup[0]},
            OTP to recover password is = {otp}
            """
            mailing.forgototp_mail(email,text)
            messagebox.showinfo("Forgot","otp send to registered email")
            attempt = 0
            while attempt <= 3:
                attempt += 1
                uotp = simpledialog.askinteger("Forgot","OTP")
                if otp == uotp:
                    # ✅ dbmanager se get_account use kiya
                    acc_data = dbmanager.get_account(acn)
                    messagebox.showinfo("password",acc_data[2])  # pass is at index 2
                    break
                else:
                    messagebox.showerror("Forgot","Invalid otp try  again ")
        else:
            messagebox.showerror("Forgot","Invalid Details")


    # Back Button 
    back_btn = Button (
        frm,
        text="Back",
        font=('Comis San MS', 18, 'bold'),
        bg='powder blue',
        command=back
    )
    back_btn.place(relx=0,rely=0)

    # Account number lable and placed 
    acn_lbl = Label (
        frm,
        text = "ACN",
        font = ('Comic Sans MS',20, 'bold'),
        bg='pink'
    )
    acn_lbl.place(relx=.3, rely=.2)

    # Account ka entry dene ke liye 
    acn_entry = Entry (
        frm,
        font = ('Comic Sans MS',20, 'bold'),
        bd=5,
    )
    acn_entry.place(relx=.4,rely=.2)
    acn_entry.focus()

    # Email label and palced
    email_lbl = Label (
        frm,
        text = "Email",
        font = ('Comic Sans MS',20, 'bold'),
        bg='pink'
    )
    email_lbl.place(relx=.3, rely=.3)

    # Account ka entry dene ke liye 
    email_entry = Entry (
        frm,
        font = ('Comic Sans MS',20, 'bold'),
        bd=5,
    )
    email_entry.place(relx=.4,rely=.3)

    # otp send button 
    otp_btn = Button (
        frm,
        text="Send otp",
        font=('Comis San MS', 18, 'bold'),
        bg='powder blue',
        command=send_forgot_otp

    )
    otp_btn.place(relx=.45,rely=.4)

# customer ke liye main screen
def customer_screen(uacn):
    frm = Frame(root, highlightbackground='black', highlightthickness=1)
    frm.configure(bg="pink")
    frm.place(relx=0, rely=.15,relwidth=1,relheight=.78)

    # ✅ dbmanager se get_name use kiya
    name = dbmanager.get_name(uacn)

    # Admin welcome label
    wel_lbl = Label(
    frm,
    text=f"Welcome {name}",
    font = ('Comic Sans MS',10,'bold'),
    bg="pink",
    fg="purple"
    )
    wel_lbl.place(relx=0, rely=0)

    def logout():
        frm.destroy()
        main_screen()

    def show():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=1)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13, rely=.12,relwidth=.78,relheight=.75)
        
        # frame ke andar lable 
        title_lbl = Label(
        ifrm,
        text="This is show Account Screen",
        font = ('Comic Sans MS',12,'bold'),
        bg="white",
        fg="purple"
        )
        title_lbl.pack() 

        # ✅ dbmanager se get_account use kiya
        tup = dbmanager.get_account(uacn)

        text = f"""
        Account No = {tup[0]}
        Open Date = {tup[7]}
        Acc Adhar = {tup[5]}
        Acc Mob = {tup[4]}
        Acc Bal = {tup[3]}
        """

        info_lbl = Label(
        ifrm,
        text=text,
        font = ('Comic Sans MS',12,'bold'),
        bg="white",
        fg="blue"
        )
        info_lbl.place(relx=.2, rely=.1)


    def edit():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=1)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13, rely=.12,relwidth=.78,relheight=.75)

        def update():
            name = name_entry.get()
            pwd = pass_entry.get()
            mob = mob_entry.get()
            email = email_entry.get()

            # ✅ Direct SQL replaced with dbmanager function
            conobj = sqlite3.connect(database="bank.sqlite")
            curobj = conobj.cursor()
            query = "update accounts set name=?, pass=?, mob=?, email=? where acn=?"
            curobj.execute(query,(name,pwd,mob,email,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("update","Details updated")
        

        
        # frame ke andar lable 
        title_lbl = Label(
        ifrm,
        text="This is Edit Account Screen",
        font = ('Comic Sans MS',12,'bold'),
        bg="white",
        fg="purple"
        )
        title_lbl.pack() 

        # name label and entry 
        name_lbl = Label (
        ifrm,
        text = "Name",
        font = ('Comic Sans MS',15, 'bold'),
        bg='white'
        )
        name_lbl.place(relx=.1, rely=.1)

        name_entry = Entry (
            ifrm,
            font = ('Comic Sans MS',20, 'bold'),
            bd=5,
        )
        name_entry.place(relx=.1,rely=.17)
        name_entry.focus()

        # Email label and entry 
        email_lbl = Label (
        ifrm,
        text = "E-Mail",
        font = ('Comic Sans MS',15, 'bold'),
        bg='white'
        )
        email_lbl.place(relx=.5, rely=.1)
        email_entry = Entry (
            ifrm,
            font = ('Comic Sans MS',20, 'bold'),
            bd=5,
        )
        email_entry.place(relx=.5,rely=.17)
        email_entry.focus()

        # Mobile label and entry 
        mob_lbl = Label (
        ifrm,
        text = "Mobile no",
        font = ('Comic Sans MS',15, 'bold'),
        bg='white'
        )
        mob_lbl.place(relx=.1, rely=.3)
        mob_entry = Entry (
            ifrm,
            font = ('Comic Sans MS',20, 'bold'),
            bd=5,
        )
        mob_entry.place(relx=.1,rely=.37)
        mob_entry.focus()

        # password label and entry 
        pass_lbl = Label (
        ifrm,
        text = "Password",
        font = ('Comic Sans MS',15, 'bold'),
        bg='white'
        )
        pass_lbl.place(relx=.5, rely=.3)
        pass_entry = Entry (
            ifrm,
            font = ('Comic Sans MS',20, 'bold'),
            bd=5,
        )
        pass_entry.place(relx=.5,rely=.37)

        # update and save btn
        update_btn = Button (
            ifrm,
            text="Update & save ",
            font=('Comis San MS', 18, 'bold'),
            bg='green',
            fg="white",
            width=15,
            command=update
        )
        update_btn.place(relx=.35,rely=.68)

        # ✅ dbmanager se get_account use kiya
        tup = dbmanager.get_account(uacn)

        name_entry.insert(0,tup[1])   # name at index 1
        pass_entry.insert(0,tup[2])   # pass at index 2
        mob_entry.insert(0,tup[4])    # mob at index 4
        email_entry.insert(0,tup[6])  # email at index 6

    def deposit():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=1)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13, rely=.12,relwidth=.78,relheight=.75)
        
        # frame ke andar lable 
        title_lbl = Label(
        ifrm,
        text="This is deposit Account Screen",
        font = ('Comic Sans MS',12,'bold'),
        bg="white",
        fg="purple"
        )
        title_lbl.pack() 
        uamt = simpledialog.askfloat("Deposit", "Amount")
        if uamt == None:
            return 

        # ✅ dbmanager se deposit_amount use kiya
        dbmanager.deposit_amount(uacn, uamt)
        messagebox.showinfo("Deposit",f"{uamt} deposited")



    def withdraw():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=1)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13, rely=.12,relwidth=.78,relheight=.75)
        
        # frame ke andar lable 
        title_lbl = Label(
        ifrm,
        text="This is Withdraw Account Screen",
        font = ('Comic Sans MS',12,'bold'),
        bg="white",
        fg="purple"
        )
        title_lbl.pack()

        uamt = simpledialog.askfloat("Withdraw", "Amount")

        # ✅ dbmanager se get_balance use kiya
        bal = dbmanager.get_balance(uacn)

        if bal >= uamt:
            # ✅ dbmanager se withdraw_amount use kiya
            dbmanager.withdraw_amount(uacn, uamt)
            messagebox.showinfo("Withdraw",f"{uamt} withdrawn")
        else:
            messagebox.showerror("Withdraw","Insufficient Balance")



    def transfer():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=1)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13, rely=.12,relwidth=.78,relheight=.75)
        
        # frame ke andar lable 
        title_lbl = Label(
        ifrm,
        text="This is Transfer Account Screen",
        font = ('Comic Sans MS',12,'bold'),
        bg="white",
        fg="purple"
        )
        title_lbl.pack()

        toacn = simpledialog.askinteger("Transfer", "To ACN")

        # ✅ dbmanager se get_account use kiya
        tup = dbmanager.get_account(toacn)
        
        if tup != None:
            uamt = simpledialog.askfloat("Transfer","Amount")

            # ✅ dbmanager se get_balance use kiya
            bal = dbmanager.get_balance(uacn)

            if bal >= uamt:
                # ✅ dbmanager se transfer_amount use kiya
                dbmanager.transfer_amount(uacn, toacn, uamt)
                messagebox.showinfo("Transfer",f"{uamt} Transfer to {toacn}")
            else:
                messagebox.showerror("Withdraw","Insufficient Balance")
        else:
            messagebox.showerror("Transfer","Invalid to ACN")

    


    # Log-out button
    logout_btn = Button (
        frm,
        text="⏻ logout",
        font=('Comis San MS', 15, 'bold'),
        bg='grey',
        command = logout,
    )
    logout_btn.place(relx=.92,rely=.01)

    # customer screen ke andar show button
    show_btn = Button (
        frm,
        text="Show Details",
        font=('Comis San MS', 15, 'bold'),
        bg='Blue',
        fg="white",
        width=12,
        command=show,
    )
    show_btn.place(relx=.001,rely=.1)
    # customer screen ke andar edit button
    edit_btn = Button (
        frm,
        text="Edit Details",
        font=('Comis San MS', 15, 'bold'),
        bg='orange',
        fg="white",
        width=12,
        command=edit,
    )
    edit_btn.place(relx=.001,rely=.25)
    # customer screen ke andar Deposit button
    deposit_btn = Button (
        frm,
        text="Deposit",
        font=('Comis San MS', 15, 'bold'),
        bg='green',
        fg="white",
        width=12,
        command=deposit
    )
    deposit_btn.place(relx=.001,rely=.4)
    # customer screen ke andar withdraw button
    withdraw_btn = Button (
        frm,
        text="Withdraw",
        font=('Comis San MS', 15, 'bold'),
        bg='red',
        fg="white",
        width=12,
        command=withdraw
    )
    withdraw_btn.place(relx=.001,rely=.55)
    # customer screen ke andar tranfer button
    transfer_btn = Button (
        frm,
        text="Transfer",
        font=('Comis San MS', 15, 'bold'),
        bg='purple',
        fg="white",
        width=12,
        command=transfer
    )
    transfer_btn.place(relx=.001,rely=.7)

# Admin ke liye main screen
def admin_screen():
    frm = Frame(root, highlightbackground='black', highlightthickness=1)
    frm.configure(bg="pink")
    frm.place(relx=0, rely=.15,relwidth=1,relheight=.78)

    # Admin welcome label
    wel_lbl = Label(
    frm,
    text="Welcome Admin..",
    font = ('Comic Sans MS',10,'bold'),
    bg="pink",
    fg="purple"
    )
    wel_lbl.place(relx=0, rely=0)

    def logout():
        frm.destroy()
        main_screen()

    # Log-out button
    logout_btn = Button (
        frm,
        text="⏻ logout",
        font=('Comis San MS', 15, 'bold'),
        bg='grey',
        command = logout,
    )
    logout_btn.place(relx=.92,rely=.01)


    # new account ke press krne pe ye function call hogi
    def new():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=1)
        ifrm.configure(bg="white")
        ifrm.place(relx=.1, rely=.2,relwidth=.8,relheight=.7)
        
        # Admin jb open account btn pe click krega to ye function call hogi 
        def open_acn():
            name = name_entry.get()
            email = email_entry.get()
            mob = mob_entry.get()
            adhar = adhar_entry.get()
            bal = 0
            opendate = time.strftime('%d-%b-%Y %r')
            pwd = generator.password()

            # ✅ dbmanager se open_account use kiya
            acn = dbmanager.open_account(name, pwd, bal, mob, adhar, email, opendate)

            # mail send ke liye call
            text = f"""
Welcome {name},
We have successfully opened your account in ABC Bank
This is your Credentails
ACN = {acn}
Pass = {pwd}
"""
            mailing.openacn_mail(email,text)
            messagebox.showinfo("Account open","we have opened account and mailed credentails")
        # frame ke andar lable 
        title_lbl = Label(
        ifrm,
        text="This is New Account Screen",
        font = ('Comic Sans MS',12,'bold'),
        bg="white",
        fg="purple"
        )
        title_lbl.pack() 

        # name label and entry 
        name_lbl = Label (
        ifrm,
        text = "Name",
        font = ('Comic Sans MS',15, 'bold'),
        bg='white'
        )
        name_lbl.place(relx=.1, rely=.1)

        name_entry = Entry (
            ifrm,
            font = ('Comic Sans MS',20, 'bold'),
            bd=5,
        )
        name_entry.place(relx=.1,rely=.17)
        name_entry.focus()

        # Email label and entry 
        email_lbl = Label (
        ifrm,
        text = "E-Mail",
        font = ('Comic Sans MS',15, 'bold'),
        bg='white'
        )
        email_lbl.place(relx=.5, rely=.1)
        email_entry = Entry (
            ifrm,
            font = ('Comic Sans MS',20, 'bold'),
            bd=5,
        )
        email_entry.place(relx=.5,rely=.17)
        email_entry.focus()

        # Mobile label and entry 
        mob_lbl = Label (
        ifrm,
        text = "Mobile no",
        font = ('Comic Sans MS',15, 'bold'),
        bg='white'
        )
        mob_lbl.place(relx=.1, rely=.3)
        mob_entry = Entry (
            ifrm,
            font = ('Comic Sans MS',20, 'bold'),
            bd=5,
        )
        mob_entry.place(relx=.1,rely=.37)
        mob_entry.focus()

        # Adhar label and entry 
        adhar_lbl = Label (
        ifrm,
        text = "Aadhar no",
        font = ('Comic Sans MS',15, 'bold'),
        bg='white'
        )
        adhar_lbl.place(relx=.5, rely=.3)
        adhar_entry = Entry (
            ifrm,
            font = ('Comic Sans MS',20, 'bold'),
            bd=5,
        )
        adhar_entry.place(relx=.5,rely=.37)
        adhar_entry.focus()

        # Open Button 
        open_btn = Button (
            ifrm,
            text="open Account",
            font=('Comis San MS', 18, 'bold'),
            bg='green',
            fg="white",
            width=15,
            command=open_acn
        )
        open_btn.place(relx=.35,rely=.68)



    # view account btn  ke press kren pe ye funcation call hogi
    def view():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=1)
        ifrm.configure(bg="white")
        ifrm.place(relx=.1, rely=.2,relwidth=.8,relheight=.7)
        
        # frame ke andar lable 
        title_lbl = Label(
        ifrm,
        text="This is View Account Screen",
        font = ('Comic Sans MS',12,'bold'),
        bg="white",
        fg="purple"
        )
        title_lbl.pack()

        uacn = simpledialog.askinteger("view Account", " Acc no")

        # ✅ dbmanager se get_account use kiya
        tup = dbmanager.get_account(uacn)
        
        if tup != None:
            messagebox.showinfo("Details",tup)
        else:
            messagebox.showerror("Details","Accounts Does not exist")
    
    # close account btn ke press krne pe ye function call hogi 
    def close():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=1)
        ifrm.configure(bg="white")
        ifrm.place(relx=.1, rely=.2,relwidth=.8,relheight=.7)
        
        # frame ke andar lable 
        title_lbl = Label(
        ifrm,
        text="This is Close Account Screen",
        font = ('Comic Sans MS',12,'bold'),
        bg="white",
        fg="purple"
        )
        title_lbl.pack()

        uacn = simpledialog.askinteger("close Account", " Acc no")
        
        # ✅ dbmanager se get_name_email use kiya
        tup = dbmanager.get_name_email(uacn)
        
        if tup != None:
            otp = generator.close_otp()
            text = f"Hello {tup[0]} \n OTP to close you account :{otp}"
            mailing.closeotp_mail(tup[1],text)
            messagebox.showinfo("Close","We have sent otp to close account")
            uotp = simpledialog.askinteger("close OTP ","OTP")
            if otp == uotp:
                # ✅ dbmanager se delete_account use kiya
                dbmanager.delete_account(uacn)
                messagebox.showinfo("close","Account Closed")
            else:
                messagebox.showerror("Close Account","Invalid OTP")
        else:
            messagebox.showerror("Close","Accounts Does not exist")

    # new Account btn 
    newacn_btn = Button (
        frm,
        text="New Account",
        font=('Comis San MS', 18, 'bold'),
        bg='green',
        bd=5,
        fg="white",
        width=12,
        command=new,
        
    )
    newacn_btn.place(relx=.1,rely=.05)

    # view Account button
    viewacn_btn = Button (
        frm,
        text="View Account",
        font=('Comis San MS', 18, 'bold'),
        bg='blue',
        bd=5,
        fg="white",
        width=12,
        command=view,
        
    )
    viewacn_btn.place(relx=.4 ,rely=.05)

    # Close Account button
    closeacn_btn = Button (
        frm,
        text="Close Account",
        font=('Comis San MS', 18, 'bold'),
        bg='red',
        bd=5,
        fg="white",
        width=12,
        command=close,
        
    )
    closeacn_btn.place(relx=.7,rely=.05)
# main screen banane ki function
def main_screen():
    def forgot():
        frm.destroy()
        forgot_screen()

    # refersh function for change the captcha
    def refersh():
        global gen
        gen_cap = generator.captcha()
        cap_lbl.configure(text=gen_cap)

    #login btn ka function
    def login():
        utype = user_combo.get()
        uacn = acn_entry.get()
        upass = pass_entry.get()
        ucap = cap_entry.get()

        if len(uacn) == 0:
            messagebox.showerror("Login","Please enter ACN")
            return
        if len(upass) == 0:
            messagebox.showerror("Login","Please enter password")
            return
        if len(upass) == 0:
            messagebox.showerror("Login","Please enter captcha")
            return




        global gen_cap
        gen_cap = gen_cap.replace(" ","")
        if ucap != gen_cap:
            messagebox.showerror("Login","Invalid Captcha")
            return
         
        if utype == "Admin":
            if uacn == "0" and upass == "admin":
                frm.destroy()
                admin_screen()
            else:
                messagebox.showerror("Login","Invalid Credentials")

        elif utype == "Customer":
            uacn = int(acn_entry.get())
            upass = pass_entry.get()
            # ✅ dbmanager se login_account use kiya
            tup = dbmanager.login_account(uacn, upass)
            if tup != None:
                frm.destroy()
                customer_screen(uacn) 
            else:
                messagebox.showerror("Login","Invalid credentials")
        else:
            messagebox.showerror("Login","please select user type")

    def reset():
        user_combo.current(0)
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        cap_entry.delete(0,"end")

        acn_entry.focus()

    frm = Frame(root, highlightbackground='black', highlightthickness=1)
    frm.configure(bg="pink")
    frm.place(relx=0, rely=.15,relwidth=1,relheight=.78)

     # user label
    user_lbl = Label (
        frm,
        text = "User",
        font = ('Comic Sans MS',20, 'bold'),
        bg='pink'
    )
    user_lbl.place(relx=.3, rely=.1)

    user_combo = Combobox (
        frm,
        values=['---select','Admin','Customer'],
        font=('Comic Sans MS',20, 'bold'),
    )
    user_combo.place(relx=.4, rely=.1)
    user_combo.current(0)

    # Account ka lable
    acn_lbl = Label (
        frm,
        text = "ACN",
        font = ('Comic Sans MS',20, 'bold'),
        bg='pink'
    )
    acn_lbl.place(relx=.3, rely=.2)

    # Account ka entry dene ke liye 
    acn_entry = Entry (
        frm,
        font = ('Comic Sans MS',20, 'bold'),
        bd=5,
    )
    acn_entry.place(relx=.4,rely=.2)
    acn_entry.focus()

    # password ke liye label
    pass_lbl = Label (
        frm,
        text = "pass",
        font = ('Comic Sans MS',20, 'bold'),
        bg='pink'
    )
    pass_lbl.place(relx=.3, rely=.3)

    # password dene ke liye entry level 
    pass_entry = Entry (
        frm,
        font = ('Comic Sans MS',20, 'bold'),
        bd=5,
        show="*"
    )
    pass_entry.place(relx=.4,rely=.3)

    # captcha ka level 
    global gen_cap
    gen_cap = generator.captcha()  # ye dusre file se inherit ho rhi h 
    cap_lbl = Label (
        frm,
        text = gen_cap,
        font = ('Comic Sans MS',20, 'bold'),
        width=10
    )
    cap_lbl.place(relx=.45,rely=.4)

    # botton for referse 
    refersh_btn = Button (
        frm,
        text=" 🔄",
        font=('Comis San MS', 18, 'bold'),
        bg='powder blue',
        command = refersh,
    )
    refersh_btn.place(relx=.58,rely=.4)

    # captcha ka fill krne ke liye entry 
    cap_entry = Entry (
        frm,
        font = ('Comic Sans MS',20, 'bold'),
        bd=5,
    ) 
    cap_entry.place(relx=.4, rely=.5)

    # Login Button 
    login_btn = Button (
        frm,
        text="Login",
        font=('Comis San MS', 18, 'bold'),
        bg='powder blue',
        command=login
    )
    login_btn.place(relx=.43,rely=.6)

    # reset button
    reset_btn = Button (
        frm,
        text="Reset",
        font=('Comis San MS', 18, 'bold'),
        bg="powder blue",
        command=reset

    )
    reset_btn.place(relx=.52, rely=.6)

    # Forgot password button 
    forgot_btn = Button (
        frm,
        text="Forgot Password",
        font=('Comis San MS', 18, 'bold'),
        bg="powder blue",
        width=20,
        command=forgot,

    )
    forgot_btn.place(relx=.41, rely=.7)


root = Tk()
root.state("zoomed")
root.configure(bg="powder blue")


title_lbl = Label(
    root,
    text="Banking Simulator",
    font = ('Comic Sans MS',30,'bold','underline'),
    bg="powder blue"
    )

title_lbl.pack()

datetime = time.strftime("%d-%b-%Y %r")
dt_lbl = Label(
    root, 
    text= datetime, 
    font = ('Comic Sans MS', 20, 'bold'), 
    bg='powder blue'
    )

dt_lbl.pack()
update_time()

img = Image.open("logo.jpg").resize((200, 120))
tkimg = ImageTk.PhotoImage(img, master=root)

logo_lbl = Label(root, image=tkimg)
logo_lbl.image = tkimg   # image ko garbage collection se bachane ke liye

logo_lbl.place(relx=0, rely=0)

# footer ke liye label
footer_lbl = Label(
    root,
    text="⚡ Crafted with Python & Tkinter by Sunny Raj ⚡",
    font=('Comic Sans MS', 12, 'bold'),
    bg='powder blue',
    fg='purple'
)

footer_lbl.pack(side='bottom', pady=8)

main_screen() # main screen function call
root.mainloop() # root function call ho rha 