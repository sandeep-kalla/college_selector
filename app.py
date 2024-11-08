from flask import Flask, render_template, request, jsonify
import os
import csv
from io import StringIO

app = Flask(__name__)

# Store CSV data in memory as a list of dictionaries
COLLEGE_DATA = []

# Initialize data when the app starts
def init_college_data():
    csv_content = '''College,Branch,Rank
IIT Bombay,Computer Science and Engineering,1
IIT Delhi,Computer Science and Engineering,2
IIT Madras,Computer Science and Engineering,3
IIT Kanpur,Computer Science and Engineering,4
IIT Kharagpur,Computer Science and Engineering,5
IIT Roorkee,Computer Science and Engineering,6
IIT Guwahati,Computer Science and Engineering,7
IIT Hyderabad,Computer Science and Engineering,8
IIT Bombay,Electrical Engineering,9
IIT Delhi,Electrical Engineering,10
IIT Madras,Electrical Engineering,11
IIT Kanpur,Electrical Engineering,12
IIT Kharagpur,Electrical Engineering,13
IIT Roorkee,Electrical Engineering,14
IIT Guwahati,Electrical Engineering,15
IIT Hyderabad,Electrical Engineering,16
IIT Bombay,Mechanical Engineering,17
IIT Delhi,Mechanical Engineering,18
IIT Madras,Mechanical Engineering,19
IIT Kanpur,Mechanical Engineering,20
IIT Kharagpur,Mechanical Engineering,21
IIT Roorkee,Mechanical Engineering,22
IIT Guwahati,Mechanical Engineering,23
IIT Hyderabad,Mechanical Engineering,24
IIT Bombay,Chemical Engineering,25
IIT Delhi,Chemical Engineering,26
IIT Madras,Chemical Engineering,27
IIT Kanpur,Chemical Engineering,28
IIT Kharagpur,Chemical Engineering,29
IIT Roorkee,Chemical Engineering,30
IIT Guwahati,Chemical Engineering,31
IIT Hyderabad,Chemical Engineering,32
IIT Bombay,Civil Engineering,33
IIT Delhi,Civil Engineering,34
IIT Madras,Civil Engineering,35
IIT Kanpur,Civil Engineering,36
IIT Kharagpur,Civil Engineering,37
IIT Roorkee,Civil Engineering,38
IIT Guwahati,Civil Engineering,39
IIT Hyderabad,Civil Engineering,40
IIT Bombay,Aerospace Engineering,41
IIT Madras,Aerospace Engineering,42
IIT Kanpur,Aerospace Engineering,43
IIT Kharagpur,Aerospace Engineering,44
IIT Bombay,Metallurgical Engineering,45
IIT Madras,Metallurgical Engineering,46
IIT Kanpur,Metallurgical Engineering,47
IIT Kharagpur,Metallurgical Engineering,48
IIT Roorkee,Metallurgical Engineering,49
IIT Bombay,Engineering Physics,50
IIT Delhi,Engineering Physics,51
IIT Madras,Engineering Physics,52
IIT Kanpur,Engineering Physics,53
IIT Kharagpur,Engineering Physics,54'''
    
    csv_file = StringIO(csv_content)
    reader = csv.DictReader(csv_file)
    for row in reader:
        COLLEGE_DATA.append({
            'College': row['College'],
            'Branch': row['Branch'],
            'Rank': row['Rank']
        })

def find_top_3_colleges(jee_rank):
    eligible_options = []
    try:
        for row in COLLEGE_DATA:
            cutoff_rank_str = row['Rank']
            if cutoff_rank_str.isdigit():
                cutoff_rank = int(cutoff_rank_str)
                if jee_rank <= cutoff_rank:
                    eligible_options.append((
                        row['College'],
                        row['Branch'],
                        cutoff_rank
                    ))
        eligible_options.sort(key=lambda x: x[2])
        return eligible_options[:3]
    except Exception:
        return None

@app.route('/')
def home():
    return "Welcome to the College Selector API!"

@app.route('/', methods=['POST'])
def api_colleges():
    try:
        data = request.get_json()
        jee_rank = int(data['jee_rank'])
        top_3_colleges = find_top_3_colleges(jee_rank)

        if top_3_colleges is None:
            return jsonify({"error": "Error processing request"}), 500

        response = [
            {"college": college, "branch": branch, "cutoff_rank": cutoff_rank}
            for college, branch, cutoff_rank in top_3_colleges
        ]
        return jsonify(response), 200

    except (ValueError, KeyError):
        return jsonify({"error": "Invalid input"}), 400

# Initialize the college data when the app starts
init_college_data()

if __name__ == '__main__':
    app.run(debug=True)
