import re
import string

from werkzeug.exceptions import BadRequest, NotFound

class Validators(object):
    def __init__(self):
        pass 

    def email_validator(self, email):
        if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
            email):
            raise BadRequest("Please provide a valid email")
        elif len(email) < 10:
            raise BadRequest("Email is too short")
        else:
            return email

    def password_validator(self, password):
        self.password = password
        
        if len(self.password) < 6:
            raise BadRequest("Password is either to short[min six characters]")
        elif len(self.password) > 12:
            raise BadRequest("Password is too long [max twelve characters]")
        else:
            return self.password            
            

    def username_validator(self, username):
        self.username = username
        if len(username) != 0 or len(username) > 4:
            for i in username:
                if not i.isalpha():
                    raise BadRequest("Username should not contain digits")
                else:
                    return self.username
        else:
            raise BadRequest("Your username is too short, a username should be a minimum of 4 characters")

    def number_not_negative(self, value):
        if value < 0:
            raise BadRequest("Your id is a negative number")
        elif type(value) == int:
            raise BadRequest("Please provide a number")
        else:
            return value

    def check_no_items(self, value):
        if len(value) == 0:
            items = "Nothing yet"
            return items
        else:
            items = value
            return items

    def status_validator(self, status):
        if status not in ["New", "Processing", "Cancelled","Completed"]:
            raise BadRequest("The order status is unknown")
        else:
            return status

    def validate_string(self, string):   
        result = re.compile('[@_!#$%^&*()<>?/\|}{~:]')     
        if(result.search(string) == None): 
            return string          
        else: 
            raise BadRequest("A field should not contain special characters, please remove them") 
                