import sqlite3


con = sqlite3.connect("dataset3.db")
cur = con.cursor()

#Problem 26  Create a Rides table / collection with the fields defined above.
cur.execute('''
    CREATE TABLE Rides (
    id INT PRIMARY KEY,
    driver_id INT,
    passenger_id INT,
    start_location VARCHAR(255),
    end_location VARCHAR(255),
    distance DECIMAL(5,2),
    ride_time DECIMAL(5,2),
    fare DECIMAL(6,2)
)''')

## Problem 26 Insert five rows / documents into the Rides table / collection with data of your choice.
data=[
    (1, 101, 201, 'Start A', 'End A', 5.2, 15, 12.50),
    (2, 102, 202, 'Start B', 'End B', 8.3, 22, 18.75),
    (3, 103, 203, 'Start C', 'End C', 3.7, 10, 8.25),
    (4, 104, 204, 'Start D', 'End D', 9.1, 25, 21.00),
    (5, 105, 205, 'Start E', 'End E', 7.0, 20, 16.50)
]

for row in data:
    cur.execute('INSERT INTO Rides (id, driver_id, passenger_id, start_location, end_location, distance, ride_time, fare) VALUES (?,?,?,?,?,?,?,?)',row)

con.commit()

## Problem 28 Write a query to fetch all rides, ordered by fare in descending order.
cur.execute('SELECT * FROM Rides ORDER BY fare DESC')
res=cur.fetchall()
for row in res:
    print(row)

#Problem 29 Write a query to calculate the total distance and total fare for all rides.
cur.execute('SELECT SUM(distance) AS total_distance,SUM(fare) AS total_fare FROM Rides')
res=cur.fetchone()

total_distance=res[0]
total_fare=res[1]
print(f"Total Distance:{total_distance} , Total Fare: {total_fare}")


## Problem 30 Write a query to calculate the average ride_time of all rides.
cur.execute('SELECT AVG(ride_time) AS average_ride_time FROM Rides')
res=cur.fetchone()
print(f'Average Ride Time: {res[0]}')

## Problem 31 Write a query to fetch all rides whose start_location or end_location contains 'Downtown'.
cur.execute('SELECT * FROM Rides WHERE start_location LIKE "%Downtown%" OR end_location LIKE "%Downtown%"')
res=cur.fetchall()
for row in res:
    print(row)

## Problem 32 Write a query to count the number of rides for a given driver_id
cur.execute('SELECT driver_id,COUNT(*) AS ride_count FROM Rides GROUP BY driver_id')
res=cur.fetchall()
for row in res:
    print(row)

# ##Problem 33 Write a query to update the fare of the ride with id 4.
# cur.execute('UPDATE Rides SET fare=27.00 WHERE id=4')

##Problem 34 Write a query to calculate the total fare for each driver_id
cur.execute('SELECT driver_id, SUM(fare) AS total_fare FROM Rides GROUP BY driver_id')
res=cur.fetchall()
for row in res:
    print(row)

##Problem 35 Write a query to delete the ride with id 2.
cur.execute('DELETE FROM Rides WHERE id=2')




con.close()
