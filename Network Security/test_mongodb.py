
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://vaishnavisoni1723:admin123@cluster0.qfyxq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)





    '''
    The uri (Uniform Resource Identifier) in this context is a connection string used 
    to provide the necessary details for connecting to a MongoDB database.
python
Copy
Edit
uri = "mongodb+srv://vaishnavisoni1723:admin123@cluster0.qfyxq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
Components of the URI
1. mongodb+srv://
Specifies the protocol used for the connection.
+srv indicates that the URI uses the DNS Seed List format to connect to a MongoDB cluster instead of a standalone server.
This makes it easier to manage clusters, as it automatically resolves the appropriate cluster node to connect to.



3. @cluster0.qfyxq.mongodb.net
This is the host address for your MongoDB Atlas cluster.
cluster0: The cluster name.
qfyxq: A unique identifier for your cluster, provided by MongoDB Atlas.


4. /?retryWrites=true&w=majority&appName=Cluster0
These are additional query parameters for configuring the connection:
retryWrites=true: Enables automatic retries of failed write operations (useful for transient errors like network issues).
w=majority: Ensures write operations are acknowledged by a majority of the nodes in the cluster, increasing data safety.
appName=Cluster0: Specifies the application name for monitoring purposes in MongoDB Atlas.
Purpose of the URI
The URI provides all the necessary information to:

Identify which MongoDB cluster to connect to (cluster0.qfyxq.mongodb.net).
Authenticate the connection (vaishnavisoni1723:admin123).
Configure the connection behavior (e.g., retry failed writes, use majority write acknowledgment).

    '''
