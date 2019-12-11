from flask import Flask, render_template, request
from service import *
from models import *

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def student():
    return render_template('MainPage.html')


@app.route('/newCondit', methods=['POST', 'GET'])
def newCondit():
    # if request.method == 'POST':
    return render_template("newCondit.html")


@app.route('/newMesur', methods=['POST', 'GET'])
def newMesur():
    # if request.method == 'POST':
    return render_template("newMesur.html")


@app.route('/newSeq', methods=['POST', 'GET'])
def newSeq():
    # if request.method == 'POST':
    return render_template("newSeq.html")


@app.route('/exp', methods=['POST', 'GET'])
def exp():
    # if request.method == 'POST':
    return render_template("exp.html")


@app.route('/expMeasurements', methods=['POST', 'GET'])
def expMeasurements():
    if request.method == 'POST':
        result = request.form
        return render_template("expMeasurements.html", result=result)


@app.route('/enterCSV', methods=['POST', 'GET'])
def enterCSV():
    # if request.method == 'POST':
    return render_template("enterCSV.html")


@app.route('/expInfo', methods=['POST', 'GET'])
def expInfo():
    # if request.method == 'POST':
    return render_template("expInfo.html")


@app.route('/sideByside', methods=['POST', 'GET'])
def sideByside():
    # if request.method == 'POST':
    return render_template("sideByside.html")


@app.route('/expComparison', methods=['POST', 'GET'])
def expComparison():
    if request.method == 'POST':
        result = request.form
        compare_exp(result)
        return render_template("expComparison.html", result=result)


@app.route('/results', methods=['POST', 'GET'])
def results():
    # if request.method == 'POST':
    return render_template("results.html")


@app.route('/resultsSC', methods=['POST', 'GET'])
def resultsSC():
    if request.method == 'POST':
        result = request.form
        return render_template("resultsSC.html", result=result)


@app.route('/inputResultsSC', methods=['POST', 'GET'])
def inputResultsSC():
    if request.method == 'POST':
        result1 = request.form.get('SequenceVal')
        result2 = request.form.get('ConditVal')
        if result1 == '':
            result1 = 0
        if result2 == '':
            result2 = 0
        result1 = int(result1)
        result2 = int(result2)
        return render_template("inputResultsSC.html", result1=result1, result2=result2)


@app.route('/resultsM', methods=['POST', 'GET'])
def resultsM():
    if request.method == 'POST':
        result = request.form
        return render_template("resultsM.html", result=result)


@app.route('/inputResultsM', methods=['POST', 'GET'])
def inputResultsM():
    if request.method == 'POST':
        result = request.form.get('LoopVal')
        if result == '':
            result = 0
        result = int(result)
        return render_template("inputResultsM.html", result=result)


@app.route('/displayResults', methods=['POST', 'GET'])
def displayResults():
    if request.method == 'POST':
        result = request.form
        return render_template("displayResults.html", result=result)


@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'POST':
        result = request.form
        insert_into_db(result)
        return render_template("different.html", result=result)


@app.route('/displayExpInfo', methods=['POST', 'GET'])
def displayExpInfo():
    if request.method == 'POST':
        result = request.form
        get_exp(result)
        return render_template("displayExpInfo.html", result=result)  # TODO: change to display exp


'''def results():
    if request.method == 'POST':
        result = request.form
        return render_template("different.html",result = result)'''

if __name__ == '__main__':
    app.run(debug=True)

'''from flask import Flask, render_template
app = Flask(__name__)

@app.route('/hello/<int:score>')
def hello_name(score):
   return render_template('hello.html', marks = score)

if __name__ == '__main__':
   app.run(debug = True)'''

'''from flask import Flask, redirect, url_for

#from models import Schema

app = Flask(__name__)


@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<name>")
def hello_name(name):
    return "Hello " + name

@app.route('/rev/<float:revNo>')
def revision(revNo):
   return 'Revision Number %f' % revNo


if __name__ == "__main__":
    #Schema()
    app.run(debug=True)'''
