'''
import mysql.connector
from collections import deque
from datetime import datetime

# Knowledge base: Diseases and their symptoms (propositional logic representation)
knowledge_base = {
    'Influenza': {'fever': True, 'cough': True, 'sore throat': True, 'runny nose': True, 'fatigue': True},
    'Tuberculosis': {'coughing blood': True, 'fever': True, 'weight loss': True, 'night sweats': True},
    'Asthma': {'shortness of breath': True, 'chest tightness': True, 'wheezing': True, 'coughing': True},
    'Sinusitis': {'facial pain': True, 'nasal congestion': True, 'runny nose': True, 'headache': True},
    'Allergic Rhinitis': {'Sneezing': True, 'Itchy eyes': True, 'runny nose': True, 'Nasal Congestion': True},
    'Bronchitis': {'cough': True, 'mucus': True, 'fatigue': True, 'shortness of breath': True},
    'Migrane': {'severe headache': True, 'nausea': True, 'sensitivity to light': True, 'throbbing pain': True},
    'Hypertension': {'severe headache': True, 'chest pains': True, 'blurred vision': True, 'shortness of breath': True},
    'Gastroenteritis': {'diarrhea': True, 'vomitting': True, 'abdominal pain': True, 'fever': True},
    'pneumonia': {'fever': True, 'chills': True, 'difficult to breath': True, 'cough': True},
    'covid-19': {'fever': True, 'loss of taste': True, 'cough': True, 'shortness of breath': True}
}

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",  
        user="root",      
        password="Singatha@1940",    
        database="Project"  
    )

# Save diagnosis record in the database
def save_record(user_name, symptoms, diagnosed_disease):
    db = connect_db()
    cursor = db.cursor()

    symptoms_str = ', '.join(symptoms.keys())  # Store symptoms as a string
    query = "INSERT INTO user_records (user_name, symptoms, diagnosed_disease) VALUES (%s, %s, %s)"
    values = (user_name, symptoms_str, diagnosed_disease)

    cursor.execute(query, values)
    db.commit()

    print(f"\nRecord saved for {user_name}.\n")
    cursor.close()
    db.close()

# Forward Chaining (BFS) to diagnose based on symptoms (propositional logic)
def forward_chaining(symptoms):
    queue = deque(knowledge_base.keys())  # Start with all diseases
    possible_diseases = []

    while queue:
        disease = queue.popleft()
        disease_symptoms = knowledge_base[disease]

        # Check if all symptoms of a disease are true in the user's provided symptoms (propositional logic)
        if all(symptom in symptoms and symptoms[symptom] == True for symptom in disease_symptoms):
            possible_diseases.append(disease)

    return possible_diseases

# Backward Chaining (DFS) to trace symptoms based on the disease (propositional logic)
def backward_chaining(disease):
    if disease in knowledge_base:
        return knowledge_base[disease]
    else:
        print(f"Disease '{disease}' not found in knowledge base.")
        return {}

# User Interface
def display_menu():
    print("\n--- Medical Diagnosis System ---")
    print("1. Forward Chaining (Diagnose Disease Based on Symptoms)")
    print("2. Backward Chaining (Find Symptoms Based on Disease)")
    print("3. Exit")
    choice = input("Select an option (1/2/3): ").strip()
    return choice

def diagnose_forward():
    print("\n--- Forward Chaining Diagnosis ---")
    user_name = input("Enter your name: ").strip()
    symptoms_input = input("Enter your symptoms separated by commas: ").split(',')
    
    # Convert user symptoms into a dictionary with propositional values
    symptoms = {symptom.strip().lower(): True for symptom in symptoms_input}
    
    possible_diseases = forward_chaining(symptoms)
    
    if possible_diseases:
        diagnosed_disease = ', '.join(possible_diseases)
        print(f"\nPossible diseases based on your symptoms: {diagnosed_disease}")

        # Save diagnosis to the database
        save_record(user_name, symptoms, diagnosed_disease)
    else:
        print("\nNo matching diseases found.")

def diagnose_backward():
    print("\n--- Backward Chaining (Disease to Symptoms) ---")
    disease = input("Enter the disease name: ").strip().title()
    
    symptoms = backward_chaining(disease)
    
    if symptoms:
        symptoms_list = [symptom for symptom, present in symptoms.items() if present]
        print(f"\nSymptoms of {disease}: {', '.join(symptoms_list)}")
    else:
        print(f"\nNo symptoms found for {disease}.")

# Main function
def main():
    while True:
        choice = display_menu()

        if choice == '1':
            diagnose_forward()
        elif choice == '2':
            diagnose_backward()
        elif choice == '3':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main() 
'''

import mysql.connector
from collections import deque
from datetime import datetime

# Knowledge base: Diseases and their symptoms (propositional logic representation)
knowledge_base = {
    'Influenza': {'fever': True, 'cough': True, 'sore throat': True, 'runny nose': True, 'fatigue': True},
    'Tuberculosis': {'coughing blood': True, 'fever': True, 'weight loss': True, 'night sweats': True},
    'Asthma': {'shortness of breath': True, 'chest tightness': True, 'wheezing': True, 'coughing': True},
    'Sinusitis': {'facial pain': True, 'nasal congestion': True, 'runny nose': True, 'headache': True},
    'Allergic Rhinitis': {'sneezing': True, 'itchy eyes': True, 'runny nose': True, 'nasal congestion': True},
    'Bronchitis': {'cough': True, 'mucus': True, 'fatigue': True, 'shortness of breath': True},
    'Migraine': {'severe headache': True, 'nausea': True, 'sensitivity to light': True, 'throbbing pain': True},
    'Hypertension': {'severe headache': True, 'chest pains': True, 'blurred vision': True, 'shortness of breath': True},
    'Gastroenteritis': {'diarrhea': True, 'vomiting': True, 'abdominal pain': True, 'fever': True},
    'Pneumonia': {'fever': True, 'chills': True, 'difficult to breathe': True, 'cough': True},
    'Covid-19': {'fever': True, 'loss of taste': True, 'cough': True, 'shortness of breath': True}
}

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",  
        user="root",      
        password="Singatha@1940",    
        database="Project"  
    )

# Save diagnosis record in the database
def save_record(user_name, symptoms, results):
    db = connect_db()
    cursor = db.cursor()

    symptoms_str = ', '.join(symptoms.keys())  # Store symptoms as a string
    results_str = ', '.join([f"{disease} ({percentage:.2f}%)" for disease, percentage in results])

    query = "INSERT INTO user_records (user_name, symptoms, diagnosed_disease) VALUES (%s, %s, %s)"
    values = (user_name, symptoms_str, results_str)

    cursor.execute(query, values)
    db.commit()

    print(f"\nRecord saved for {user_name}.\n")
    cursor.close()
    db.close()

# Forward Chaining (BFS) to diagnose based on symptoms and calculate percentage match
def forward_chaining(symptoms):
    queue = deque(knowledge_base.keys())  # Start with all diseases
    possible_diseases = []

    while queue:
        disease = queue.popleft()
        disease_symptoms = knowledge_base[disease]
        matched_symptoms = [symptom for symptom in disease_symptoms if symptom in symptoms and symptoms[symptom] == True]
        total_disease_symptoms = len(disease_symptoms)
        matched_percentage = (len(matched_symptoms) / total_disease_symptoms) * 100

        if matched_percentage > 0:
            possible_diseases.append((disease, matched_percentage))

    return possible_diseases

# Backward Chaining (DFS) to trace symptoms based on the disease (propositional logic)
def backward_chaining(disease):
    if disease in knowledge_base:
        return knowledge_base[disease]
    else:
        print(f"Disease '{disease}' not found in knowledge base.")
        return {}

# User Interface
def display_menu():
    print("\n--- Medical Diagnosis System ---")
    print("1. Forward Chaining (Diagnose Disease Based on Symptoms)")
    print("2. Backward Chaining (Find Symptoms Based on Disease)")
    print("3. Exit")
    choice = input("Select an option (1/2/3): ").strip()
    return choice

def diagnose_forward():
    print("\n--- Forward Chaining Diagnosis ---")
    user_name = input("Enter your name: ").strip()
    symptoms_input = input("Enter your symptoms separated by commas: ").split(',')
    
    # Convert user symptoms into a dictionary with propositional values
    symptoms = {symptom.strip().lower(): True for symptom in symptoms_input}
    
    possible_diseases = forward_chaining(symptoms)
    
    if possible_diseases:
        print("\nPossible diseases and their match percentages:")
        for disease, percentage in possible_diseases:
            print(f"- {disease}: {percentage:.2f}% match")
        
        # Save diagnosis to the database
        save_record(user_name, symptoms, possible_diseases)
    else:
        print("\nNo matching diseases found.")

def diagnose_backward():
    print("\n--- Backward Chaining (Disease to Symptoms) ---")
    disease = input("Enter the disease name: ").strip().title()
    
    symptoms = backward_chaining(disease)
    
    if symptoms:
        symptoms_list = [symptom for symptom, present in symptoms.items() if present]
        print(f"\nSymptoms of {disease}: {', '.join(symptoms_list)}")
    else:
        print(f"\nNo symptoms found for {disease}.")

# Main function
def main():
    while True:
        choice = display_menu()

        if choice == '1':
            diagnose_forward()
        elif choice == '2':
            diagnose_backward()
        elif choice == '3':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
   

  