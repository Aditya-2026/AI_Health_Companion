from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os
from werkzeug.utils import secure_filename
import http.client

app = Flask(__name__)
conn = http.client.HTTPSConnection("workout-planner1.p.rapidapi.com")

# RapidAPI keys (Replace with your actual keys)
EXERCISES_API_KEY = "YOUR_EXERCISES_API_KEY"
WORKOUT_PLANNER_API_KEY = "YOUR_WORKOUT_PLANNER_API_KEY"

# Add these configurations after creating the Flask app
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Health recommendations route
@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

# Function to call Exercises API
def fetch_exercises(body_part, muscle_target, equipment_used):
    url = "https://exercises2.p.rapidapi.com/"
    headers = {
        "x-rapidapi-host": "exercises2.p.rapidapi.com",
        "x-rapidapi-key": EXERCISES_API_KEY
    }
    params = {
        "bodyPart": body_part,
        "muscleTarget": muscle_target,
        "equipmentUsed": equipment_used
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

# Exercises route
@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'POST':
        body_part = request.form['body_part']
        muscle_target = request.form['muscle_target']
        equipment_used = request.form['equipment_used']

        exercises = fetch_exercises(body_part, muscle_target, equipment_used)
        return render_template('exercises.html', exercises=exercises)

    return render_template('exercises.html')

# Function to call Workout Planner API
def fetch_workout_plan(time, equipment, muscle, fitness_level, fitness_goals):
    print("inside fetch_workout_plan function")
    url = "https://workout-planner1.p.rapidapi.com/customized"

    querystring = {"time":"30","equipment":"dumbbells","muscle":"biceps","fitness_level":"beginner","fitness_goals":"strength"}

    headers = {
        "x-rapidapi-key": "aa81da170cmshe3df47affbbbe25p1a598bjsnfa1bbc9bc8ec",
        "x-rapidapi-host": "workout-planner1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        print("success response from api", flush=True)
        print(response.text)
        return response.json()
    else:
        print(f'Error occur due to {response.text}', flush=True)
        return {"error": response.text}

# Workout Planner route
@app.route('/workout-planner', methods=['GET', 'POST'])
def workout_planner():
    if request.method == 'POST':
        time = request.form['time']
        equipment = request.form['equipment']
        muscle = request.form['muscle']
        fitness_level = request.form['fitness_level']
        fitness_goals = request.form['fitness_goals']

        workout_plan = fetch_workout_plan(time, equipment, muscle, fitness_level, fitness_goals)
        return render_template('workout_planner.html', workout_plan=workout_plan)

    return render_template('workout_planner.html')

# Mindfulness route
@app.route('/mindfulness')
def mindfulness():
    return render_template('mindfulness.html')

# Mood tracking route
@app.route('/mood-tracking', methods=['GET', 'POST'])
def mood_tracking():
    if request.method == 'POST':
        mood = request.form['mood']
        notes = request.form['notes']
        print(f"Mood: {mood}, Notes: {notes}")
        return redirect(url_for('home'))

    return render_template('mood_tracking.html')

# Add this new route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload-health-data', methods=['POST'])
def upload_health_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filepath': filepath})
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
