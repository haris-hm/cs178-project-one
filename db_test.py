import pymysql
import creds 

def mysqlconnect():
    # To connect MySQL database
    conn = pymysql.connect(
        host= creds.host,
        user= creds.user, 
        password = creds.password,
        db=creds.db,
        )
    cur = conn.cursor()

    # Execute Query
    cur.execute(
        """
        SELECT * FROM Inventory        
        """)
    output = cur.fetchall()
    
    # Print Results
    for row in output:
        print(row[0], "\t", row[1], "\t", row[2], "\t", row[3])
      
    # To close the connection
    conn.close()
  
# Driver Code
if __name__ == "__main__" :
    mysqlconnect()