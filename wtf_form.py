from binascii import Error
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.fields.simple import SubmitField
from wtforms.validators import InputRequired, Length, ValidationError , length ,EqualTo
from models import users
from passlib.hash import pbkdf2_sha256
def user_available(form,field):
        query = {'username':form.username.data}
 
        user_object = users.find(query)
        if len(list(user_object)) > 0:
            raise ValidationError("username already taken,try another username")
        else:
            hasp=pbkdf2_sha256.hash(form.password.data)
            users.insert({"username":form.username.data,"password":hasp})

class PasswordError(Error):
    pass
class UsernameError(Error):
    pass

def user_find(form,field):
    username = form.username.data
    password = form.password.data
    print(username,password)
    try:
        i=None
        
        for i in users.find({'username':username}):
            if( not pbkdf2_sha256.verify(str(password),i['password'])):
                # print("In pbk  ")
                raise PasswordError
        if(i==None):
            raise UsernameError       
    
    except PasswordError:
        raise ValidationError("password incorrect")
    except UsernameError:
        raise ValidationError("username not registered")
    # except:
    #     print("in exception")
    #     raise ValidationError("Username and Password incorrect")






class RegistrationForm(FlaskForm):
    username = StringField('Enter username',validators=[InputRequired(message="Username required"),Length(min=8,max=20,message="username must be 8-20 characters"),user_available],render_kw={"placeholder":"must be 8-20 character","class_":"username"})
    password = PasswordField('Enter Password',validators=[InputRequired(message="Password required"),Length(min=8,max=20,message="password must be 8-20 characters")],render_kw={"placeholder":"must be 8-20 characters","class_":"password"})
    confirm_password = PasswordField('Confirm Password',validators=[InputRequired(message="passwrod required"),EqualTo('password',message="password must be same")],render_kw={"placeholder":"must be 8-20 characters","class_":"password"})

class LoginForm(FlaskForm):
    username = StringField('Enter username',validators=[InputRequired(message="Username required"),Length(min=8,max=20,message="username must be 8-20 characters"),user_find],render_kw={"placeholder":"must be 8-20 character","class_":"username"})
    password = PasswordField('Enter Password',validators=[InputRequired(message="Password required"),Length(min=8,max=20,message="password must be 8-20 characters")],render_kw={"placeholder":"must be 8-20 characters","class_":"password"})
      
class Room(FlaskForm):
    createroom = SubmitField("Create Room")      
