from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, redirect
import atexit
import os, io
import json
from google.cloud import vision
from google.cloud.vision import types

# Import working directory
dir_path = os.path.dirname(os.path.realpath('check.py'))

# Google vision setup
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = dir_path+'/GoogleV_C.json'
clientg = vision.ImageAnnotatorClient()


app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        # creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        # user = creds['username']
        # password = creds['password']
        # url =  creds['url']
        client = Cloudant.iam("4f190e31-fe6b-4254-9f74-5da1ac78d3ed-bluemix",
         "Gzezz92858RutHg7fMbfd-mzcUIw_DaeYpMHriZKYsfC",
         connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/upl')
def root():
    return app.send_static_file('index.html')


# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */


@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)



# File Upload


app.config["IMAGE_UPLOADS"] = dir_path+"/static/img"


@app.route("/", methods=["GET","POST"])
def upload_im():
        if request.method == "POST":

            if request.files:
                image1 = request.files["image"]

                image1.save(os.path.join(app.config["IMAGE_UPLOADS"], image1.filename))
                
                # print("Image saved")
                # with io.open(os.path.join(app.config["IMAGE_UPLOADS"], image1.filename))
                print(image1.filename)
                with io.open(os.path.join(app.config["IMAGE_UPLOADS"], image1.filename),'rb') as image_file:
                    content = image_file.read()

                image = vision.types.Image(content=content)
                respo = clientg.text_detection(image=image)
                print(respo)

                return redirect(request.url)

        return render_template("upload.html")


@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
