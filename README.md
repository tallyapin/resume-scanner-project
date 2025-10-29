Here’s a professional, GitHub-ready **README.md** for your project — structured clearly and written to appeal to both technical and non-technical readers:

---

# 🧠 Resume Scan Buddy

**Smart Resume Scanner for Job Matching Optimization**

#### 🎥 [Video Demo](https://www.youtube.com/watch?v=-2ggXc5vS3M)

---

## 📋 Overview

**Resume Scan Buddy** is a Python Flask web application that helps job seekers tailor their resumes to specific job descriptions by generating a **Resume Match Score**. The app uses **natural language processing (NLP)** techniques to analyze and compare the similarity between a resume and a job posting, highlighting missing keywords and best-practice improvements to increase interview success rates.

---

## 🚀 Features

* 🧩 **Resume–Job Matching:** Calculates a cosine similarity score between processed resume and job description tokens.
* 🧠 **NLP-Driven Text Processing:** Tokenization, stopword removal, lemmatization, and POS tagging using the **NLTK** library.
* 📊 **Visual Results Dashboard:** Displays the match score using **Chart.js**, with detailed skill comparisons in a Pandas DataFrame.
* ✅ **ATS Best-Practice Checks:** Automatically verifies presence of email, phone, LinkedIn, and optimal word count.
* 🔍 **Skill Gap Detection:** Highlights missing or under-represented keywords from the job description.
* 💾 **SQLite Database Integration:** Stores data locally for efficient and lightweight persistence.

---

## 🧱 Project Structure

```
ResumeScanBuddy/
│
├── app.py                 # Main Flask application
├── helpers.py             # Core NLP and text processing functions
├── templates/
│   ├── homepage.html      # Input form for resume and job description
│   ├── results.html       # Results visualization template
├── static/
│   ├── styles.css         # Front-end styling
│   └── chart.js           # Chart for match score visualization
├── database.db            # SQLite3 database file
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## ⚙️ How It Works

1. **User Input:**
   The user uploads or pastes their resume text and job description via a form on the homepage.

2. **Data Validation:**
   Flask performs backend checks to ensure all required fields are filled.

3. **Preprocessing & NLP:**

   * Special characters removed
   * Tokenization using `nltk`
   * Stopwords and non-English words filtered
   * Lemmatization applied for normalization
   * POS tagging identifies skill-related nouns and adjectives

4. **Keyword Extraction:**
   High-value words from the job description are compared against the resume tokens.

5. **Match Score Calculation:**
   A **cosine similarity** function (via `sklearn`) returns a percentage match score.

6. **Results Display:**
   The app generates a donut chart, skill gap table, and feedback message guiding the user on how to improve their resume alignment.

---

## 🧰 Technologies Used

| Category         | Tools & Libraries      |
| ---------------- | ---------------------- |
| Web Framework    | Flask                  |
| Database         | SQLite3                |
| NLP              | NLTK                   |
| File Handling    | docx2txt               |
| Machine Learning | scikit-learn           |
| Visualization    | Chart.js, Pandas       |
| Front-End        | HTML5, CSS3, Bootstrap |

---

## 🧑‍💻 Installation & Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/<your-username>/ResumeScanBuddy.git
   cd ResumeScanBuddy
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Mac/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   ```bash
   flask run
   ```

   The app will start on **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 📈 Example Output

* **Resume Match Score:** `87%`
* **Top Missing Keywords:** `‘data modeling’, ‘stakeholder’, ‘governance’`
* **ATS Checks:** ✅ Email found | ✅ LinkedIn found | ⚠️ Word count below recommended

---


## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

## 💬 Acknowledgements

* [NLTK Documentation](https://www.nltk.org/)
* [Flask](https://flask.palletsprojects.com/)
* [scikit-learn](https://scikit-learn.org/)
* [Chart.js](https://www.chartjs.org/)

---

🌟 About Me
Hi there! I'm Tal Lyapin. I am a data analyst who specializes in building data solutions, dashboards, and models that turn complex data into clear, actionable insights. Skilled in Python, SQL, Power BI, dbt, Spark, and Snowflake, I focus on using data to optimize performance and guide strategic decisions.
