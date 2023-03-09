from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Create your views here.
def home1(request):
    return render(request,"app/main.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['cpassword']
        
        if User.objects.filter(username = username):
            messages.error(request,"Username already exists.")
            return redirect("home1")
        if User.objects.filter(email = email):
            messages.error(request,"email already registered.")
            return redirect("home1")
        if len(username)>20:
            messagaes.error(request,"username should not be greater than 20 characters")
        if pass1 != pass2:
            messages.error(request,"Passwords doesn't match")
        if not username.isalnum():
            messages.error(request,"Username must be alphanumeric")
            return redirect("home1")
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        
        messages.success(request,"Your account has been successfully created.")
        
        return redirect('signin')
    return render(request,"app/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            fname = user.first_name
            return redirect("home")
        else:
            messages.error(request,"Add Credentials")
            return redirect("home1")
    return render(request,"app/signin.html")

def home(request):
    return render(request,"app/home.html")

def signout(request):
    logout(request)
    messages.success(request,"Loged out successfully")
    return redirect("home1")

def predict(request):
    heart_data = pd.read_csv("media\heart.csv")
    x=heart_data.head()

    #print last 5 rows of the dataset
    y = heart_data.tail()

    # no of rows and columns in the dataset
    z = heart_data.shape

    #getting some info about the data
    a = heart_data.info()

    #checking for missing values
    b = heart_data.isnull().sum()

    #statistical measures about the data
    c = heart_data.describe()

    #checking the distribution of the target variable
    d = heart_data['target'].value_counts()

    X = heart_data.drop(columns = 'target',axis = 1)
    Y = heart_data['target']
    

    X_train,X_test,Y_tarin,Y_test = train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=2)
    
    
    #Logistic regression
    model = LogisticRegression()
    #training the Logistic regression model
    model.fit(X_train,Y_tarin)
    #accuracy on training data
    X_train_prediction = model.predict(X_train)
    training_data_accuracy = accuracy_score(X_train_prediction,Y_tarin)
    
    #accuracy on test data
    X_test_prediction = model.predict(X_test)
    test_data_accuracy = accuracy_score(X_test_prediction,Y_test)
    
    #predictive model
    
    if request.method == 'POST':
        age = request.POST['age']
        sex = request.POST['sex']
        cp = request.POST['cp']
        trestbps = request.POST['trestbps']
        chol = request.POST['chol']
        fbs = request.POST['fbs']
        restecg = request.POST['restecg']
        thalach = request.POST['thalach']
        exang = request.POST['exang']
        oldpeak = request.POST['oldpeak']
        slope = request.POST['slope']
        ca = request.POST['ca']
        thal = request.POST['thal']
        
        age = int(age)
        sex = int(sex)
        cp = int(cp)
        trestbps = int(trestbps)
        chol = int(chol)
        fbs = int(fbs)
        restecg = int(restecg)
        thalach = int(thalach)
        exang = int(exang)
        oldpeak = float(oldpeak)
        slope = int(slope)
        ca = int(ca)
        thal = int(thal)
                
        input_data = (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)
        #change the input data to a numpy array
        input_data_as_numpy_array = np.asarray(input_data)

        #reshape the numpy array as we are predicting for only one instatnce
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
        prediction = model.predict(input_data_reshaped)
        if(prediction[0] == 0):
            return render(request,"app/result.html")  
        else:
            return render(request,"app/result2.html")  
    return render(request,"app/predict.html")