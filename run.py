#!/usr/bin/env python3
from flask import Flask, request, Response
import json
import uuid
import time
from functools import wraps
import random
import base64

app = Flask(__name__)

print("* Made by fhody125")
# -------- Load raw XML and encode to Base64 --------
with open('real_ss_info.txt', 'r', encoding='utf-8') as f:
    raw_xml = f.read().strip()
# Encode to Base64
SS_INFO_BASE64 = base64.b64encode(raw_xml.encode('utf-8')).decode('utf-8')

# -------- Helper for JSON responses with SP-RES-KIND --------
def json_response(data, status=200, sp_res_kind='0'):
    resp = Response(json.dumps(data), status=status, mimetype='application/json')
    resp.headers['SP-RES-KIND'] = sp_res_kind
    return resp

# -------- Logging decorator --------
def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("\n" + "="*60)
        print(f"[{request.method}] {request.path}")
        print(f"Headers: {dict(request.headers)}")
        body = request.get_data(as_text=True)
        if body:
            try:
                parsed = json.loads(body)
                print(f"Body: {json.dumps(parsed, indent=2)}")
            except:
                print(f"Body: {body}")
        else:
            print("Body: (empty)")
        print("="*60 + "\n")
        return func(*args, **kwargs)
    return wrapper

# -------- ss.info --------
@app.route('/bb-eu/ss.info', methods=['GET'])
@log_request
def serve_ss_info():
    resp = Response(SS_INFO_BASE64, mimetype='text/plain; charset=utf-8')
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    resp.headers['Content-Length'] = str(len(SS_INFO_BASE64))
    return resp

# -------- Login --------
@app.route('/basic_utils/login', methods=['POST'])
@log_request
def login():
    body = request.get_data(as_text=True)
    try:
        req = json.loads(body)
        platform_id = req.get('PlatformAccountId', str(random.randint(1000, 10000)))
    except:
        platform_id = str(random.randint(1000, 10000))

    response_data = {
        "ServerVersion": 1,
        "UserStatus": 0,
        "SessionId": str(uuid.uuid4()),
        "PlatformAccountId": platform_id,
        "LanguageId": 19.0,
        "UserId": random.randint(1000, 10000),
        "MessageId": "LoginResponse",
        "WarningMessage": "VGhpcyBzZXJ2ZXIgaXMgYSBmYWtlIHNlcnZlciwgdXNlZCBvbmx5IHRvIGFsbG93IHlvdSB0byBjb25uZWN0IHRvIHlvdXIgU2hhZG5ldCh3b3p6YXJkbWFuIHZlcnMpIHNlcnZlciAoZm9yIG1hdGNoIG1ha2luZyBvbmx5KSB3aXRob3V0IGFueSBkZXBlbmRlbmN5IG9uIHRoZSBodW50ZXJzIGRyZWFtIHNlcnZlcnMuCg====",
        "IssuerId": 100.0,
        "ResKind": 0
    }
    return json_response(response_data, sp_res_kind='0')

# -------- get_normal_notice --------
@app.route('/basic_utils/get_normal_notice', methods=['POST'])
@log_request
def get_normal_notice():
    response_data = {
        "NoticeList": [
            {
                "Title": "VGhlIEZhaGFkIERyZWFt",
                "Notice": "VGhlIEZhaGFkIERyZWFt=",
                "Id": 1
            }
        ],
        "ResKind": 0,
        "MessageId": "NoticeNormalGetResponse"
    }
    return json_response(response_data, sp_res_kind='0')

# -------- sync_chara_id --------
@app.route('/basic_utils/sync_chara_id', methods=['POST'])
@log_request
def sync_chara_id():
    response_data = {
        "PublishCharacterIdList": [],
        "ResKind": 0,
        "MessageId": "SyncCharaIdResponse"
    }
    return json_response(response_data, sp_res_kind='0')

# -------- penalty/check_user_priority_move_count --------
@app.route('/penalty/check_user_priority_move_count', methods=['POST'])
@log_request
def check_user_priority_move_count():
    response_data = {
        "ResKind": 0,
        "MessageId": "UserPropertiesMoveCountCheckResponse"
    }
    return json_response(response_data, sp_res_kind='0')

# -------- blood_messenger/exist_messages --------
@app.route('/blood_messenger/exist_messages', methods=['POST'])
@log_request
def blood_messenger_exist_messages():
    response_data = {
        "BloodMessEvaluationList": [],
        "LostBloodMessIdList": [],
        "ResKind": 0,
        "MessageId": "BloodMessSearchAddResponse"
    }
    return json_response(response_data, sp_res_kind='0')

# -------- get_emergency_notice --------
@app.route('/basic_utils/get_emergency_notice', methods=['POST'])
@log_request
def get_emergency_notice():
    return json_response({"ResKind": 0, "MessageId": "EmergencyNoticeGetResponse", "NoticeList": []}, sp_res_kind='0')

# -------- get_user_agreement --------
@app.route('/basic_utils/get_user_agreement', methods=['POST'])
@log_request
def get_user_agreement():
    return json_response({"ResKind": 0, "MessageId": "UserAgreementGetResponse", "Agreements": []}, sp_res_kind='0')

# -------- get_datetime --------
@app.route('/basic_utils/get_datetime', methods=['POST'])
@log_request
def get_datetime():
    return json_response({"ResKind": 0, "MessageId": "DateTimeResponse", "Timestamp": int(time.time() * 1000)}, sp_res_kind='0')

# -------- Catch-all for any other endpoint --------
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@log_request
def catch_all(path):
    if path == 'bb-eu/ss.info':
        return serve_ss_info()
    return json_response({"ResKind": 0}, sp_res_kind='0')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20443, debug=False)