from logging import info
from os import name
import sqlite3
from numpy import result_type
from sqlalchemy.engine.interfaces import ExceptionContext
from sqlalchemy.sql.functions import mode
import streamlit as st
from streamlit.state.session_state import Value
#from Function.example_2 import add
from medical_inventory import Supplier,Drug,Customer,Invoice
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,DateTime, engine
from PIL import Image

conn=sqlite3.connect('data.db')
c=conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def open_db():
    '''function connects to database'''
    engine = create_engine('sqlite:///medical_inventory.sqlite3')
    Session = sessionmaker(bind=engine)
    return Session()

st.title("Medical Inventory")

image = Image.open('inventory.jpg')
st.image(image, caption='Medicine Inventory Application')

menu=['Home','Login','Sign up']
choice=st.sidebar.selectbox("Menu",menu)
if choice=="home":
    st.subheader("Home")
elif choice=="Login":
    st.subheader("Login")
    username=st.sidebar.text_input("User Name")
    password=st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Login"):
        create_usertable()
        result=login_user(username,password)
        if result:
            st.success("Logged in as {} ".format(username))
        
            choices = ['Supplier','Drug','Customer','Invoice','Show Details']
            selected_choice = st.selectbox("select an option",options=choices)

            if selected_choice== choices[0]:
                st.subheader("Supplier")
                choices = ['Add Supplier Details','Update and Delete Supplier Details','show Supplier Details',]
                selected_choice = st.selectbox("select an option",options=choices)

                if selected_choice== choices[0]:
                    
                    with st.form("Add Supplier Details"):
                
                        id=st.number_input("Enter supplier id",value=0)
                        companyName=st.text_input("Enter company name")
                        col1,col2=st.columns(2)
                        with col1:
                            mobile=st.number_input(label="Mobile Number",value=0,)

                    
                        with col2:
                            email = st.text_input(label='E-mail')
                        
                        address=st.text_input("Enter Address")
                        city=st.text_input('Enter city')
                        
                        btn= st.form_submit_button("Submit")
                        
                    if id and btn :
                        try:
                            db=open_db()
                            c1=Supplier(id=id,companyname=companyName,mobilephone=mobile,emailaddress=email,address=address,city=city)
                            db.add(c1)
                            db.commit()
                            st.success("Supplier info save successfully")

                            st.markdown(f'''
                            ##### supplier id - {id}
                            - ###### Company name - {companyName}
                            - ###### Mobile Number - {mobile}
                            - ###### E-mail - {email}
                            - ###### Address - {address}
                            - ###### City - {city}
                            ''')

                            db.close()

                        except Exception as e:
                            st.error(f"Could not save the info of Supplier . {e}")

                elif selected_choice== choices[1]:
                    
                    st.form("Update and Delete Supplier Details")
                    id = st.number_input("Supplier ID",value=0)
                    db = open_db()
                    result = db.query(Supplier).get(id)
                    if not result:
                        st.warning("first fill the Supplier ID.")
                    else:
                        with st.form("add supplier"):

                            companyName=st.text_input("Enter company name",value=result.companyname)
                            col1,col2=st.columns(2)
                            with col1:
                                mobile=st.number_input(label="Mobile Number",value=result.mobilephone)
                            with col2:
                                email = st.text_input(label='E-mail',value=result.emailaddress)
                            
                            address=st.text_input("Enter Address",value=result.address)
                            city=st.text_input('Enter city',value=result.city)
                            
                            col1,col2,col3,col4 = st.columns(4)
                            with col1:
                                pass 
                            with col2:
                                btn1= st.form_submit_button("Update")
                                
                            with col3:
                                btn2= st.form_submit_button("Delete")

                            with col4:
                                pass 
                        
                        if id and btn1:
                            try:
                                result.companyname=companyName
                                result.mobilephone=mobile
                                result.emailaddress=email
                                result.address=address
                                result.city=city
                                db.commit()
                                st.success("Supplier info Update successfully")

                                st.markdown(f'''
                                ##### Supplier id - {id}
                                - ###### Company name - {companyName}
                                - ###### Mobile Number - {mobile}
                                - ###### E-mail - {email}
                                - ###### Address - {address}
                                - ###### City - {city}
                                ''')
                            except Exception as e:
                                st.error(f"Could not Update the info of Supplier . {e}")

                        elif id and btn2:
                            try:
                                db.delete(result)
                        
                                db.commit()
                                st.success("Supplier info Delete successfully")

                            except Exception as e:
                                st.error(f"Could not Delete the info of Supplier . {e}")
                                
                    db.close() 
            
                elif selected_choice== choices[2]:
                    st.subheader("Showing Supplier Details")
                    db = open_db()
                    supplier_list= db.query(Supplier)
                    for item in supplier_list:
                        st.markdown(f'''
                        ##### supplier id - {item.id}
                        - ###### Company name - {item.companyname}
                        - ###### Mobile Number - {item.mobilephone}
                        - ###### E-mail - {item.emailaddress}
                        - ###### Address - {item.address}
                        - ###### City - {item.city}
                        ''')

                    db.close()  
                
            elif selected_choice==choices[1]:
                st.subheader('Drugs')
                choices = ['Add Drug Details','Update and Delete Drug Details','Show Drugs Details',]
                selected_choice = st.selectbox("select an option",options=choices)

                if selected_choice== choices[0]:
                    with st.form("Add Drug Details"):
                        id=st.number_input("Enter drug id",value=0)
                        drugname=st.text_input("Drug Name")
                        scientificname=st.text_input("Scientific Name")
                        manufacturer=st.text_input("Manufacturer")
                        col1,col2=st.columns(2)
                        with col1:
                            unitPrice=st.number_input("Unit Price")
                        with col2:
                            no_of_units_in_Package=st.number_input("No of units in package")
                        
                        col1,col2=st.columns(2)
                        with col1:
                            storageTemperature=st.number_input("Storage Temperature in ° C")
                        with col2:
                            dangerousLevel=st.radio(label="Dangarous Level ",options=["Low","Medium","High"])
                        storageLocation=st.text_input("Storage Location")
                        #supplier=st.text_input("supplier")
                        btn= st.form_submit_button("Submit")
                    if id and btn :
                        try:
                            db=open_db()
                            c1=Drug(id=id,name=drugname,scientificname=scientificname,manufacturer=manufacturer,unitprice=unitPrice,no_of_units_in_package=no_of_units_in_Package,storagetemperature=storageTemperature,dangerouslevel=dangerousLevel,storagelocation=storageLocation)
                            db.add(c1)
                            db.commit()
                            st.success("Drug info save Successfully")

                            st.markdown(f'''
                            ##### Drug id - {id}
                            - ###### Name - {drugname}
                            - ###### Scientific Name - {scientificname}
                            - ###### Manufacturer - {manufacturer}
                            - ###### Unitprice - {unitPrice}
                            - ###### No_Of_Units_In_Package - {no_of_units_in_Package}
                            - ###### Storage Temperature - {storageTemperature}
                            - ###### Dangerous Level - {dangerousLevel}
                            - ###### Storage Location - {storageLocation}
                            
                            ''')
                            db.close()

                        except Exception as e:
                            st.error(f"Could not save the info of Drug . {e}")
                
                elif selected_choice==choices[1]:
                    st.subheader('Update Drug Details')

                    id = st.number_input("Drug ID",value=0)
                    db = open_db()
                    result = db.query(Drug).get(id)
                    if not result:
                        st.warning("first fill the Drug ID.")
                    else:
                        with st.form("add Drug"):

                            drugname=st.text_input("Drug Name",value=result.name)
                            scientificname=st.text_input("Scientific Name",value=result.scientificname)
                            manufacturer=st.text_input("Manufacturer",value=result.manufacturer)
                            col1,col2=st.columns(2)
                            with col1:
                                unitPrice=st.number_input("Unit Price",value=result.unitprice)
                            with col2:
                                no_of_units_in_Package=st.number_input("No of units in package",value=result.no_of_units_in_package)
                            
                            col1,col2=st.columns(2)
                            with col1:
                                storageTemperature=st.number_input("Storage Temperature in ° C",value=result.storagetemperature)
                            with col2:
                                dangerousLevel=st.radio(label="Dangarous Level ",options=["Low","Medium","High"])
                            storageLocation=st.text_input("Storage Location",value=result.storagelocation)
                                
                            col1,col2,col3,col4 = st.columns(4)
                            with col1:
                                pass 
                            with col2:
                                btn1= st.form_submit_button("Update")
                                
                            with col3:
                                btn2= st.form_submit_button("Delete")

                            with col4:
                                pass 
                        
                        if id and btn1:
                            try:
                                result.name=drugname
                                result.scientificname=scientificname
                                result.manufacturer=manufacturer
                                result.unitprice=unitPrice
                                result.no_of_units_in_package=unitPrice
                                result.storagetemperature=no_of_units_in_Package
                                result.dangerouslevel=storageTemperature
                                result.storagelocation=storageLocation
                                db.commit()
                                st.success("Drug info Update Successfully")

                                st.markdown(f'''
                                ##### Drug id - {id}
                                - ###### Name - {drugname}
                                - ###### Scientific Name - {scientificname}
                                - ###### Manufacturer - {manufacturer}
                                - ###### Unitprice - {unitPrice}
                                - ###### No_Of_Units_In_Package - {no_of_units_in_Package}
                                - ###### Storage Temperature - {storageTemperature}
                                - ###### Dangerous Level - {dangerousLevel}
                                - ###### Storage Location - {storageLocation}
                                
                                ''')
                            except Exception as e:
                                st.error(f"Could not Update the info of Drug . {e}")

                        elif id and btn2:
                            try:
                                db.delete(result)
                        
                                db.commit()
                                st.success("Drug info Delete Successfully")

                            except Exception as e:
                                st.error(f"Could not Delete the info of Drug . {e}")
                
                    db.close()
                
                elif selected_choice== choices[2]:
                    st.subheader("Showing Drug Details")
                    db = open_db()
                    drug_list= db.query(Drug)
                    for item in drug_list:
                        st.markdown(f'''
                        ##### Drug id - {item.id}
                        - ###### Name - {item.name}
                        - ###### Scientific Name - {item.scientificname}
                        - ###### Manufacturer - {item.manufacturer}
                        - ###### Unitprice - {item.unitprice}
                        - ###### No_Of_Units_In_Package - {item.no_of_units_in_package}
                        - ###### Storage Temperature - {item.storagetemperature}
                        - ###### Dangerous Level - {item.dangerouslevel}
                        - ###### Storage Location - {item.storagelocation}
                        
                        ''')

                    db.close()

            elif selected_choice==choices[2]:

                st.subheader('Customer')
                choices = ['Add Customer Details','Update and Delete Customer Details','Show Customer Details',]
                selected_choice = st.selectbox("select an option",options=choices)

                if selected_choice== choices[0]:
                    with st.form('Add Customer Details'):

                        id=st.text_input(label="Cutomer Id",value=0)
                        pharmacyname=st.text_input("Enter your pharmacy name")
                        col1, col2 = st.columns(2)
                        with col1:
                            firstname = st.text_input(label='First Name')

                    
                        with col2:
                            lastname=st.text_input(label="Last Name")

                        col1, col2 = st.columns(2)
                        with col1:
                            age = st.number_input(label='Age',value=0)

                    
                        with col2:
                            mobile=st.number_input(label="Mobile Number",value=0)

                    
                        
                        email = st.text_input(label='E-mail')

                        address=st.text_input(label="Address")

                        btn= st.form_submit_button("Submit")
                    
                    if id and btn :
                        try:
                            db=open_db()
                            c1=Customer(id=id,pharmacyname=pharmacyname,firstname=firstname,lastname=lastname,mobilephone=mobile,emailaddress=email,age=age,address=address)
                            db.add(c1)
                            db.commit()
                            st.success("Customer info save Successfully")

                            st.markdown(f'''
                            ##### Invoice id - {id}
                            - ###### First Name - {firstname}
                            - ###### Last Name - {lastname}
                            - ###### Mobile Number - {mobile}
                            - ###### E-mail - {email}
                            - ###### Pharmacy Name - {pharmacyname}
                            - ###### Age - {age}
                            - ###### Address - {address}
                                            
                            ''')

                            db.close()

                        except Exception as e:
                            st.error(f"Could not save the info of Customer . {e}")

                elif selected_choice==choices[1]:
                    st.subheader('Update Customer Details')

                    id = st.number_input("Customer ID",value=0)
                    db = open_db()
                    result = db.query(Customer).get(id)
                    if not result:
                        st.warning("first fill the Customer ID.")
                    else:
                        with st.form("add Customer"):
                            pharmacyname=st.text_input("Enter your pharmacy name",value=result.pharmacyname)
                        
                            col1, col2 = st.columns(2)
                            with col1:
                                firstname = st.text_input(label='First Name',value=result.firstname)

                        
                            with col2:
                                lastname=st.text_input(label="Last Name",value=result.lastname)

                            col1, col2 = st.columns(2)
                            with col1:
                                age = st.number_input(label='Age',value=result.age)

                        
                            with col2:
                                mobile=st.number_input(label="Mobile Number",value=result.mobilephone)

                        
                            
                            email = st.text_input(label='E-mail',value=result.emailaddress)

                            address=st.text_input(label="Address",value=result.address)

                            col1,col2,col3,col4 = st.columns(4)
                            with col1:
                                pass 
                            with col2:
                                btn1= st.form_submit_button("Update")
                                
                            with col3:
                                btn2= st.form_submit_button("Delete")

                            with col4:
                                pass 
                        
                        if id and btn1 :
                            try:
                                result.pharmacyname=pharmacyname
                                result.firstname=firstname
                                result.lastname=lastname
                                result.mobilephone=mobile
                                result.emailaddress=email
                                result.age=age
                                result.address=address
                                db.commit()
                                st.success("Customer info Update Successfully")

                                st.markdown(f'''
                                ##### Invoice id - {id}
                                - ###### First Name - {firstname}
                                - ###### Last Name - {lastname}
                                - ###### Mobile Number - {mobile}
                                - ###### E-mail - {email}
                                - ###### Pharmacy Name - {pharmacyname}
                                - ###### Age - {age}
                                - ###### Address - {address}
                                                    
                                ''')
                            except Exception as e:
                                st.error(f"Could not Update the info of Customer . {e}")

                        elif id and btn2:
                            try:
                                db.delete(result)
                        
                                db.commit()
                                st.success("Customer info Delete Successfully")

                            except Exception as e:
                                st.error(f"Could not Delete the info of Customer . {e}")
                    db.close()

                elif selected_choice== choices[2]:
                    
                    st.subheader("Showing Customer Details")
                    db = open_db()
                    invoice_list= db.query(Customer)
                    
                    for item in invoice_list:
                        st.markdown(f'''
                        ##### Invoice id - {item.id}
                        - ###### First Name - {item.firstname}
                        - ###### Last Name - {item.lastname}
                        - ###### Mobile Number - {item.mobilephone}
                        - ###### E-mail - {item.emailaddress}
                        - ###### Pharmacy Name - {item.pharmacyname}
                        - ###### Age - {item.age}
                        - ###### Address - {item.address}
                        
                        
                        ''')
                    db.close()  
                
            elif selected_choice==choices[3]:
                st.subheader('Invoice')

                choices = ['Add Invoice Details','Update and Delete Invoice Details','Show Invoice Details',]
                selected_choice = st.selectbox("select an option",options=choices)

                if selected_choice== choices[0]:
                    with st.form('Add Invoice Details'):
                        col1, col2 = st.columns(2)
                        with col2:
                            date=st.date_input(label="Date")
                        with col1:
                            id=st.number_input(label="Invoice ID",value=0)

                        radio=st.radio(label="Payment Type",options=["cash","online"])

                        col1, col2 = st.columns(2)
                        with col1:
                            totalAmount=st.number_input(label="Total Amount")
                        with col2:
                            discount =st.number_input(label="Discount",value=0)
                            

                        
                        payedAmount=st.number_input(label="Payed Amount")

                        newprice=totalAmount*(1-(discount/100))
                        
                        remainingAmount = newprice-payedAmount

                        btn= st.form_submit_button("Submit")
                    
                    if id and btn :
                        try:
                            db=open_db()
                            c1=Invoice(id=id,date=date, paymenttype=radio, totalamount=totalAmount,payedamount=payedAmount,newprice=newprice,discount=discount,remainingamount=remainingAmount)
                            db.add(c1)
                            db.commit()
                            st.success("Invoice info save Successfully")

                            st.markdown(f'''
                            ##### Invoice id - {id}
                            - ###### Date - {date}
                            - ###### Payment Type - {radio}
                            - ###### Total Price - {totalAmount}
                            - ###### Discount - {discount}
                            - ###### Payable Price - {newprice}
                            - ###### Payed Amount - {payedAmount}
                            - ###### Remaining Amount - ({remainingAmount})
                                            
                            ''')

                            db.close()

                        except Exception as e:
                            st.error(f"Could not save the info of Invoice . {e}")

                elif selected_choice==choices[1]:
                    st.subheader('Update Invoice Details')

                    id = st.number_input("Invoice ID",value=0)
                    db = open_db()
                    result = db.query(Invoice).get(id)
                    if not result:
                        st.warning("first fill the Invoice ID.")
                    else:
                        with st.form("add Invoice"):
                        
                        
                            date=st.date_input(label="Date",value=result.date)
                            

                            radio=st.radio(label="Payment Type",options=["cash","online"])

                            col1, col2 = st.columns(2)
                            with col1:
                                totalAmount=st.number_input(label="Total Amount",value=result.totalamount)
                            with col2:
                                discount =st.number_input(label="Discount",value=result.discount)
                                

                            
                            payedAmount=st.number_input(label="Payed Amount",value=result.payedamount)

                            newprice=totalAmount*(1-(discount/100))
                            
                            remainingAmount = newprice-payedAmount

                            col1,col2,col3,col4 = st.columns(4)
                            with col1:
                                pass 
                            with col2:
                                btn1= st.form_submit_button("Update")
                                
                            with col3:
                                btn2= st.form_submit_button("Delete")

                            with col4:
                                pass 
                        
                        if id and btn1:
                            try:
                                result.date=date
                                result.paymenttype=radio
                                result.totalamount=totalAmount
                                result.discount=discount
                                result.payedamount=payedAmount
                                result.newprice=newprice
                                result.remainingamount=remainingAmount
                                db.commit()
                                st.success("Invoice info Update Successfully")

                                st.markdown(f'''
                                ##### Invoice id - {id}
                                - ###### Date - {date}
                                - ###### Payment Type - {radio}
                                - ###### Total Price - {totalAmount}
                                - ###### Discount - {discount}
                                - ###### Payable Price - {newprice}
                                - ###### Payed Amount - {payedAmount}
                                - ###### Remaining Amount - ({remainingAmount})
                                                    
                                ''')
                        
                            except Exception as e:
                                st.error(f"Could not Update the info of Invoice . {e}")

                        elif id and btn2:
                            try:
                                db.delete(result)
                        
                                db.commit()
                                st.success("Customer info Delete Successfully")

                            except Exception as e:
                                st.error(f"Could not Delete the info of Customer . {e}")
                    db.close()
                    
                elif selected_choice== choices[2]:
                    st.subheader("Showing Invoice Details")
                    db = open_db()
                    invoice_list= db.query(Invoice)
                    for item in invoice_list:
                        st.markdown(f'''
                        ##### Invoice id - {item.id}
                        - ###### Date - {item.date}
                        - ###### Payment Type - {item.paymenttype}
                        - ###### Total Price - {item.totalamount}
                        - ###### Discount - {item.discount}
                        - ###### Payable Price - {item.newprice}
                        - ###### Payed Amount - {item.payedamount}
                        - ###### Remaining Amount - {item.remainingamount}
                        
                        
                        ''')

                    db.close()

            elif selected_choice== choices[4]:
                st.subheader("Show Detalis")

                choices = ['Show Supplier Details','Show Drug Details','Show Invoice Details','Show Customer Details',]
                selected_choice = st.selectbox("select an option",options=choices)

                if selected_choice== choices[0]:
                    st.subheader("Showing Supplier Details")
                    db = open_db()
                    supplier_list= db.query(Supplier)
                    for item in supplier_list:
                        st.markdown(f'''
                        ##### supplier id - {item.id}
                        - ###### Company name - {item.companyname}
                        - ###### Mobile Number - {item.mobilephone}
                        - ###### E-mail - {item.emailaddress}
                        - ###### Address - {item.address}
                        - ###### City - {item.city}
                        ''')

                    db.close()
                    
                elif selected_choice== choices[1]:
                    st.subheader("Showing Drug Details")
                    db = open_db()
                    drug_list= db.query(Drug)
                    for item in drug_list:
                        st.markdown(f'''
                        ##### Drug id - {item.id}
                        - ###### Name - {item.name}
                        - ###### Scientific Name - {item.scientificname}
                        - ###### Manufacturer - {item.manufacturer}
                        - ###### Unitprice - {item.unitprice}
                        - ###### No_Of_Units_In_Package - {item.no_of_units_in_package}
                        - ###### Storage Temperature - {item.storagetemperature}
                        - ###### Dangerous Level - {item.dangerouslevel}
                        - ###### Storage Location - {item.storagelocation}
                        
                        ''')

                    db.close()

                elif selected_choice== choices[2]:
                    st.subheader("Showing Invoice Details")
                    db = open_db()
                    invoice_list= db.query(Invoice)
                    for item in invoice_list:
                        st.markdown(f'''
                        ##### Invoice id - {item.id}
                        - ###### Date - {item.date}
                        - ###### Payment Type - {item.paymenttype}
                        - ###### Total Price - {item.totalamount}
                        - ###### Discount - {item.discount}
                        - ###### Payable Price - {item.newprice}
                        - ###### Payed Amount - {item.payedamount}
                        - ###### Remaining Amount - {item.remainingamount}
                        
                        
                        ''')

                    db.close()

                elif selected_choice== choices[3]:
                    
                    st.subheader("Showing Customer Details")
                    db = open_db()
                    invoice_list= db.query(Customer)
                    
                    for item in invoice_list:
                        st.markdown(f'''
                        ##### Invoice id - {item.id}
                        - ###### First Name - {item.firstname}
                        - ###### Last Name - {item.lastname}
                        - ###### Mobile Number - {item.mobilephone}
                        - ###### E-mail - {item.emailaddress}
                        - ###### Pharmacy Name - {item.pharmacyname}
                        - ###### Age - {item.age}
                        - ###### Address - {item.address}
                        
                        
                        ''')
                    db.close()      

        else:
            st.error("! User id or Password are incorrect")

elif choice=="Sign up":
    st.subheader("create New Account")
    new_user=st.text_input("Username")
    new_password=st.text_input("Password",type='password')
    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user,new_password)
        st.success("You have sucessssfully created a valid account")
        st.info("Go to login menu to login")

