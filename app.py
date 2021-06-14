from random import random
from flask import Flask,render_template,redirect,url_for,session
from flask.globals import request
from flask_socketio import SocketIO,join_room
from wtf_form import *
from models import * 
import random
import string
import datetime 
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
app.secret_key="fuckmf"
socketio = SocketIO(app)

@app.route("/",methods=['GET','POST'])
def index():
    reg_form = RegistrationForm()
    if request.method=='POST' and reg_form.validate():
        return redirect( url_for("login") ) 
    return render_template("index.html",reg_form=reg_form)

# @app.route("/testing",methods=["GET","POST"])
# def chatbox():
#     reg_form=RegistrationForm()
#     login_form=LoginForm()
#     return render_template("testing .html",reg_form=reg_form,login_form=login_form) 


@app.route("/login",methods=["GET","POST"])
def login():
    login_form=LoginForm()
    if request.method == 'POST' and login_form.validate():
        session['user']=request.form.get("username")
        print(session['user'])

        return redirect(url_for("room"))
    return render_template("login.html",login_form=login_form)



@app.route("/room")
def room():
    if session['user'] != None:
        return render_template('room.html')
    else:
        return redirect(url_for("login"))

@app.route("/room_id",methods=["GET"])
def room_id():
    if request.method=='GET' and "user" in session:
        room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        rooms.insert_one({"username":session['user'],"room_id":room_id,"timestamp":str(datetime.datetime.utcnow())})
        print(room_id,"Room id")
            
    else:
        return redirect(url_for("login"))
    return room_id
    




@app.route("/chat/<string:room_id>",methods=['GET'])
def chat(room_id):
    if room_id in get_roomid() and 'user' in session:
        return render_template('chaat.html', username=session["user"], room_id=room_id)
    else:
        return redirect(url_for('login'))
@app.route("/logout")
def logout():
    session['user']=None
    return redirect(url_for("index"))


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'],data['room_id']))
    join_room(data['room_id'])
    socketio.emit('join_room_announcement',data)
    
@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {} : {}".format(data['username'],data['room_id'],data['message']))
    socketio.emit('recieve_message',data,room=data['room_id'])
if __name__ == "__main__" :

    socketio.run(app)
