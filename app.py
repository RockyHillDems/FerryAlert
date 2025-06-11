from flask import Flask, render_template
import requests
import datetime
import os

app = Flask(__name__)

## get a key for free from https://ctroads.org/developers/doc and store in .env 
KEY = os.getenv("FERRY_API_KEY")

from dotenv import load_dotenv
load_dotenv()

def get_ferry_alert():
    url = "http://ctroads.org/api/v2/get/alerts?key=" + KEY
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                posts = response.json()
                ferry_posts = [post for post in posts if post.get("Id") == 4614]
                if ferry_posts:
                    post = ferry_posts[0]
                    message = post.get('Message', 'No message available.')
                    print(message)
                    start_time = datetime.datetime.fromtimestamp(post.get('StartTime'))
                    start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
                    return f"{message}<br>First Reported: {start_str}"
                else:
                    return "The Rocky Hill Ferry should be running on normal schedule."
            except Exception:
                return "The Rocky Hill Ferry should be running on normal schedule."
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

@app.route('/')
def home():
    result = get_ferry_alert()
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)