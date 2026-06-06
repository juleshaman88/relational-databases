from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///shop.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    shipped = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="orders")
    product = relationship("Product")

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

user1 = User(name="Alice Smith", email="alice@example.com")
user2 = User(name="Bob Johnson", email="bob@example.com")

prod1 = Product(name="Laptop", price=1000)
prod2 = Product(name="Smartphone", price=500)
prod3 = Product(name="Headphones", price=150)

session.add_all([user1, user2, prod1, prod2, prod3])
session.commit()

order1 = Order(user_id=user1.id, product_id=prod1.id, quantity=1, shipped=True)
order2 = Order(user_id=user1.id, product_id=prod3.id, quantity=2, shipped=False)
order3 = Order(user_id=user2.id, product_id=prod2.id, quantity=1, shipped=True)
order4 = Order(user_id=user2.id, product_id=prod3.id, quantity=1, shipped=False)

session.add_all([order1, order2, order3, order4])
session.commit()

print("-- 1. All Users ---")
users = session.query(User).all()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")

print("\n-- 2. All Products ---")
products = session.query(Product).all()
for product in products:
    print(f"Product: {product.name}, Price: {product.price}")

print("\n-- 3. All Orders ---")
orders = session.query(Order).all()
for order in orders:
    print(f"Order ID: {order.id}, User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}")

print("\n--- 4. Update Product Price (Laptop to $1200) ---")
laptop = session.query(Product).filter(Product.name == "Laptop").first()
if laptop:
    laptop.price = 1200
    session.commit()
    print(f"Updated {laptop.name} price to ${laptop.price}")
else:
    print("Laptop not found")

print("\n--- Unshipped Orders ---")
unshipped_orders = session.query(Order).filter(Order.shipped == False).all()
for order in unshipped_orders:
    print(f"Unshipped Order ID: {order.id}, User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}")\
    
print("\n--- Total Orders Per User ---")
order_counts = session.query(User.name, func.count(Order.id)).join(Order).group_by(User.id).all()
for name, count in order_counts:
    print(f"User: {name}, Total Orders: {count}")

print("\n--- Delete User by ID ---")
user_to_delete = session.query(User).filter(User.id == 2).first()
if user_to_delete:
    session.delete(user_to_delete)
    session.commit()
    print(f"Deleted user with ID: {user_to_delete.id}")

print("\n--- Remaining Users ---")
remaining_users = session.query(User).all()
for user in remaining_users:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")

session.close()