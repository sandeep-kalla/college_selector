from flask import Flask, request, jsonify
from io import StringIO
import csv

app = Flask(__name__)

# Store CSV data in memory as a list of tuples for better memory efficiency
COLLEGE_DATA = []

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
    
    for line in csv_content.strip().split('\n')[1:]:  # Skip header
        college, branch, rank = line.split(',')
        COLLEGE_DATA.append((college, branch, int(rank)))

def find_top_3_colleges(jee_rank):
    eligible_options = [
        option for option in COLLEGE_DATA 
        if jee_rank <= option[2]
    ]
    return sorted(eligible_options, key=lambda x: x[2])[:3]

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'GET':
        return "Welcome to the College Selector API!"
    
    try:
        jee_rank = int(request.get_json()['jee_rank'])
        top_3_colleges = find_top_3_colleges(jee_rank)
        
        return jsonify([
            {
                "college": college,
                "branch": branch,
                "cutoff_rank": rank
            }
            for college, branch, rank in top_3_colleges
        ]), 200

    except (ValueError, KeyError, TypeError):
        return jsonify({"error": "Invalid input"}), 400

init_college_data()

if __name__ == '__main__':
    app.run()
