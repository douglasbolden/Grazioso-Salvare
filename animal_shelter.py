from pymongo import MongoClient
from bson.objectid import ObjectId

# The class is what we will call to make an instance of our database in our code.
class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """
    
    # Initializes the MongoClient. This helps to Access the MongoDB databases and collections. 
    def __init__(self, username, password):
        
        #The below line has user authentication, while the line below it skips user authentication.
        self.client = MongoClient('mongodb://%s:%s@localhost:47126' % (username, password))
        #self.client = MongoClient('mongodb://localhost:47126')
        # Set the database being used.
        self.database = self.client['AAC']
        
    # Implements the C in CRUD for creation.
    # Returns an Exception if data sent is empty. Inserts an entry if it isn't.
    # Data should be in the form of a dictionary.
    def create(self, data):
        if data is not None:
            self.database.animals.insert(data)
            return True
        else:
            print("Error Saving Entry")
            return False
    
    # Implements the R in CRUD for reading.
    # Returns a cursor that points to a list of results.
    # Must implement a loop to see all data.
    def read(self, data):
        if data is not None:
            # Cursor to loop through.
            cursor = self.database.animals.find(data, {'_id':False})
            return cursor
        else:
            print("Nothing Found.")
            return False
    
    # Implements the U in CRUD for updating.
    # Returns an exception if the data sent is incorrect.
    def update(self, data, newData):
        if data is not None:
            return self.database.animals.update(data, {"$set":newData})
        else:
            print("No data submitted.")
            return False
    
    # Implements the D in CRUD for deletion.
    # Returns an exception if the data sent is incorrect.
    def delete(self, data):
        if data is not None:
            return self.database.animals.delete_one(data)
        else:
            print("No data submitted.")
            return False
            
            