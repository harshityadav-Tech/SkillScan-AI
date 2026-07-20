async function analyzeResume() {
    const resumeText = document.getElementById('resumeInput').value;
    const jobDescription = document.getElementById('jobDescription').value;
    
    const response = await fetch("http://127.0.0.1:5000/predict",
        {method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            resume_text: resumeText,
            job_description: jobDescription
        })}
    );
    const data = await response.json();
    let color = '#f44336'; // Red for low score
    if (data.ats_score >= 80) {
        color = '#4CAF50'; // Green for high score
    } else if (data.ats_score >= 50) {
        color = '#FF9800'; // Orange for medium score
    }     

    console.log(data);
    document.getElementById('result').innerHTML = `
    <h2>Prediction Result:</h2>
    <p><strong>Predicted Job Role:</strong> ${data.predicted_category}</p>
    <p><strong> Extracted Skills:</strong> ${data.extracted_skills.join(", ")}</p>
      
    <div class="ats-container" >
    <h3>ATS Score</h3 >
    <div class="progress-bar" >
    <div class="progress-fill" style="width: ${data.ats_score}%;" >
    </div >
    </div >
    <p style="color: ${color}; font-weight: bold;" >${data.ats_score}%</p >
    </div >
    
    <p><strong>Matched Skills:</strong> ${data.matched_skills.join(", ")}</p>
    <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ")}</p>
    <p><strong>Extracted skills:</strong> ${data.extracted_skills.join(", ")}</p>
    `;  
}