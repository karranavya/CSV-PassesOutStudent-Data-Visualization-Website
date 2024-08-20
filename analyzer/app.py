from flask import Flask, render_template, request
import pandas as pd
import json
import os

app = Flask(__name__)

file_path = os.path.join('C:\\Users\\karra\\Desktop\\project1\\CSV-Data-Visualization-Website-main\\analyzer\\static', 'Book2.csv')
df = pd.read_csv(file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        password = request.form['password']

        # Authenticate the user
        user_data = df[(df['Roll numbers'] == roll_number) & (df['passwords'] == password)]
        if not user_data.empty:
            user_data = user_data.iloc[0]
            student_name = user_data['Student Name']

            # Convert integer values (cgpa, attendance) to regular integers
            sem_cols1 = [f'SEM-{i}' for i in range(1, 9)]  # List of SEM column names
            cgpa = [int(value) for value in user_data[sem_cols1]]  # Convert and store in cgpa list

            sem_cols2 = [f'A{i}' for i in range(1, 9)]  # List of A column names
            attendance = [int(value) for value in user_data[sem_cols2]]  # Convert and store in attendance list

            total_activities = [int(user_data['hackathon']), int(user_data['projects']), int(user_data['sports']),
                                int(user_data['workshops']), int(user_data['clubs']), int(user_data['internships']),
                                int(user_data['tech visits']), int(user_data['research papers'])]

            # Extract additional values
            cgpa_value = f"{user_data['CGPA']:.2f}"
            total_a_value = f"{user_data['TOTAL A']:.2f}"
            total_activities_sum = sum(total_activities)
            spf_value = user_data['SPF']

            chart_data = {
                'cgpa': cgpa,
                'attendance': attendance,
                'total_activities': total_activities
            }

            # Render template with additional values
            return render_template('select.html', 
                                   chart_data=json.dumps(chart_data), 
                                   student_name=student_name, 
                                   cgpa_value=cgpa_value,
                                   total_a_value=total_a_value,
                                   total_activities_sum=total_activities_sum,
                                   spf_value=spf_value)
        else:
            error_message = "Invalid roll number or password."
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
