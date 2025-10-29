import os
from flask import Flask, redirect, render_template, request
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime

import docx2txt
from cs50 import SQL
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
from helpers import find_email, find_phone_number, find_linkedin, process_text, create_bow, calculate_ats, compare_key_words, count_words

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def homepage():

    if request.method == "GET":
        
        return render_template("homepage.html")
    
    else:

         # Get the uploaded file
        resume_file = request.files.get('resume_file')

        # Get the resume text from the form data
        resume_text = request.form.get('resume_text')

        # Get the resume text from the form data
        job_text = request.form.get('job_text')

        # perform backend validation
        if not request.form.get('job_text'):
            return redirect("/")
        
        # check to see if a resume was uploaded
        if not request.files.get('resume_file') and not request.form.get('resume_text'):
            return redirect("/")
        
        # check to see if a file and text were both posted
        if request.files.get('resume_file') and request.form.get('resume_text'):
            return redirect("/")
        
        # check to see if a resume file was uploaded or text
        if resume_file:
            # check that input is a .docx file
            if resume_file.filename.endswith('.docx'):
                resume = docx2txt.process(resume_file)
            else:
                return redirect("/")  
        else:
            resume = resume_text

        # check to see if job description length is adequate
        if count_words(job_text) <= 10:
            job_error = "Scan failed, job description does not contain enough words"
            return render_template("homepage.html", form_error=job_error, scroll_to_element="scan-now")
        
        job_posting = job_text

        #import excluded words file
        excluded_words = ['experience', 'new', 'best', 'years', 'work', 'skills', 'proficient', 'strong', 'excellent', 'ability', 'knowledge', 'responsibilities', 'duties', 'achievements', 'accomplishments', 'multitask', 
	    'fast-paced', 'track', 'record', 'passion', 'successful', 'minimum', 'degree', 'job', 'career', 'salary', 'pay', 'including', 'co', 'preferred', 'requires', 'require', 'required', 'able', 'role', 'senior']


        # returns bool if email is found in the resume
        email = find_email(resume)


        # returns bool if a phone number is found in the resume
        phone_number = find_phone_number(resume)


        # returns bool if a linkedin profile is found in the resume
        linkedin = find_linkedin(resume)


        # returns bool if resume word count if between 450 - 750 words
        word_count = count_words(resume)

        if 450 <= word_count <= 750:
            word_count_bool = True
        else:
            word_count_bool = False


        # process job posting text into tokens by removing special characters, removing stop words, and digits
        job_processed = process_text(job_posting)
        
        resume_processed = process_text(resume)


        # remove excluded words
        job_processed = [token for token in job_processed if token not in excluded_words]


        # create a WordNet lemmatizer
        lemmatizer = WordNetLemmatizer()


        # perform lemmatization
        lemmatized_job = [lemmatizer.lemmatize(token, wordnet.VERB) if wordnet.VERB else lemmatizer.lemmatize(token) for token in job_processed]
        lemmatized_resume = [lemmatizer.lemmatize(token, wordnet.VERB) if wordnet.VERB else lemmatizer.lemmatize(token) for token in resume_processed]

        # join lemmatized job description tokens
        lemmatized_job_joined = " ".join(lemmatized_job)


        # Define list of skills
        skills = []

        # define parts of speach tags to extract from job posting
        skills_pos = ['NN','NNS','NNPS','NNP','VBG','VB','VBD','VBN','VBP','VBZ','JJ','JJR','JJS']

        
        # Loop through job posting tagged words and extract hard and soft skills
        for word in lemmatized_job:
            # Assign a POS tag to the word
            pos_tagged_word = pos_tag([word])[0]

            # Check if the POS tag corresponds to a skill
            if pos_tagged_word[1] in skills_pos and pos_tagged_word[0] not in excluded_words:
                
                # If the POS tag corresponds to a skill, append the word to the skills list
                skills.append(pos_tagged_word[0])

        
        # join skills array into a string to store in the databse
        skills_joined = " ".join(skills)


        # create bucket of words using the vocabulary from job description, return if not enough words to create BOW
        try:
            job_bow, resume_bow = create_bow(lemmatized_resume, skills)
        except ValueError:
            form_error = "Scan failed, no key words detected in the job description."
            return render_template("homepage.html", form_error=form_error, scroll_to_element="scan-now")


        # calcualte ats resume score by comaring bow's 
        ats_score = round(calculate_ats(job_bow, resume_bow))


        #determine result message based on the ats score or word count
        if word_count < 25:
            ats_score = 0
            ats_message = "Your resume word count is extremely low. We recommend revising your resume to increase the mention of key words as well as your skills and experience."
        
        elif 25 < word_count < 200:
            ats_message = "Your resume word count is extremely low. We recommend revising your resume to increase the mention of key words as well as your skills and experience."

        elif ats_score >= 76:
            ats_message = "Fantastic! Your score indicates that your resume is an excellent match for the job requirements. We highly recommend applying for the job with confidence."
        
        elif ats_score >= 65 and ats_score <= 75:
            ats_message = "Congratulations! Your score indicates that your resume is well-suited to the job requirements. We recommend applying for the job with confidence."
        
        elif ats_score >= 60 and ats_score <= 64:
            ats_message = "Your score indicates that your resume is almost compatible with the job requirements! Include the mention of frequent key words to reach a score of 65%."
        
        elif ats_score >= 30 and ats_score <= 59:
            ats_message = "Your score indicates that your resume is somewhat compatible with the job requirements. Revise your resume to increase the mention of keywords and highlight your experience using measurable results."

        else:
            ats_message = "Your score indicates that your resume may not meet the requirements for this job. We suggest making changes to your resume to better match the job description."


        # extract skills comparison matrix as a panda dataframe
        skills_df = compare_key_words(skills_joined, skills, job_bow, resume_bow)


        # storing scan results in the database
        db.execute("INSERT INTO scan_results (DTTM, RESUME_TEXT, JD_TEXT, ATS_SCORE, KEY_WORDS) VALUES(?, ?, ?, ?, ?)",
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"), resume, job_posting, ats_score, skills_joined)


        return render_template("results.html", ats_score=ats_score, skills_df=skills_df, email=email, phone_number=phone_number, 
                               linkedin=linkedin, ats_message=ats_message, word_count_bool=word_count_bool)


@app.route("/privacy-policy", methods=["GET"])
def privacy():

    if request.method == "GET":
        
        return render_template("privacy_policy.html")
    
    else:

        return render_template("homepage.html")
    


@app.route("/contact-us", methods=["GET", "POST"])
def contact():

    if request.method == "GET":
        
        return render_template("contact_us.html")
    
    else:

        # perform backend validation
        name = request.form.get('name')

        email = request.form.get('email')

        message = request.form.get('message')
        
        if not request.form.get('name'):
            return redirect("/contact-us")
        
        if not request.form.get('email'):
            return redirect("/contact-us")
        
        if not request.form.get('message'):
            return redirect("/contact-us")
        
        # storing message information in the database
        db.execute("INSERT INTO contact_us (DTTM, NAME, EMAIL, MESSAGE) VALUES(?, ?, ?, ?)",
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, email, message)

        return redirect("/thank-you")
    

@app.route("/thank-you", methods=["GET"])
def thank_you():

    if request.method == "GET":
        
        return render_template("thank_you.html")
    
    else:

        return render_template("homepage.html")