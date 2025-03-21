
import streamlit as st
import joblib
import pandas as pd

# Load the pre-trained model
pipeline = joblib.load('career_recommendation_model.pkl')

# Grade conversion dictionary
GRADE_POINTS = {
    "A": 4.0, "B": 3.0, "C": 2.0,
    "D": 1.0, "E": 0.5, "F": 0.0
}

def get_student_input():
    st.title("Career Path Recommendation System")
    
    # Collect basic information
    st.header("Student Information")
    gender = st.selectbox("Gender", ["Male", "Female"])
    
    # Collect core subject grades (convert to numerical)
    st.header("Core Subject Grades")
    col1, col2, col3 = st.columns(3)
    with col1:
        math_grade = GRADE_POINTS[st.selectbox("Math", ["A", "B", "C", "D", "E", "F"])]
    with col2:
        english_grade = GRADE_POINTS[st.selectbox("English", ["A", "B", "C", "D", "E", "F"])]
    with col3:
        kiswahili_grade = GRADE_POINTS[st.selectbox("Kiswahili", ["A", "B", "C", "D", "E", "F"])]
    
    # Collect optional subjects and grades
    st.header("Optional Subjects")
    optional_subjects = ["Biology", "Chemistry", "Physics", "Geography",
                        "History", "Religion", "Business", "Computer Science", "Agriculture"]
    
    selected_subjects = st.multiselect(
        "Choose 4 subjects (order matters):",
        optional_subjects,
        help="Select exactly 4 subjects. The order matters for subject numbering."
    )
    
    if len(selected_subjects) != 4:
        st.error("Please select exactly 4 optional subjects.")
        st.stop()
    
    # Collect and convert optional subject grades
    optional_grades = []
    st.header("Optional Subject Grades")
    for subject in selected_subjects:
        grade = GRADE_POINTS[st.selectbox(
            f"{subject} Grade", 
            ["A", "B", "C", "D", "E", "F"],
            key=f"grade_{subject}"
        )]
        optional_grades.append(grade)
    
    # Calculate GPA
    all_grades = [math_grade, english_grade, kiswahili_grade] + optional_grades
    gpa = round(sum(all_grades) / 7, 2)
    
    # Check science subjects
    took_all_sciences = all(subj in selected_subjects 
                          for subj in ["Biology", "Chemistry", "Physics"])
    
    return {
        "Gender": gender,
        "Math_Grade": math_grade,
        "English_Grade": english_grade,
        "Kiswahili_Grade": kiswahili_grade,
        "Subject_4": selected_subjects[0],
        "Subject_5": selected_subjects[1],
        "Subject_6": selected_subjects[2],
        "Subject_7": selected_subjects[3],
        "Grade_4": optional_grades[0],
        "Grade_5": optional_grades[1],
        "Grade_6": optional_grades[2],
        "Grade_7": optional_grades[3],
        "Took_All_Sciences": took_all_sciences,
        "Average_Performance": gpa
    }

def predict_career(student_data):
    # Convert to DataFrame
    input_df = pd.DataFrame([student_data])
    
    # Convert categorical features to string type
    categorical_cols = ["Gender", "Subject_4", "Subject_5", "Subject_6", "Subject_7"]
    input_df[categorical_cols] = input_df[categorical_cols].astype("category")
    
    # Make prediction
    prediction = pipeline.predict(input_df)[0]
    
    # Get probabilities
    probabilities = pipeline.predict_proba(input_df)[0]
    classes = pipeline.classes_
    
    # Get top 3 predictions
    top_3_indices = probabilities.argsort()[-3:][::-1]
    top_3 = [(classes[i], round(probabilities[i] * 100, 2)) 
            for i in top_3_indices]
    
    return prediction, top_3

def main():
    student_data = get_student_input()
    
    if st.button("Predict Career Path"):
        prediction, top_3 = predict_career(student_data)
        
        st.subheader("Results")
        st.metric("Average GPA", student_data["Average_Performance"])
        st.success(f"**Recommended Career Path:** {prediction}")
        
        st.write("**Top 3 Career Recommendations:**")
        for career, probability in top_3:
            st.write(f"- {career} ({probability}%)")

if __name__ == "__main__":
    main()