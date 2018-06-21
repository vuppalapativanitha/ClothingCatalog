from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, ClothingDB, User

engine = create_engine('sqlite:///ClothingCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="admin", email="vuppalapativanitha@gmail.com")
session.add(User1)
session.commit()

# Dummy books data
product1 = ClothingDB(
         productName="Designer Kurti",
         coverUrl="static/images/kurti.jpg",
         description="Daily wear kurti yet a royal one", category="Kurti",
         user_id=1)

session.add(product1)
session.commit()

product2 = ClothingDB(
         productName="Designer Saree",
         coverUrl="static/images/saree.jpg",
         description="A Saree with a class look ", category="Saree",
         user_id=1)

session.add(product2)
session.commit()

product3 = ClothingDB(
         productName="Punjabi Patiala",
         coverUrl="static/images/patiala.jpg",
         description="A Royal One", category="patiala", user_id=1)

session.add(product3)
session.commit()

product4 = ClothingDB(
         productName="Anarkali",
         coverUrl="static/images/anarkali.jpg",
         description="Indian Ethnic wear", category="Anarkali", user_id=1)

session.add(product4)
session.commit()

product5 = ClothingDB(
         productName="Bridal Lehenga",
         coverUrl="static/images/lehenga.jpg",
         description="Makes Your Wedding More Colorful",
         category="Lehenga", user_id=1)

session.add(product5)
session.commit()


print ("added Products!")
