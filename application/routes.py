
from flask import request, jsonify
import json
from datetime import datetime
from functools import wraps

from . import app
from . import mongodb
from . import bcrypt
from . import admin_routes

def save_logs(logs):
    mongodb.insert_one(collection_name='Logs',
                       document=logs)
    
def request_controller_decorator(f):
    @wraps(f)
    def wrapper():
        logs = {
            'Method': request.method,
            'Url': request.url,
            'ClientIp': request.remote_addr,
            'Endpoint': request.endpoint,
            'TransactionDate': datetime.now()
            }

        if request.method != 'POST':
            msg = 'Only POST requests are accepted.'
            logs['Result'] = msg
            logs['UserNo'] = None
            save_logs(logs)
            return msg
        
        if not ('UserNo' in request.headers and 'Authorization' in request.headers):
            msg = 'UserNo and Authorization are required for process.'
            logs['Result'] = msg
            logs['UserNo'] = None
            save_logs(logs)
            return msg
        
        auth_code = request.headers.get('Authorization')
        user_no = int(request.headers.get('UserNo'))
        user_info = mongodb.find_documents(collection_name='Documents',
                                           query={'userNo': user_no},
                                           data={'authCode': 1, 'onProcess': 1})
        logs['UserNo'] = user_no
        if len(user_info) == 0:
            msg = 'User not found!'
            logs['Result'] = msg
            save_logs(logs)
            return msg
        user_info = user_info[0]
        control = bcrypt.check_password_hash(user_info['authCode'], auth_code)
        if control:
            msg = 'Permission denied!'
            logs['Result'] = msg
            save_logs(logs)
            return msg
        
        if user_info['onProcess']:
            msg = "This user is currently engaged in another transaction."
            logs['Result'] = msg
            save_logs(logs)
            return msg
        
        mongodb.update_document(collection_name='Documents', 
                                        query={'userNo': user_no}, 
                                        update_data={'onProcess': True})
        result = f()
        mongodb.update_document(collection_name='Documents', 
                                query={'userNo': user_no}, 
                                update_data={'onProcess': False})
        if isinstance(result, str):
            logs['Result'] = result
        else:
            logs['Result'] = 'The process has been successfully completed.'
        save_logs(logs)
        return result
        
    return wrapper
    

@app.route('/add-new-card', methods=['POST'])
@request_controller_decorator
def add_new_card():
    user_no = int(request.headers.get('UserNo'))

    try:
        data = json.loads(request.get_json())
        card_number = data['Card']
        is_selected = data['IsSelected']
    except:
        return "For this operation, Card and IsSelected information are required!"

    doc = mongodb.find_documents(collection_name='Documents',
                                    query={'userNo': user_no})[0]
    if is_selected:
        doc['selectedCard'] = card_number
    saved_flag = False
    if card_number not in doc['allCards']:
        doc['allCards'].append(str(card_number))
        saved_flag = True
    doc['updatedOn'] = datetime.now()
    mongodb.update_document(collection_name='Documents', query={'userNo': user_no}, update_data=doc)
    if saved_flag:
        return 'The new card have been successfully added.'
    return 'The card is already exists'

@app.route('/payment', methods=['POST'])
@request_controller_decorator
def payment():
    user_no = int(request.headers.get('UserNo'))
    data = json.loads(request.get_json())

    card_number = data['Card']
    is_selected = data['IsSelected']
    total_amount = data['TotalAmount']

    doc = mongodb.find_documents(collection_name='Documents',
                                query={'userNo': user_no})[0]
    
    if total_amount > doc['balance']:
        return "Insufficient balance!"
    
    doc['allCards'].append(str(card_number))
    if is_selected:
        doc['selectedCard'] = card_number

    doc['balance'] = doc['balance'] - total_amount

    doc['updatedOn'] = datetime.now()

    mongodb.update_document(collection_name='Documents', query={'userNo': user_no}, update_data=doc)

    return 'Payment successfully completed. The new card have been successfully saved.'

@app.route('/refund', methods=['POST'])
@request_controller_decorator
def refund():
    user_no = int(request.headers.get('UserNo'))
    data = json.loads(request.get_json())
    refund_amount = data['RefundAmount']
    doc = mongodb.find_documents(collection_name='Documents',
                                    query={'userNo': user_no})[0]
    doc['balance'] = doc['balance'] + refund_amount
    doc['updatedOn'] = datetime.now()
    mongodb.update_document(collection_name='Documents', query={'userNo': user_no}, update_data=doc)
    return 'Refund completed successfully.'


@app.route('/list-card-info', methods=['POST'])
@request_controller_decorator
def list_card_info():
    user_no = int(request.headers.get('UserNo'))
    doc = mongodb.find_documents(collection_name='Documents',
                                    query={'userNo': user_no})[0]
    return {
        'userNo': doc['userNo'],
        'allCards': doc['allCards'],
        'selectedCard': doc['selectedCard']
    }
    
@app.route('/health')
def health_check():
    return '200'