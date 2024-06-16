import os
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk #pip install pillow
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from billing import BillClass
from sales import salesClass
class IMS:
   def __init__(self,root):
       self.root=root
       self.root.geometry("1350x700+0+0")
       self.root.title("Inventory Management System")
       self.root.config(bg="white")
    #_____Title___#
       self.icon_title=PhotoImage(file="images/logo1.png")
       title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

    #____BTN__LOGOUT___#
       btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
    
    

    #____Left Menu____#
       self.MenuLogo=Image.open("images/menu_im.png")
       self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
       self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
       LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
       LeftMenu.place(x=0,y=102,width=200,height=565)         
       
        
       lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
       lbl_menuLogo.pack(side=TOP,fill=X)
       
       self.icon_side=PhotoImage(file="images/side.png")
       lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
       
       
       btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
       btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
       btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
       btn_product=Button(LeftMenu,text="Products",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
       btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
       btn_exit=Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
 
      #____Content____#
       self.DashboardImage=PhotoImage(file="images/D2.png")
       label = Label(self.root, image = self.DashboardImage)
       label.place(x=215,y=96,width=1125,height=550)

      
       

      #___Footer___#
       lbl_footer=Label(self.root,text="IMS: Inventory Management System \n © 2022 Sandeep Dwivedi",font=("times new roman",12 ,"bold"),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
#==================================================================================================
   def employee(self):
      self.new_win=Toplevel(self.root)
      self.new_obj=employeeClass(self.new_win) 

   def supplier(self):
          self.new_win=Toplevel(self.root)
          self.new_obj=supplierClass(self.new_win)  
   def category(self):
          self.new_win=Toplevel(self.root)
          self.new_obj=categoryClass(self.new_win)
   
   def product(self):
          self.new_win=Toplevel(self.root)
          self.new_obj=productClass(self.new_win)
   def bill(self):
          self.new_win=Toplevel(self.root)
          self.new_obj=BillClass(self.new_win)
   def sales(self):
          self.new_win=Toplevel(self.root)
          self.new_obj=salesClass(self.new_win)

   def update_content(self):
         con=sqlite3.connect(database=r'ims.db')
         cur=con.cursor()
         try:
            cur.execute('select * from product')
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Products\n[ {str(len(product))}')

            cur.execute('select * from category')
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total category\n[ {str(len(category))}')

            cur.execute('select * from employee')
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employees\n[ {str(len(employee))}')
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales [ {str(bill)}')


         except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

   def logout(self):
          self.root.destroy()
          os.system("python login.py")

            
          

if __name__=="__main__":
         root=Tk()
         obj=IMS(root)
         root.mainloop()

