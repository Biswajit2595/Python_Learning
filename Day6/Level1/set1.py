import sqlite3

# Connect to the database (creates a new database if it doesn't exist)
con = sqlite3.connect("my_data.db")

# Create a cursor object to interact with the database
cur = con.cursor()

#Problem 1 Create a Customers table with fields id, name, email, address, and phone_number.
cur.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    address TEXT,
    phone_number TEXT
)''')

#Problem 2 Insert five rows / documents into the Customers table / collection with data of your choice.
data = [
    ('John Smith', 'john@example.com', '123 Main St, City, Country', '+1 (123) 456-7890'),
    ('Jane Doe', 'jane@example.com', '456 Elm St, Town, Country', '+1 (987) 654-3210'),
    ('Alice Johnson', 'alice@example.com', '789 Oak St, Village, Country', '+1 (555) 123-4567'),
    ('Bob Brown', 'bob@example.com', '101 Pine St, Hamlet, Country', '+1 (777) 888-9999'),
    ('Eva Williams', 'eva@example.com', '246 Willow St, Town, Country', '+1 (222) 333-4444')
]

for row in data:
    cur.execute('INSERT INTO Customers (name, email, address, phone_number) VALUES (?, ?, ?, ?)', row)

#Insert data into the table
con.commit()


#Problem 3 Write a query to fetch all data from the Customers table / collection.
cur.execute('SELECT * FROM Customers')
result = cur.fetchall()

for row in result:
    print(row)


#Problem 4 Write a query to select only the name and email fields for all customers.
cur.execute('SELECT name,email FROM Customers')
result = cur.fetchall()

for row in result:
    print(row)

#Problem 5 Write a query to fetch the customer with the id of 3.
cur.execute('SELECT * FROM Customers WHERE id = 3')
result=cur.fetchall()

for row in result:
    print(row)

#Problem 6 Write a query to fetch all customers whose name starts with 'A'
cur.execute('SELECT * FROM Customers WHERE name LIKE "A%"')
res=cur.fetchall()
for row in res:
    print(row)

#Problem 7 Write a query to fetch all customers, ordered by name in descending order.
cur.execute('SELECT * FROM Customers ORDER BY name DESC')
res=cur.fetchall()
for row in res:
    print(row)

#Problem 8 Write a query to update the address of the customer with id 4.
cur.execute('UPDATE Customers SET address="New Address" WHERE id=4')

#Problem 9 Write a query to fetch the top 3 customers when ordered by id in ascending order.
cur.execute('SELECT * FROM Customers ORDER BY id ASC LIMIT 3')
print(*cur.fetchall())

#Problem 10 Write a query to delete the customer with id 2.
cur.execute('DELETE FROM Customers WHERE id=2')

#Problem 11 Write a query to count the number of customers.
cur.execute('SELECT COUNT(*) FROM Customers')
res=cur.fetchone()
print(res[0])

#Problem 12 Write a query to fetch all customers except the first two when ordered by id in ascending order.
cur.execute('SELECT * FROM Customers ORDER BY id ASC OFFSET 2')
res=cur.fetchall()
print(res)

#Problem 13 Write a query to fetch all customers whose id is greater than 2 and name starts with 'B'
cur.execute('SELECT * FROM Customers WHERE id>2 AND name LIKE "B%"')
res=cur.fetchall()
print(res)

#Problem 14 Write a query to fetch all customers whose id is less than 3 or name ends with 's'.
cur.execute('SELECT * FROM Customers WHERE id<3 OR name LIKE "%s"')
res=cur.fetchall()
print(res)


#Problem 15 Write a query to fetch all customers where the phone_number field is not set or is null.
cur.execute('SELECT * FROM Customers WHERE phone_number IS NULL OR phone_number=""')
res=cur.fetchall()

for row in res:
    print(row)

# Close the database connection
con.close()
