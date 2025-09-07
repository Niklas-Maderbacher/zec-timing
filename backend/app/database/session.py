from sqlalchemy import create_engine 
from sqlalchemy.engine import URL 
from sqlalchemy.orm import sessionmaker 
 
url = URL.create( 
    drivername="postgresql+psycopg", 
    username="postgres", 
    password="postgres", 
    host="localhost", 
    database="mydb", 
    port=5432 
) 
 
engine = create_engine(url) 
Session = sessionmaker(bind=engine) 
session = Session() 
