from flask import Flask, render_template, request
import pandas as pd
import json
import os

app = Flask(__name__)

# Load the CSV file
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
            cgpa = [user_data[f'SEM-{i}'] for i in range(1, 9)]
            attendance = [user_data[f'A{i}'] for i in range(1, 9)]
            chart_data = {
                'cgpa': cgpa,
                'attendance': attendance
            }
            return render_template('select.html', chart_data=json.dumps(chart_data), student_name=student_name)
        else:
            error_message = "Invalid roll number or password."
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
