# -*- coding: cp1252 -*-
from bottle import route, run, debug, request, response
import json
import sqlite3
import time


class ChatKit:
    def __init__(self):
        self.db = 'chkit_DB.db'

    def add_msg(self, user_id, room_id, msg, m_time, tmpID):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        casted = 0

        # Adding Query
        query = "INSERT INTO messages(user_id,room_id,text, casted, m_timestamp, tmpID ) VALUES (?,?,?,?,?,?)"
        cur.execute(query, (user_id, room_id, msg,casted, m_time, tmpID,))

        conn.commit()
        cur.close()
        return 'done'
    def add_room(self, room_name):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        # Adding Query
        query = "INSERT INTO rooms(room_name) VALUES (?)"
        cur.execute(query, (room_name,))

        conn.commit()
        cur.close()
        return
    def get_messages(self, room_id):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        # Get messages Query
        query = "SELECT * FROM messages WHERE room_id = ?"
        raw_data = cur.execute(query, (room_id,))

        messages = []

        for f in raw_data:
            message_arr =  {
                'id': f[0],
                'userID':f[1],
                'roomID':f[2],
                'text':f[3],
                'timestamp':f[4]
                }
            messages.append(message_arr)

        return messages
    def get_messages_by_user(self, user_id):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        # Get messages Query
        query = "SELECT * FROM messages WHERE user_id = ?"
        raw_data = cur.execute(query, (user_id,))

        messages = []

        for f in raw_data:
            message_arr =  {
                'id': f[0],
                'userID':f[1],
                'roomID':f[2],
                'text':f[3],
                'timestamp':f[4]
                }
            messages.append(message_arr)

        return messages
    def get_messages_by_msg(self, msg_id):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        # Get messages Query
        query = "SELECT * FROM messages WHERE id = ?"
        raw_data = cur.execute(query, (msg_id,))

        messages = []

        for f in raw_data:
            message_arr =  {
                'id': f[0],
                'userID':f[1],
                'roomID':f[2],
                'text':f[3],
                'casted':f[4],
                'timestamp':f[5]
                }
            messages.append(message_arr)

        return messages
    def get_uncasted_messages(self, room_id):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        # Get messages Query
        query = "SELECT * FROM messages WHERE room_id = ? AND casted = 0 "
        raw_data = cur.execute(query, (room_id,))

        messages = []

        for f in raw_data:
            message_arr =  {
                'id': f[0],
                'userID':f[1],
                'roomID':f[2],
                'text':f[3],
                'casted':f[4],
                'timestamp':f[5],
                'tmpID':f[6]
                }
            messages.append(message_arr)

        return messages
    def set_casted(self, msg_id):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        # Get messages Query
        query = "UPDATE messages SET casted = 1, tmpID = null WHERE id = ?"
        cur.execute(query, (msg_id,))

        conn.commit()
        cur.close()
        return "done"

c = ChatKit()

@route('/message/', method="POST")
def message():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    
    body = request.body.read().decode('utf8') # read directly HTTP input
    get_dict = json.loads(body) # decode json and get native python dict
    userID = get_dict['userID']
    tmpID = get_dict['tmpID']
    roomID = get_dict['roomID']
    msg = get_dict['text']
    m_time = time.strftime("%d-%m-%Y-%H-%M-%S")
    ret = c.add_msg(userID,
                    roomID,
                    msg,
                    m_time,
                    tmpID)
               
    return ret

@route('/room/<r_name>')
def room(r_name):
    c.add_room(r_name)
    return ("done adding room "+r_name)

@route('/get_messages/<room_id:int>/')
def get_messages(room_id):
    #Get messages by room id
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.content_type = 'application/json'

    dumped = json.dumps(c.get_messages(room_id))
    return json.dumps(c.get_messages(room_id))


@route('/get_stream/<room_id:int>/')
def get_stream(room_id):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.headers["Cache-Control"] = "no-cache"
    response.content_type = "text/event-stream"

    ret_msgs = []
    for i in c.get_uncasted_messages(room_id):
        c.set_casted(i['id'])
        print i
        ret_msgs.append(i)
    if ret_msgs == []:
        return
    else:
        yield "event:newMsg\ndata:%s\n\n"%(json.dumps(ret_msgs))

@route('/get_messages_by_user/<user_id>/')
def get_messages_by_user(user_id):
    print "dslk"
    #get messages by user id
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.content_type = 'application/json'

    dumped = json.dumps(c.get_messages_by_user(user_id))
    print c.get_messages_by_user(user_id)[1]
    return json.dumps(c.get_messages_by_user(user_id))

@route('/get_messages_by_msg/<msg_id>/')
def get_messages_by_msg(msg_id):
    print "dslk"
    #get messages by user id
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.content_type = 'application/json'

    dumped = json.dumps(c.get_messages_by_msg(msg_id))
    return json.dumps(c.get_messages_by_msg(msg_id))

import optparse
import sys
from gevent import monkey; monkey.patch_all()

if __name__=="__main__":
    parser = optparse.OptionParser("usage: %prog [options] arg1 arg2")
    parser.add_option("-H", "--host", dest="hostname",
                      default="127.0.0.1", type="string",
                      help="specify hostname to run on")
    parser.add_option("-p", "--port", dest="portnum", default=8090,
                      type="int", help="port number to run on")
    (options, args) = parser.parse_args()

   

    hostname = options.hostname
    portnum = options.portnum
try:
    run(server="gevent", host=hostname, port=portnum, reloader=True)
except KeyboardInterrupt:
    sys.exit(0)
