from flask import Flask ,render_template
 
#initalization
app=Flask(__name__)

@app.route("/")
def welcome():
    #intergrate html tag directly
    return "<html><h1>Welcome to my flask !!</h1></html>"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=="__main__":
    app.run(debug=True)