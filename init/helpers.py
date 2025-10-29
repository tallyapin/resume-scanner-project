import os
import re
import nltk
import numpy as np
from nltk.corpus import stopwords
nltk.download('words')
nltk.download('averaged_perceptron_tagger')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from nltk.corpus import wordnet


# download the stop words corpus
nltk.download('stopwords')

#download the punkt corpus
nltk.download('punkt')

# download the wordnet corpus
nltk.download('wordnet')
english_words = set(wordnet.words())

# set stop words
stop_words = set(stopwords.words('english'))


# define function that takes a string as input and returns the number of words
def count_words(text):

   # Remove leading and trailing whitespace
    text = text.strip()
    
    # Split the string into words
    words = text.split()
    
    return len(words)


# define function to check for enlish words    
def is_english_word(word):

    synsets = wordnet.synsets(word)

    return len(synsets) > 0 and synsets[0].pos() in ['n', 'v', 'a', 'r']


# define function to detect an email address and return a bool
def find_email(text):
    # define email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # search for email pattern in resume text
    email = re.search(email_pattern, text)
    
    # return email if found, otherwise return None
    
    if email:
        return email.group()
    else:
        return None


# define function to detect a phone number and return a bool
def find_phone_number(text):
    
    phone_regex = r"\+?\d{0,2}\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    
    match = re.search(phone_regex, text)
    
    if match:
        return match.group(0)
    else:
        return None


# define function to detect a linkedin profile and return a bool
def find_linkedin(text):

    linkedin_regex = r"(?i)linkedin.com/(?:in|profile)[/\w\d-]+"
    
    match = re.search(linkedin_regex, text)
    
    if match:
        return match.group(0)
    else:
        return None


# define function to take as input a string and return a list of tokens that have been filtered to remove stop words and non-english words
def process_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    
    text_tokens = nltk.word_tokenize(text)

    text_tokens = [word for word in text_tokens if word not in stop_words]

    text_tokens = [word for word in text_tokens if not bool(re.search(r'\d', word))]

    text_tokens = [word for word in text_tokens if is_english_word(word)]

    return text_tokens


# define function to create a bucket of words taking as input two lists of tokens and returning a bucket of words based off the job desctiption vocabulary
def create_bow(resume_tokens, job_tokens):

    # Join the tokens into strings
    resume_text = ' '.join(resume_tokens)
    job_text = ' '.join(job_tokens)

    # Instantiate the CountVectorizer object on the job posting text in order to target the set of words used for comparison
    vectorizer = CountVectorizer()
    vectorizer.fit([job_text])

    # Fit and transform the text data
    resume_bow = vectorizer.transform([resume_text])
    job_bow = vectorizer.transform([job_text])

    return job_bow, resume_bow


# define function to calculate ats score
def calculate_ats(job_bow, resume_bow):

    # calculate the cosine similarity between the two bags of words
    similarity_score = cosine_similarity(resume_bow, job_bow)[0][0]

    # calculate the percentage score
    max_score = 1.0
    percent_score = (similarity_score / max_score) * 100

    return percent_score


# define function to return a panda dataframe containing a list of key words, the resume count, job posting count, and net difference
def compare_key_words(job_text, skills, job_bow, resume_bow):

    # Instantiate the CountVectorizer object
    vectorizer = CountVectorizer()
    vectorizer.fit([job_text])
    
    # create a dataframe to hold the results
    skills_df = pd.DataFrame(columns=['word', 'resume_count', 'job_posting_count', 'difference'])

    # loop through the vocabulary list
    for i, word in enumerate(vectorizer.get_feature_names_out()):
        
        # get the counts for the word in the resume and job posting bags of words
        resume_count = resume_bow[0, i]
        job_posting_count = job_bow[0, i]
        
        # calculate the difference between the two counts
        difference = resume_count - job_posting_count
        
        # add the row to the dataframe
        if word in skills:
            skills_df.loc[i] = [word.capitalize(), resume_count, job_posting_count, difference]

    # sort the dataframe by the difference column in descending order
    skills_df = skills_df.sort_values(by='job_posting_count', ascending=False)
    skills_df = skills_df.loc[skills_df['job_posting_count'] > 1]
    skills_df = skills_df.head(20)

    return skills_df