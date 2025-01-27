# backend/app.py (Flask API)
from flask import Flask, jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Helper functions
def get_zodiac(birth_date):
    # Mock zodiac calculation
    dates = [(120, 'Capricorn'), (219, 'Aquarius'), (320, 'Pisces'),
             (420, 'Aries'), (521, 'Taurus'), (621, 'Gemini')]
    date_num = int(birth_date.strftime("%m%d"))
    return next((zodiac for num, zodiac in dates if date_num <= num), 'Gemini')

def generate_horoscope(commits):
    # Simple Markov-style horoscope
    predictions = [
        "Beware of merge conflicts during Mercury retrograde",
        "Your code shall inherit the wisdom of the Pythonic ancients",
        "A mysterious stranger will review your PR favorably"
    ]
    return predictions[len(commits) % len(predictions)]

@app.route('/analyze/<username>/<repo>')
def analyze_repo(username, repo):
    # Get GitHub commits
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    url = f'https://api.github.com/repos/{username}/{repo}/commits'
    response = requests.get(url, headers=headers)
    commits = response.json()
    
    # Process data
    commit_data = [{
        'hash': c['sha'][:7],
        'time': c['commit']['author']['date'],
        'message': c['commit']['message'],
        'lines': c['stats']['total'] if 'stats' in c else 0
    } for c in commits[:100]]  # Limit to 100 commits
    
    # Generate constellation data
    stars = []
    for idx, commit in enumerate(commit_data):
        stars.append({
            'x': idx % 10,  # Fake constellation shape
            'y': idx // 10,
            'size': min(commit['lines'] // 10 + 1, 10),
            'color': '#%02x%02x%02x' % (
                idx * 25 % 255,  # Fake color based on position
                idx * 50 % 255,
                idx * 75 % 255
            )
        })
    
    return jsonify({
        'stars': stars,
        'horoscope': generate_horoscope(commits),
        'zodiac': get_zodiac(datetime.now())  # Mock user birthdate
    })

if __name__ == '__main__':
    app.run(port=5000)
