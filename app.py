from flask import Flask, render_template, request
import joblib
import os
import hashlib
import requests
import json
import base64

# Rest of your code...


app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))
app.config['SECRET_KEY'] = 'abc123@567$#'

# Load the Logistic Regression model
LogisticRegression_Model = joblib.load('LogisticRegression_Model.joblib')


def callEnzoicAPI(password):
    apiKey = 'f8e26dc0edbf441080becff0719deff1'
    secretKey = 'S7Th9YvpKzRnwAp4Cd!mg^P&?MMc7!Eq'
    authorizationParameter = apiKey+":"+secretKey
    authorizationParameter = authorizationParameter.encode('ascii')
    authorizationParameter = (base64.b64encode(authorizationParameter)).decode('ascii')
    authorizationParameter = "basic "+str(authorizationParameter)
    password = password.encode('utf-8')
    sha1HashTemp = hashlib.sha1(password)
    sha1Hash = str(sha1HashTemp.hexdigest())
    sha256HashTemp = hashlib.sha256(password)
    sha256Hash = str(sha256HashTemp.hexdigest())
    md5HashTemp = hashlib.md5(password)
    md5Hash = str(md5HashTemp.hexdigest())
    rawData = {'partialSHA1':sha1Hash, 'partialSHA256':sha256Hash, 'partialMD5':md5Hash}
    url = 'https://api.enzoic.com/passwords'
    response = requests.post(url, data = json.dumps(rawData),headers={'content-type':'application/json',
    'authorization':authorizationParameter})
    if(response.status_code == 404):
        print("Not found")
        return (False,0)
    finalResponse = json.loads(response.content.decode('ascii'))
    return (finalResponse["candidates"][0]["revealedInExposure"], finalResponse["candidates"][0]["exposureCount"])





@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/main/', methods=['POST'])
def mainpage():
    if request.method == "POST":
        enteredPassword = request.form['password']
        
        # Load the Logistic Regression model
        LogisticRegression_Model = joblib.load('LogisticRegression_Model.joblib')
        Password = [enteredPassword]
        # Predict the strength
        LogisticRegression_Test = LogisticRegression_Model.predict(Password)
        return render_template("main.html", LogReg=LogisticRegression_Test)
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
