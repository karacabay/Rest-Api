


from flask import request
import json
from datetime import datetime

from . import app
from . import mongodb
from . import bcrypt


@app.route('/create-admin-user', methods=['POST'])
def create_admin_user():

    if request.method == 'POST':
        password = request.headers.get('Password')
        admin_name = request.headers.get('Admin')

        hashed_password = bcrypt.generate_password_hash(password)
        mongodb.insert_one(collection_name='Admin',
                           document={
                               'Admin': admin_name, 
                               'Password': hashed_password
                               })

        return 'New admin user created!'
    

@app.route('/add-new-document', methods=['POST'])
def add_document():

    if request.method == 'POST':
        candidate_password = request.headers.get('Password')
        admin_name = request.headers.get('Admin')
        document = json.loads(request.get_json())

        data = mongodb.find_documents(collection_name='Admin',
                                      query={'Admin': admin_name})
        
        if len(data) == 0:
            return 'Permission denied!'
        
        admin_data = data[0]
        hs_password = admin_data['Password']
        control = bcrypt.check_password_hash(hs_password, candidate_password)
        if not control:
            return 'Permission denied!'
        
        for date_key in ['birthDate', 'createdOn', 'updatedOn']:
            document[date_key] = datetime.fromtimestamp(document[date_key])
        authCode = document['authCode']
        hashed_authCode = bcrypt.generate_password_hash(authCode)
        document['authCode'] = hashed_authCode
        document['OriginalAuthCode'] = authCode
        mongodb.insert_one(collection_name='Documents', document=document)

        return 'The new document have been successfully added.'