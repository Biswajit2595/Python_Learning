import sqlite3

con=sqlite3.connect("dataset3.db")
cur=con.cursor()


cur.execute('SELECT * FROM Rides')
res=cur.fetchall()
for row in res:
    print(row)

#Problem 36 Write a query to find the ride with the highest and lowest fare
cur.execute('SELECT * FROM Rides ORDER BY fare DESC LIMIT 1')
res=cur.fetchone()
print(f'Ride with highest fare: {res}')
cur.execute('SELECT * FROM Rides ORDER BY fare ASC LIMIT 1')
res=cur.fetchone()
print(f'Ride with lowest fare: {res}')

##Problem 37 Write a query to find the average fare and distance for each driver_id
cur.execute('SELECT driver_id, AVG(fare) AS average_fare,AVG(distance) AS average_distance FROM Rides GROUP BY driver_id')
res=cur.fetchall()
for row in res:
    print(f'Driver id: {row[0]} with Average fare {row[1]} and Average Distance {row[2]}')

##Problem 38 Write a query to find driver_id that have completed more than 5 rides
cur.execute('SELECT driver_id, COUNT(*) AS ride_count FROM Rides GROUP BY driver_id HAVING COUNT(*)>5')

##Problem 39 Assuming there is another collection/table called Drivers with driver_id and name fields, write a query to find the name of the driver with the highest fare.
cur.execute('SELECT D.name FROM AS R INNER JOIN Drivers AS D ON R.driver_id=D.driver_id ORDER BY R.fare DESC LIMIT 1')
res=cur.fetchall()
print(res)

##Problem 40 Write a query to find the top 3 drivers who have earned the most from fares. Return the drivers' ids and total earnings.
cur.execute('SELECT driver_id, SUM(fare) AS total_earnings FROM Rides GROUP BY driver_id ORDER BY total_earnings DESC LIMIT 3')
res=cur.fetchall()
for r in res:
    print(f'Driver ID:{r[0]} has earned total of {r[1]}')

##Problem 41 Assuming there's a ride_date field of date type in the Rides table / collection, write a query to find all rides that happened in the last 7 days.
cur.execute('SELECT * FROM Rides WHERE ride_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)')
res=cur.fetchall()
print(res)

##Problem 42 Write a query to find all rides where the end_location is not set.
cur.execute('SELECT * FROM Rides WHERE end_location IS NULL OR end_location =""')
res=cur.fetchall()
for r in res:
    print(r)

##Problem 43 Write a query to calculate the fare per mile for each ride and return the ride ids and their fare per mile, ordered by fare per mile in descending order.
cur.execute('SELECT id, ROUND((fare / distance), 2) AS fare_per_mile FROM Rides ORDER BY fare_per_mile DESC')
res=cur.fetchall()
for r in res:
    print(f'Id:{r[0]} has per mile fare of {r[1]}')

##Problem 44 Assuming there's another collection/table Passengers with passenger_id and name fields, write a query to return a list of all rides including the driver's name and passenger's name.
cur.execute('SELECT R.id, R.start_location, R.end_location, R.distance, R.fare, R.driver_id, D.name AS driver_name, R.passenger_id, P.name AS passenger_name FROM Rides AS R INNER JOIN Drivers AS D ON R.driver_id = D.driver_id INNER JOIN Passengers AS P ON R.passenger_id = P.passenger_id;')
res=cur.fetchall()

##Problem 45 Write a query to add a tip field to the Rides table / collection.
cur.execute('ALTER TABLE Rides ADD COLUMN tip DECIMAL(6,2)')
con.commit()

con.close()