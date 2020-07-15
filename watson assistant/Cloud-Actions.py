import sys
import ibm_db
from cloudant import Cloudant
from cloudant.result import Result, ResultByKey
 
def main(dict):
    try:
        db_name = 'mydb'
        client = Cloudant.iam("4f190e31-fe6b-4254-9f74-5da1ac78d3ed-bluemix","Gzezz92858RutHg7fMbfd-mzcUIw_DaeYpMHriZKYsfC",connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
        # Create document content data
        {
        "selector": {
                "cname": "ibm"
            },
            "fields" : [
                "cquestion"
                ]
            }
        

        docs = db.get_query_result(selector)
        return {"msg":docs}


# Check that the document exists in the database
        if my_document1.exists():
            qOne = "Success!!"
            return { "msg" : qOne }
            
    finally:
          client.disconnect()
          