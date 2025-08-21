from flask import Flask
'''
It create an instance of the Flask class,
which will be your WSGI(Web Server Gateway Interface) application.
'''
#initalize flask -> WSGI Appliaction
app=Flask(__name__)#entery point

#decotartor
@app.route("/")
def welcome():
    return "welcome to my 1st flask tutorial.This should be amazine course"

@app.route("/index")
def index():
    return "this is my index function!!"


#entery point of flas app
if __name__=="__main__":
    app.run(debug=True)#anytime u make chnages it  automatically restart your server
