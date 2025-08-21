from flask import Flask,url_for,redirect,request ,render_template

#initalizaation
app=Flask(__name__)

@app.route('/sai/<int:score>')
def sai(score):
    if score>=50:
        res="PASS"
    else:
        res="FAIL"
    return render_template('resultt.html',result=res)


@app.route('/submit',methods=['GET','POST'])
def submit():
    total_score=0
    if request.method=='POST':
        subject1=float(request.form['subject1'])
        subject2=float(request.form['subject2'])
        subject3=float(request.form['subject3'])
        subject4=float(request.form['subject4'])
        subject5=float(request.form['subject5'])

        total_score=(subject1+subject2+subject3+subject4+subject5)/5
    else:
        return render_template('sai')
    return redirect(url_for('sai',score=int(total_score))) 


if __name__=="__main__":
    app.run(debug=True)