import pandas as pd
import numpy as np
import random

# Expanded list of career paths
CAREER_PATHS = [
    # Science & Medicine
    "Medicine", "Dentistry", "Pharmacy", "Nursing", "Veterinary Science", "Biomedical Science",
    # Engineering & Technology
    "Civil Engineering", "Mechanical Engineering", "Electrical Engineering", "Computer Engineering",
    "Software Engineering", "Telecommunications", "Aerospace Engineering", 
    # Computer Science & IT
    "Computer Science", "Information Technology", "Data Science", "Cybersecurity", "AI & Machine Learning",
    # Business & Economics
    "Business Administration", "Accounting", "Finance", "Economics", "Marketing", "Human Resource Management",
    # Agriculture & Environment
    "Agricultural Science", "Environmental Science", "Forestry", "Food Science",
    # Education & Social Sciences
    "Education", "Psychology", "Sociology", "Social Work", "Counseling",
    # Law & Humanities
    "Law", "International Relations", "Languages", "Journalism", "Media Studies",
    # Arts & Design
    "Fine Arts", "Graphic Design", "Architecture", "Music", "Theatre Arts",
    # Hospitality & Tourism
    "Hospitality Management", "Tourism", "Culinary Arts"
]

# All possible subjects
ALL_SUBJECTS = ["Math", "English", "Kiswahili", "Biology", "Chemistry", "Physics", 
                "Geography", "History", "Religion", "Business", "Computer Science", "Agriculture"]

# Compulsory subjects
COMPULSORY_SUBJECTS = ["Math", "English", "Kiswahili"]

# Optional subjects
OPTIONAL_SUBJECTS = [s for s in ALL_SUBJECTS if s not in COMPULSORY_SUBJECTS]

# Grades with point values
GRADES = ["A", "B", "C", "D", "E", "F"]
GRADE_POINTS = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "E": 0.5, "F": 0.0}

def generate_weighted_grade(weights=None):
    """Generate a grade with optional weights"""
    if weights is None:
        weights = [25, 30, 20, 15, 5, 5]  # Default distribution
    return random.choices(GRADES, weights=weights)[0]

def is_qualified_for_career(student_data, career):
    """Determine if a student qualifies for a specific career based on subjects and grades"""
    
    # Extract key information
    math_grade = student_data["Math_Grade"]
    english_grade = student_data["English_Grade"]
    optional_subjects = [
        student_data["Subject_4"],
        student_data["Subject_5"],
        student_data["Subject_6"],
        student_data["Subject_7"]
    ]
    optional_grades = [
        student_data["Grade_4"],
        student_data["Grade_5"],
        student_data["Grade_6"],
        student_data["Grade_7"]
    ]
    took_all_sciences = student_data["Took_All_Sciences"]
    gpa = student_data["Average_Performance"]
    
    # Check qualifications based on career path
    
    # Medicine & Health Sciences
    if career in ["Medicine", "Dentistry", "Pharmacy"]:
        return (took_all_sciences and 
                GRADE_POINTS[math_grade] >= 3.0 and
                GRADE_POINTS[english_grade] >= 3.0 and
                gpa >= 3.5 and
                "Biology" in optional_subjects and
                "Chemistry" in optional_subjects)
    
    elif career in ["Nursing", "Veterinary Science", "Biomedical Science"]:
        return (took_all_sciences and 
                GRADE_POINTS[math_grade] >= 2.5 and
                gpa >= 3.0)
    
    # Engineering
    elif "Engineering" in career:
        has_physics = "Physics" in optional_subjects
        physics_index = optional_subjects.index("Physics") if has_physics else -1
        physics_grade = optional_grades[physics_index] if has_physics else "F"
        
        return (GRADE_POINTS[math_grade] >= 3.0 and
                "Physics" in optional_subjects and
                GRADE_POINTS[physics_grade] >= 3.0 and
                gpa >= 3.0)
    
    # Computer Science & IT
    elif career in ["Computer Science", "Software Engineering", "Information Technology", 
                   "Data Science", "Cybersecurity", "AI & Machine Learning"]:
        cs_in_subjects = "Computer Science" in optional_subjects
        return (GRADE_POINTS[math_grade] >= 3.0 and
                gpa >= 2.8 and
                (cs_in_subjects or GRADE_POINTS[math_grade] >= 3.5))
    
    # Business & Economics
    elif career in ["Business Administration", "Accounting", "Finance", 
                   "Economics", "Marketing", "Human Resource Management"]:
        has_business = "Business" in optional_subjects
        return (GRADE_POINTS[math_grade] >= 2.5 and
                GRADE_POINTS[english_grade] >= 2.5 and
                (has_business or gpa >= 2.8))
    
    # Agriculture & Environment
    elif career in ["Agricultural Science", "Environmental Science", "Forestry", "Food Science"]:
        has_agriculture = "Agriculture" in optional_subjects
        has_biology = "Biology" in optional_subjects
        return (gpa >= 2.5 and (has_agriculture or has_biology))
    
    # Education
    elif career == "Education":
        return gpa >= 2.0
    
    # Social Sciences
    elif career in ["Psychology", "Sociology", "Social Work", "Counseling"]:
        return (GRADE_POINTS[english_grade] >= 2.5 and gpa >= 2.7)
    
    # Law & Humanities
    elif career in ["Law", "International Relations", "Languages", "Journalism", "Media Studies"]:
        return (GRADE_POINTS[english_grade] >= 3.0 and
                GRADE_POINTS[student_data["Kiswahili_Grade"]] >= 2.5 and
                gpa >= 2.8)
    
    # Arts & Design
    elif career in ["Fine Arts", "Graphic Design", "Architecture", "Music", "Theatre Arts"]:
        if career == "Architecture":
            return (GRADE_POINTS[math_grade] >= 3.0 and gpa >= 3.0)
        else:
            return (GRADE_POINTS[english_grade] >= 2.5 and gpa >= 2.2)
    
    # Hospitality & Tourism
    elif career in ["Hospitality Management", "Tourism", "Culinary Arts"]:
        return (GRADE_POINTS[english_grade] >= 2.5 and gpa >= 2.3)
    
    # Default fallback
    return gpa >= 2.0

def assign_career(student_data):
    """Assign a suitable career based on subjects and performance"""
    
    # Shuffle careers to avoid bias
    shuffled_careers = CAREER_PATHS.copy()
    random.shuffle(shuffled_careers)
    
    # Find all possible careers the student qualifies for
    qualified_careers = []
    for career in shuffled_careers:
        if is_qualified_for_career(student_data, career):
            qualified_careers.append(career)
    
    # Return a random career from qualified options
    if qualified_careers:
        return random.choice(qualified_careers)
    else:
        # Fallback to a less selective career if none match
        fallback_careers = ["Education", "Business Administration", "Agriculture"]
        return random.choice(fallback_careers)

def generate_student():
    """Generate a complete student profile"""
    
    # Randomly assign gender
    gender = random.choice(["Male", "Female"])
    
    # Assign compulsory subjects (Math, English, Kiswahili)
    # Higher weights for A/B in Math
    math_grade = generate_weighted_grade(weights=[25, 30, 20, 15, 5, 5])
    english_grade = generate_weighted_grade(weights=[20, 30, 25, 15, 5, 5])
    kiswahili_grade = generate_weighted_grade(weights=[20, 25, 30, 15, 5, 5])
    
    # Choose 4 optional subjects (non-compulsory)
    optional_subjects = random.sample(OPTIONAL_SUBJECTS, k=4)
    
    # Generate grades for optional subjects with slight bias by subject
    grades = []
    for subject in optional_subjects:
        if subject in ["Biology", "Chemistry", "Physics"]:
            # Sciences might have slightly tougher grading
            grades.append(generate_weighted_grade(weights=[20, 25, 25, 20, 5, 5]))
        elif subject == "Computer Science":
            # Computer Science with mixed difficulty
            grades.append(generate_weighted_grade(weights=[25, 20, 25, 20, 5, 5]))
        else:
            # Other subjects with standard distribution
            grades.append(generate_weighted_grade())
    
    # Check if all 3 sciences are taken
    took_all_sciences = all(subj in optional_subjects for subj in ["Biology", "Chemistry", "Physics"])
    
    # Calculate GPA (average of all 7 subjects)
    all_grades = [math_grade, english_grade, kiswahili_grade] + grades
    gpa = round(sum([GRADE_POINTS[g] for g in all_grades]) / 7, 2)
    
    # Create the student data dictionary
    student_data = {
        "Gender": gender,
        "Math_Grade": math_grade,
        "English_Grade": english_grade,
        "Kiswahili_Grade": kiswahili_grade,
        "Subject_4": optional_subjects[0],
        "Subject_5": optional_subjects[1],
        "Subject_6": optional_subjects[2],
        "Subject_7": optional_subjects[3],
        "Grade_4": grades[0],
        "Grade_5": grades[1],
        "Grade_6": grades[2],
        "Grade_7": grades[3],
        "Took_All_Sciences": took_all_sciences,
        "Average_Performance": gpa
    }
    
    # Assign career based on subjects and grades
    student_data["Career_Path"] = assign_career(student_data)
    
    return student_data

def analyze_dataset(df):
    """Perform basic analysis on the generated dataset"""
    print(f"Total records: {len(df)}")
    print(f"Gender distribution: {df['Gender'].value_counts(normalize=True).to_dict()}")
    print(f"Average GPA: {df['Average_Performance'].mean():.2f}")
    print(f"Percentage taking all sciences: {df['Took_All_Sciences'].mean() * 100:.1f}%")
    print("\nCareer distribution:")
    career_counts = df['Career_Path'].value_counts()
    for career, count in career_counts.items():
        print(f"  {career}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\nPopular optional subjects:")
    all_optional = pd.Series(
        df[['Subject_4', 'Subject_5', 'Subject_6', 'Subject_7']].values.flatten()
    ).value_counts()
    for subj, count in all_optional.items():
        print(f"  {subj}: {count} ({count/(len(df)*4)*100:.1f}%)")

# Generate the dataset
def generate_dataset(num_records=1000, filename="career_recommendation_dataset.csv"):
    """Generate the full dataset with the specified number of records"""
    print(f"Generating dataset with {num_records} records...")
    data = [generate_student() for _ in range(num_records)]
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename}")
    
    # Analyze the dataset
    analyze_dataset(df)
    
    return df

# Run the generator
if __name__ == "__main__":
    # Set random seed for reproducibility (optional)
    random.seed(42)
    
    # Generate 1000 entries
    df = generate_dataset(1000)