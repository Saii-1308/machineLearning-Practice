##building Url Dynamically
#variable rule
##jinja 2 template Engine

from flask import Flask,request,render_template

#initalization
app=Flask(__name__)

@app.route('/')
def home():
    return "<html><H1> hello how are u sai</H1></html>"


@app.route("/index",methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

#When we submit datav it hit thus function
@app.route("/submit",methods=['GET','POST'])
def submit():
    if request.method=='POST':
        name=request.form['name']
        return f"hey {name}!!"
    return render_template('form.html')

#variable rule
@app.route('/success/<int:score>')
def success(score):
    return "tha marks you got is "+str(score)
#You cannot directly concatenate a string and an integer in Python:

@app.route('/try1/<int:marks>')
def try1(marks):
    return f"your enter {marks} marks"


@app.route('/sai/<int:score>')
def sai(score):
    if score>=50:
        res="PASS"
    else:
        res="FAIL"
    return render_template('result.html',result=res)

'''
{{}} expression to print output in html
{% %}condition expression
{# #} comments

'''
@app.route('/try2/<name>')
def try2(name):
    if name=="sai":
        a="heyy!!"
    else:
        a="Byee!!"
    return render_template('try22.html',result=a)

#if condition->
@app.route('/sai1/<int:score>')
def sai1(score):
    if score>=50:
        res="PASS"
    else:
        res="FAIL"
    
    ex={'score':score,'res':res}
    return render_template('result1.html',result=ex)

#if condition
@app.route('/if_con/<int:score>')
def if_con(score):
    return render_template('result.html',result=score)

if __name__=="__main__":
    app.run(debug=True)

    