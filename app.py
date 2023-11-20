from dependency import *

# Dictonary for Questions Answers

question_dict={"Strongly Disagreee":1,
               "Disagree":2,
               "Somewhat Disagree":3,
               "Neutral":4,
               "Somewhat Agree":5,
               "Agree":6,
               "Strongly Agree":7,
               "Very Strongly Agree":8,
               "Extremely Agree":9,
               "Completely Agree":10}



# Endpoint for Homepage

@app.route('/')
def homepage():
    return render_template('HomePage.html')

# App Route for Contact Us

@app.route('/contactusV1')
def contactus():
    return render_template('ContactUs.html')

# App Route for Registration Page

@app.route('/RegistrationV1')
def registrationpage():
    return render_template('RegistrationPageV1.html')

# App Route for Login-SignUp Page

@app.route('/loginSignupV1')
def loginsignup():
    return render_template('LoginSignupV1.html')



# registration success
@app.route('/RegistrationSuccessV1')
def registration_success():
    return render_template('registration_success.html')


# code for Registration Page

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        # Registration process
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        date = datetime.now()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        existing_user = collection.find_one({'EMAIL_ID': email})
        if existing_user:
            error_message = 'User with the same email already exists!!'
            return render_template('LoginSignupV1.html', error_message=error_message)

        user_data = {

            "USERNAME": name,
            "EMAIL_ID": email,
            "CREATED_DATE": date,
            "PASSWORD": hashed_password,
            "IS_STEP1_DONE" : "N",
            "IS_STEP2_DONE" : "N",
            "IS_COMPLETED" : "N"
        }
        collection.insert_one(user_data)
        print(user_data)

        return render_template('registration_success.html')
    return render_template('LoginSignupV1.html')


# code for Login Page 

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        date = datetime.now()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = collection.find_one({'EMAIL_ID': email, 'PASSWORD': hashed_password})
        if user:
            data = collection1.insert_one({
                'USER_ID': user['_id'],
                'USERNAME': user['USERNAME'],
                'EMAIL_ID': user['EMAIL_ID'],
                'LOGINDATE_TIME': date
            })
            if user['IS_STEP1_DONE']== 'Y':
                temp="You've completed ROUND 1! Best of luck for ROUND 2!"
                return jsonify(temp)

            if user['IS_STEP2_DONE']=='Y':
                temp="Round 2 is finished! Thank you for selecting HireIQ."
                return jsonify(temp)
            
            if user['IS_COMPLETED']=='Y':
                temp="Completion of all tests! Appreciate your choice of HireIQ."
                return jsonify(temp)
            
            return render_template('RegistrationPageV1.html')
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render_template('LoginSignupV1.html', error_message=error_message)



# code for contact us 

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['msg']
    date=datetime.now()
    data1 = collection2.insert_one({
                'USERNAME': name,
                'MESSAGE': message,
                'EMAIL_ID':email,
                'LOGINDATE_TIME': date
            })
    print(data1)
    response = {'status': 'success', 'message': 'Form submitted successfully'}
    return render_template('formsubmission.html',name=name)



UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Code for User Registration Page

@app.route('/UserDetails', methods=['POST'])
def user_details():
    # Retrieve form data
    fname = request.form.get('fname')
    openness = request.form.get('openness')
    email = request.form.get('email')
    conscientiousness = request.form.get('conscientiousness')
    locality = request.form.get('locality')
    extraversion = request.form.get('extraversion')
    state = request.form.get('state')
    zip_code = request.form.get('zip')
    agreeableness = request.form.get('agreeableness')
    dob = request.form.get('dob')
    neuroticism = request.form.get('neuroticism')
    country_code = request.form.get('country_code')
    phone = request.form.get('phone')
    resume = request.files['resume']
    gender = request.form.get('sex')

    filename = secure_filename(resume.filename)
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume.save(resume_path)

    # Update existing user data

    collection.update_one({'EMAIL_ID': email}, {
        '$set': {
            "IS_STEP1_DONE" : "Y",
            'GENDER':gender,
            'ADDRESS': locality,
            'CONTACT': int(phone),
            'STATE': state,
            'ZIP_CODE': int(zip_code),
            'COUNTRY_CODE': country_code,
            'DATE_OF_BIRTH': dob,
            'OPENNESS_RATING': int(openness),
            'CONSCIENTIOUSNESS_RATING': int(conscientiousness),
            'EXTRAVERSION_RATING': int(extraversion),
            'AGREEABLENESS_RATING': int(agreeableness),
            'NEUROTICISM_RATING': int(neuroticism),
            'RESUME_URL': resume_path
        }
    }, upsert=True)

    existing_user = collection.find_one({'EMAIL_ID': email})

    print("existing_user",existing_user)


    temp={"Message":"Data received successfully!"}

    return jsonify(temp)




if __name__ == "__main__" :
    app.run(debug=True)