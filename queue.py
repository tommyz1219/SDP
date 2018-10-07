class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
		
#!/usr/bin/python
import MySQLdb
import time

q = Queue()

db = MySQLdb.connect(host="localhost",    #host, either localhost or 192.168.43.42
                     user="app",         #username
                     passwd="sdp",  #password
                     db="images")        #data base name

cursor = db.cursor()

#checks size of server before accessing
cursor.execute("SELECT COUNT(*) FROM imgnum")
for size in cursor.fetchone():
    print ("Inital row size: " + str(size))

db.close()    

#will only access if there are entries
hasRequests = 0    
while 1:
    print("waiting")
    #opens new connection so SQL table stays updated after receiving new requests
    db = MySQLdb.connect(host="localhost",    #host, either localhost or 192.168.43.42
                     user="app",         #username
                     passwd="sdp",  #password
                     db="images")        #data base name

    cursor = db.cursor()
    #checks if there are requests in imgnum table
    cursor.execute("SELECT COUNT(*) FROM imgnum")
    for size1 in cursor.fetchone():
        if size1 > 0:
            hasRequests = 1
            #print("check=1")

    time.sleep(2)        
    while hasRequests == 1:

        #gets requests from table by selecting all rows
        cursor.execute("SELECT * FROM imgnum")
        for row in cursor.fetchone():
            q.enqueue(row)
            print ("Value added to queue: " + row)
            cursor.execute("DELETE FROM imgnum WHERE name =%s limit 1", (row,))
            db.commit()

        #checks if there are still requests in present connection
        #if not, connection ends and while loop will exit
        cursor.execute("SELECT COUNT(*) FROM imgnum")
        for size2 in cursor.fetchone():
            print ("Row size after delete: " + str(size2))
            if size2 == 0:
                hasRequests = 0
                db.close()

        time.sleep(5)
        #ensures that if there are no more requests, board maintains last image
        print("Queue size before dequeue is: " + str(q.size()))
        if size2 > 0:
            print(q.dequeue())
        print("Queue size after is: " + str(q.size()))

