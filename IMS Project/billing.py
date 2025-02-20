from ast import Str
from os import stat
import string
from telnetlib import STATUS
from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import time
import sqlite3
import os
import tempfile

class BillClass:
       def __init__(self,root):
              self.root=root
              self.root.geometry("1350x700+0+0")
              self.root.title("Inventory Management System")
              self.root.config(bg="white")
              self.cart_list=[]
              self.chk_print=0
    #_____Title___#
              self.icon_title=PhotoImage(file="images/logo1.png")
              title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

    #____BTN__LOGOUT___#
              btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
 #=====Product Frame========
      
              productFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
              productFrame1.place(x=6,y=110,width=410,height=550)

              pTitle=Label(productFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

              productFrame2=Frame(productFrame1,bd=2,relief=RIDGE,bg="white")
              productFrame2.place(x=2,y=42,width=398,height=90)

       #==========label=============

              self.var_search=StringVar() 

              lbl_search=Label(productFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
       
              lbl_search=Label(productFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
              txt_search=Entry(productFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=130,y=47,width=150,height=22)
              btn_search=Button(productFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)

              btn_show_all=Button(productFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083551",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

              cart_frame=Frame(productFrame1,bd=3,relief=RIDGE)
              cart_frame.place(x=2,y=140,width=398,height=375)

              scrolly=Scrollbar(cart_frame,orient=VERTICAL)
              scrollx=Scrollbar(cart_frame,orient=HORIZONTAL)

              self.product_Table=ttk.Treeview(cart_frame,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
              scrollx.pack(side=BOTTOM,fill=X)
              scrolly.pack(side=RIGHT,fill=Y)
              scrollx.config(command=self.product_Table.xview)
              scrolly.config(command=self.product_Table.yview)

              self.product_Table.heading("pid",text="PID")
              self.product_Table.heading("name",text="Name")
              self.product_Table.heading("price",text="Price")
              self.product_Table.heading("qty",text="QTY")
              self.product_Table.heading("status",text="Status")
              self.product_Table["show"]="headings"
              self.product_Table.pack(fill=BOTH,expand=1)

              self.product_Table.column("pid",width=40)
              self.product_Table.column("name",width=100)
              self.product_Table.column("price",width=100)
              self.product_Table.column("qty",width=40)
              self.product_Table.column("status",width=90)
              self.product_Table.pack(fill=BOTH,expand=1)
              self.product_Table.bind("<ButtonRelease-1>",self.get_data)
       

              lbl_note=Label(productFrame1,text="Note:Enter 0 Qunatity to remove product from the cart",font=("gaudy old style",10,"bold"),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)

#==========Customer Frame

              self.var_name=StringVar()
              self.var_contact=StringVar()
              customerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
              customerFrame.place(x=420,y=110,width=530,height=70)
              cTitle=Label(customerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgrey").pack(side=TOP,fill=X)
              lbl_name=Label(customerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
              txt_name=Entry(customerFrame,textvariable=self.var_name,font=("times new roman",15),bg="lightyellow").place(x=80,y=35,width=180)

              lbl_contact=Label(customerFrame,text="contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
              txt_contact=Entry(customerFrame,textvariable=self.var_contact,font=("times new roman",15),bg="lightyellow").place(x=380,y=35,width=140)

              Cal_Cart_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
              Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)
       
#=================Calculator Frame===========
              self.var_cal_input=StringVar()
              Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
              Cal_Frame.place(x=5,y=10,width=268,height=340)
       

              txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=("arial",15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
              txt_cal_input.grid(row=0,columnspan=4)

              btn_7=Button(Cal_Frame,text='7',font=("arial",15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=0)
              btn_8=Button(Cal_Frame,text="8",font=("arial",15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=1)
              btn_9=Button(Cal_Frame,text="9",font=("arial",15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=2)
              btn_sum=Button(Cal_Frame,text= "+",font=("arial",15,'bold'),command=lambda:self.get_input("+"),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=3)


              btn_4=Button(Cal_Frame,text="4",font=("arial",15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=0)
              btn_5=Button(Cal_Frame,text="5",font=("arial",15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=1)
              btn_6=Button(Cal_Frame,text="6",font=("arial",15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=2)
              btn_subtract=Button(Cal_Frame,text= "-",font=("arial",15,'bold'),command=lambda:self.get_input("-"),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=3)


              btn_1=Button(Cal_Frame,text="1",font=("arial",15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=0)
              btn_2=Button(Cal_Frame,text="2",font=("arial",15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=1)
              btn_3=Button(Cal_Frame,text="3",font=("arial",15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=2)
              btn_mul=Button(Cal_Frame,text= "*",font=("arial",15,'bold'),command=lambda:self.get_input("*"),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=3)

              btn_0=Button(Cal_Frame,text="0",font=("arial",15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=0)
              btn_c=Button(Cal_Frame,text="c",font=("arial",15,'bold'),command=self.clear_cal,bg="green",bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=1)
              btn_eq=Button(Cal_Frame,text="=",font=("arial",15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=2)
              btn_div=Button(Cal_Frame,text= "/",font=("arial",15,'bold'),command=lambda:self.get_input("/"),bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=3)
#======================== 
              cart_frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
              cart_frame.place(x=280,y=8,width=245,height=342)
              self.cartTitle=Label(cart_frame,text="Cart \t Total Ptoducts: [0] ",font=("goudy old style",15),bg="lightgrey")
              self.cartTitle.pack(side=TOP,fill=X)
              
              scrolly=Scrollbar(cart_frame,orient=VERTICAL)
              scrollx=Scrollbar(cart_frame,orient=HORIZONTAL)

              self.CartTable=ttk.Treeview(cart_frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
              scrollx.pack(side=BOTTOM,fill=X)
              scrolly.pack(side=RIGHT,fill=Y)
              scrollx.config(command=self.CartTable.xview)
              scrolly.config(command=self.CartTable.yview)

              self.CartTable.heading("pid",text="PID")
              self.CartTable.heading("name",text="Name")
              self.CartTable.heading("price",text="Price")
              self.CartTable.heading("qty",text="QTY")
              
              self.CartTable["show"]="headings"
              self.CartTable.pack(fill=BOTH,expand=1)

              self.CartTable.column("pid",width=40)
              self.CartTable.column("name",width=90)
              self.CartTable.column("price",width=100)
              self.CartTable.column("qty",width=40)
              
              self.CartTable.pack(fill=BOTH,expand=1)
              self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart) 

#====================menu=========================
              self.var_pid=StringVar()
              self.var_pname=StringVar()
              self.var_price=StringVar()
              self.var_qty=StringVar()
              self.var_stock=StringVar()
              
              Add_cartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
              Add_cartWidgetsFrame.place(x=420,y=550,width=530,height=110)
                     
              
              lbl_p_name=Label(Add_cartWidgetsFrame,text="Product Name", font=("times new roman",15),bg="white").place(x=5,y=5)
              txt_p_name=Entry(Add_cartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=150,height=22)

              lbl_p_price=Label(Add_cartWidgetsFrame,text="Price per Qty", font=("times new roman",15),bg="white").place(x=230,y=5)
              txt_p_price=Entry(Add_cartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

              lbl_p_Qty=Label(Add_cartWidgetsFrame,text="Quantity", font=("times new roman",15),bg="white").place(x=390,y=5)
              txt_p_Qty=Entry(Add_cartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)

              self.lbl_instock=Label(Add_cartWidgetsFrame,text="In stock",font=("times new roman",15),bg="white")
              self.lbl_instock.place(x=5,y=70)
     
              btn_clear_cart=Button(Add_cartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgrey",cursor="hand2").place(x=180,y=70,width=150,height=30)
              btn_add_cart=Button(Add_cartWidgetsFrame,text="Add | update cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)

              #=====================Billing Frame============================

              billFrame=Frame(self.root,bd=2,relief=RIDGE)
              billFrame.place(x=953,y=110,width=410,height=410)
              bTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="red",fg="white").pack(side=TOP,fill=X)
              scrolly=Scrollbar(billFrame,orient=VERTICAL)
              scrolly.pack(side=RIGHT,fill=Y)
              
              self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
              self.txt_bill_area.pack(fill=BOTH,expand=1)
              
              scrolly.config(command=self.txt_bill_area.yview)

              #===============Billing Buttn=================
              billMenuFrame=Frame(self.root,bd=2,relief=RIDGE)
              billMenuFrame.place(x=953,y=520,width=410,height=410)

              self.lbl_amnt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("times new roman",15,"bold"),bg="#3f51b5",fg="white")
              self.lbl_amnt.place(x=2,y=5,width=120,height=120)
              
              self.lbl_discount=Label(billMenuFrame,text="Discount\n[5%]",font=("times new roman",15,"bold"),bg="#8bc34a",fg="white")
              self.lbl_discount.place(x=124,y=5,width=120,height=70)
              
              self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("times new roman",15,"bold"),bg="#607d8b",fg="white")
              self.lbl_net_pay.place(x=246,y=5,width=120,height=70)

              #btn_print=Button(billMenuFrame,text="Print",cursor="hand2",font=("times new roman",15,"bold"),bg="#3f51b5",fg="white")
              #btn_print.place(x=2,y=80,width=120,height=50)
              
              btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,cursor="hand2",font=("times new roman",15,"bold"),bg="#8bc34a",fg="white")
              btn_clear_all.place(x=124,y=80,width=120,height=50)
              
              btn_generate=Button(billMenuFrame,text="Generate Bill \n /Save Bill",command=self.generate_bill,cursor="hand2",font=("times new roman",15,"bold"),bg="dark green",fg="white")

              btn_generate.place(x=246,y=80,width=120,height=50)

              #========Footer======
              footer=Label(self.root,text="IMS-Inventory Management System",font=("times new roman",11),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
              self.show()
              #self.bill_top()
       #====================All Functions==============
       def get_input(self,num):
              xnum=self.var_cal_input.get()+str(num)
              self.var_cal_input.set(xnum)
       
       def clear_cal(self):
              self.var_cal_input.set('')

       def perform_cal(self):
              result=self.var_cal_input.get()
              self.var_cal_input.set(eval(result))




       def show(self):
              con=sqlite3.connect(database=r'ims.db')
              cur=con.cursor()
              try:
                cur.execute("select pid,name,price,qty,status from product where status='Active'")
                rows=cur.fetchall()
                self.product_Table.delete(*self.product_Table.get_children())
                for row in rows:
                            self.product_Table.insert('',END,values=row)
              
              except Exception as ex:
                     messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


   
  
  
  
       def search(self):
              con=sqlite3.connect(database=r'ims.db')
              cur=con.cursor()
              try:
                     if self.var_search.get()=="":
                            messagebox.showerror("Error","Search Input Should Be Required",parent=self.root)
                     else:
                            cur.execute("select pid,name,price,qty,status from product where name  LIKE '%"+ self.var_search.get()+"%'") 
                            rows=cur.fetchall()
                            if len(rows)!=0:
                               self.product_Table.delete(*self.product_Table.get_children())
                            else:
                                 messagebox.showerror("Error","No Record Found!!!",parent=self.root)

                            for row in rows:
                             self.product_Table.insert('',END,values=row)
                            
              except Exception as ex:
                     messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
       def get_data(self,ev):
              f=self.product_Table.focus()
              content=(self.product_Table.item(f))
              row=content['values']
              self.var_pid.set(row[0])
              self.var_pname.set(row[1])   
              self.var_price.set(row[2])
              self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
              
              self.var_qty.set('1')


       def get_data_cart(self,ev):
              f=self.product_Table.focus()
              content=(self.product_Table.item(f))
              row=content['values']

              self.var_pid.set(row[0])
              self.var_pname.set(row[1])   
              self.var_price.set(row[2])
              self.var_qty.set(row[3])
              self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
              self.var_stock.set(row[4])
       
       
       def add_update_cart(self):
              if self.var_pid.get()=='':
                     messagebox.showerror('Error',"Please select Product from the list")
              elif self.var_qty.get()=='':
                            messagebox.showerror("Error","Quantity is required",parent=self.root)
              elif str(self.var_qty.get())>str(self.var_stock):
                            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
              else:
               price_cal=self.var_price.get()     
               cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()] #===update cart
               present='no'
               index_=0
               for row in self.cart_list:
                     if self.var_pid.get()==row[0]:
                            present='yes'
                            break
                     index_=1
              if present=='yes':
                     op=messagebox.askyesno('Confirm',"Product already present\ndo you want to update| Remove from the cart List",parent=self.root)
                     if op==True:
                            if self.var_qty.get()=="0":
                                   self.cart_list.pop(index_)
                            else:
                                   self.cart_list[index_][2]=price_cal #price
                                   self.cart_list[index_][3]=self.var_qty.get()
                                   self.cart_list[index_][3]=self.var_qty.get()
              else:
                     self.cart_list.append(cart_data)
              self.show_cart()
              self.bill_updates()


       def bill_updates(self):
              self.bill_amnt=0
              self.net_pay=0
              self.discount=0
              for row in self.cart_list:
                     
                     self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))

              self.discount=(self.bill_amnt*5)/100
              self.net_pay=self.bill_amnt-self.discount
              self.lbl_amnt.config(text=f'Bill Amount\n{str(self.bill_amnt)}')
              self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
              self.cartTitle.config(text=f"Cart |t Total Product [{str(len(self.cart_list))}]")
              

               
       def show_cart(self):
              try:
                   self.CartTable.delete(*self.CartTable.get_children())
                   for row in self.cart_list:
                            self.CartTable.insert('',END,values=row)
              
              except Exception as ex:
                     messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

       def generate_bill(self):
              if self.var_name.get()=='' or self.var_contact.get()=='':
                     messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
              elif len(self.cart_list)==0:
                     messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)
              else:
                     self.bill_top(),
                     self.bill_middle(),
                     self.bill_bottom()

                     fp=open(f"bill/{str(self.invoice)}.txt",'w')
                     fp.write(self.txt_bill_area.get('1.0',END))
                     fp.close()
                     messagebox.showinfo("Saved","Bill has been generated And Saved in Backend",parent=self.root)


       def bill_top(self):
            self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
            bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 98725*** , Delhi-125001
{str("="*47)}
 Customer Name: {self.var_name.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
            self.txt_bill_area.delete('1.0',END)
            self.txt_bill_area.insert('1.0',bill_top_temp)

       def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''

        self.txt_bill_area.insert(END,bill_bottom_temp)

       
        
       def bill_middle(self):
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()

            try:
                     for row in self.cart_list:
                            
                            pid=row[0]
                            name=row[1]
                            self.var_stock.get()
                            qty=row[3]
                            #qty=row[3]

                            if str(qty)==str(row[4]):
                                   status='Inactive'
                            if str(qty)!=str(row[4]):
                                   status='Active'


                            price=float(row[2])*int(row[3])
                            price=str(price)
                            self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+qty+"\tRs."+price)
                            cur.execute('update product set status=? where pid=?',(

                                   status,
                                   pid
                            ))
                            con.commit()
                     con.close()
                     self.show()
        
            except Exception as ex:
                     messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
       
       def clear_cart(self):
            self.var_pid.set('')
            self.var_pname.set('')   
            self.var_price.set('')
            self.var_qty.set('')
            self.lbl_instock.config(text=f"In Stock")
            self.var_stock.set('')
       
       def clear_all(self):
              del self.cart_list[:]
              self.var_name.set('')
              self.var_contact.set('')
              self.txt_bill_area.delete('1.0',END)
              self.cartTitle.config(text=f"cart \t Total Product:[0]")
              self.var_search.set('')
              self.clear_cart()
              self.show()
              self.show_cart()

       def logout(self):
              self.root.destroy()
              os.system("python login.py")




if __name__=="__main__":
              root=Tk()
              obj=BillClass(root)
              root.mainloop()