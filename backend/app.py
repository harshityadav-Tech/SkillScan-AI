from flask import Flask, request, jsonify
import joblib
import re
from flask_cors import CORS
app= Flask(__name__)
CORS(app)
rf_model = joblib.load("rf_model.pkl")
tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")
skills = ["python", "java", "c++", "javascript", "html","css","react","nodejs","flask","django","tensorflow","pytorch","sql","mongodb","aws","git","github","docker","kubernetes","pandas","numpy","scikit-learn","matplotlib","seaborn"]
def clean_resume_text(text):
    text=text.lower();
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text )
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def extract_skills(resume_text):
    resume_text = resume_text.lower()
    found_skills = []
    for skill in skills:
        if skill in resume_text:
            found_skills.append(skill)  
    return found_skills

def predict_resume_category(resume_text):
    cleaned_text = clean_resume_text(resume_text)
    features = tfidf_vectorizer.transform([cleaned_text])
    predicted_category = rf_model.predict(features)[0]
    return predicted_category   
@app.route('/') 
def home():
    return "Welcome to the Resume Analysis API! Use the /predict endpoint to analyze resumes."

def calculate_ats_score(resume_skills, jd_skills):
    mateched_skills = []
    for skill in jd_skills:
        if skill in resume_skills:
            mateched_skills.append(skill)
    
    missing_skills = []
    for skill in jd_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)
    if len(jd_skills) == 0:
        return 0,[],[]
    else:
        ats_score = (len(mateched_skills) / len(jd_skills)) * 100
    return ats_score,mateched_skills,missing_skills
@app.route('/predict', methods=['POST'])
def predict():  
    data = request.json
    resume_text = data.get('resume_text', '')
    job_description = data.get('job_description', '')
    predicted_category = predict_resume_category(resume_text)
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)
    ats_score, matched_skills, missing_skills = calculate_ats_score(resume_skills, jd_skills)
    response = {
        'predicted_category': predicted_category,
        'extracted_skills': resume_skills,
        'ats_score': round(ats_score, 2),
        'matched_skills': matched_skills,
        'missing_skills': missing_skills
    }
    print("Received Resume:",resume_text)
    print("predicted_category:",predicted_category)
    print("Job Description:",job_description)
    print("ATS Score:",ats_score)
    print("Matched Skills:",matched_skills)
    print("Missing Skills:",missing_skills)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
        