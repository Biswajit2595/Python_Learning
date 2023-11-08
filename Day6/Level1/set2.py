import sqlite3

# Connect to the database
con = sqlite3.connect("dataset2.db")
cur = con.cursor()

#Problem 16 Create a Restaurants table / collection with the fields defined above.
cur.execute('''
    CREATE TABLE Restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    cuisine_type VARCHAR(100),
    location VARCHAR(255),
    average_rating DECIMAL(3,2),
    delivery_available BOOLEAN
)''')

# Problem 17 Insert five rows / documents into the Restaurants table / collection with data of your choice.
data = [
    (1, 'Restaurant A', 'Italian', 'New York', 4.5, 1),
    (2, 'Restaurant B', 'Chinese', 'Los Angeles', 4.2, 1),
    (3, 'Restaurant C', 'Mexican', 'Chicago', 3.8, 0),
    (4, 'Restaurant D', 'Japanese', 'San Francisco', 4.7, 0),
    (5, 'Restaurant E', 'Indian', 'Houston', 4.0, 0)
]

for row in data:
    cur.execute('INSERT INTO Restaurants (id, name, cuisine_type, location, average_rating, delivery_available) VALUES (?, ?, ?, ?, ?, ?)', row)

# Commit the changes to the database
con.commit()

# Problem 18 Write a query to fetch all restaurants, ordered by average_rating in descending order
cur.execute('SELECT * FROM Restaurants ORDER BY average_rating DESC')
res = cur.fetchall()
for row in res:
    print(row)

# Problem 19 Write a query to fetch all restaurants that offer delivery_available and have an average_rating of more than 4.
cur.execute('SELECT * FROM Restaurants WHERE delivery_available=true AND average_rating>4')
res=cur.fetchall()
for row in res:
    print(row)
    
# Problem 20 Write a query to fetch all restaurants where the cuisine_type field is not set or is null.
cur.execute('SELECT * FROM Restaurants WHERE cuisine_type IS NULL OR cuisine_type=""')
res=cur.fetchall()
for row in res:
    print(row)

# Problem 21 Write a query to count the number of restaurants that have delivery_available.
cur.execute('SELECT COUNT(*) FROM Restaurants WHERE delivery_available=true')
res=cur.fetchone()
print(res[0])

# Problem 22 Write a query to fetch all restaurants whose location contains 'New York'.
cur.execute('SELECT * FROM Restaurants WHERE location lIKE "%New York%"')
res=cur.fetchall()
for row in res:
    print(row)

# Problem 23 Write a query to calculate the average average_rating of all restaurants.
cur.execute('SELECT AVG(average_rating) FROM Restaurants')
res=cur.fetchone()
print(res[0])

## Problem 24 Write a query to fetch the top 5 restaurants when ordered by average_rating in descending order.
cur.execute('SELECT * FROM Restaurants ORDER BY average_rating DESC LIMIT 5')
res=cur.fetchall()
for row in res:
    print(row)

## Problem 25 Write a query to delete the restaurant with id 3.
cur.execute('DELETE FROM Restaurants WHERE id=3')
con.commit()

# Close the database connection
con.close()

