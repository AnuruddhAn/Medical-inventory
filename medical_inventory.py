from sqlalchemy import create_engine, Column,Integer,String,Float, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import VARCHAR, DateTime


Inventory= declarative_base()



class Supplier(Inventory):

    __tablename__ = "suppliers"

    id= Column(Integer, primary_key=True)
    companyname=Column(String)
    mobilephone = Column(Integer)
    emailaddress = Column(VARCHAR)
    address = Column(VARCHAR)
    city=Column(String)
    


class Drug(Inventory):

    __tablename__ = "drugs"

    id= Column(Integer, primary_key=True)
    name=Column(String)
    scientificname=Column(VARCHAR)
    # category=Column(String)
    manufacturer=Column(String)
    unitprice=Column(Float)
    no_of_units_in_package=Column(Integer)
    storagetemperature=Column(Float)
    dangerouslevel=Column(VARCHAR)
    storagelocation=Column(String)
    supplier=ForeignKey('Supplier')




class Customer(Inventory):

    __tablename__ = "customers"

    id= Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    mobilephone = Column(Integer)
    emailaddress = Column(VARCHAR)
    pharmacyname=Column(String)
    age=Column(Integer)
    address = Column(VARCHAR)
    

class Invoice(Inventory):

    __tablename__ = "invoices"

    id= Column(Integer, primary_key=True)
    date = Column(DateTime)
    paymenttype = Column(String)
    totalamount = Column(Float)
    discount = Column(Float)
    newprice = Column(Float)
    payedamount = Column(Float)
    remainingamount = Column(Float)
    drug=Column(Integer,ForeignKey('drugs.id'))
    customer=Column(Integer,ForeignKey('customers.id'))

if __name__ == "__main__":
    engine= create_engine('sqlite:///medical_inventory.sqlite3')
    Inventory.metadata.create_all(engine)