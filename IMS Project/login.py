from cProfile import label
import email
import os
from textwrap import fill
from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
class Login_system:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System | Developed By Sandeep")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        
        self.otp=''

        #======images
        self.phone_image=PhotoImage(file="images/login2.png")
  
# Create a Label Widget to display the text or Image
        label = Label(self.root, image = self.phone_image)
        label.pack()
  
#======Login Frame
        self.employee_id=StringVar()
        self.password=StringVar()
        
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)
        
      
        title=Label(login_frame,text="Login System",font=("courier New",30,"bold"),bg='white',fg='black').place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("courier New",15),bg="white",fg="black").place(x=50,y=100)
        txt_employee_id=id=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("courier New",15),bg="white",fg="black").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,command=self.login,text="Log In",font=("courier New",15),bg="green",activebackground="#00B0F0",fg="White",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        OR_=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        OR_=Label(login_frame,text="OR",bg="white",fg="black",font=("times new roman",15,"bold")).place(x=150,y=355)

        btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",13),bg="white",activebackground="white",fg="#00759E",activeforeground="#00759E",cursor="hand2",bd=0).place(x=100,y=390)

        #=====Frame2
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=650,y=570,width=350,height=60)

        lbl_reg=Label(register_frame,text="© 2022 Sandeep Dwivedi",font=("times new roman",13),bg="white").place(x=33,y=20)

        
    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try: 
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"All fields are required",parent=self.root)
            else:
                cur.execute('select utype from employee where eid=? AND pass=?',((self.employee_id.get(),self.password.get())))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"Invalid Username/password",parent=self.root)
                else:
                   
                    if user[0]=="Admin":    
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",F"Error due to : {str(ex)}",parent=self.root)

    

    def forget_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error',"Employee ID must be required",parent=self.root)
            else:
                cur.execute('select email from employee where eid=? ',((self.employee_id.get(),)))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid Employee ID ,Try Again",parent=self.root)
                else:
                    #forget Window
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #call send_email_function() 
                    chk=self.send_email(email[0])
                    if chk!='s':
                        messagebox.showerror("Error","connection Error, Try again",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)                    
                        self.forget_win.title('Reset Password')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text='Reset Password',font=('goudy old style',15,'bold'),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text='Enter OTP sent on Registered Email',font=('times new roman',15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=('times new roman',15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

                        self.btn_reset=Button(self.forget_win,text="submit",command=self.validate_otp,font=('times new roman',15),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)


                        new_pass=Label(self.forget_win,text='New Password',font=('times new roman',15)).place(x=20,y=160)
                        text_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=('times new roman',15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        conf_pass=Label(self.forget_win,text='Confirm Password',font=('times new roman',15)).place(x=20,y=225)
                        txt_conf_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=('times new roman',15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="update",command=self.update_password,state=DISABLED,font=('times new roman',15),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)
        except Exception as ex:
                messagebox.showerror("Error",F"Error due to : {str(ex)}",parent=self.root)

    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        

        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/madam,\n\nYour Reset OTP is {str(self.otp)}.\n\n with regards, \n IMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)

        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get()!=  self.var_conf_pass.get():
            messagebox.showerror("Error","New Password & confirm Password should be same")
        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","password updated Successfully",parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",F"Error due to : {str(ex)}",parent=self.root)


    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error",'Invalid OTP, Try Again',parent=self.forget_win)

root=Tk()
obj=Login_system(root)
root.mainloop()