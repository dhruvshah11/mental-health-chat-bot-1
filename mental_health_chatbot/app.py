import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Emotional Advice Database (28 common emotions and advice)
EMOTIONS_ADVICE = {
    "joy": "It's great to feel joyful! Keep embracing positivity and share your happiness with others.",
    "sadness": "I'm sorry you're feeling down. Sometimes talking to someone can help. You are not alone.",
    "anger": "It's normal to feel anger, but it's important to channel it positively. Try some deep breathing or physical exercise to release the tension.",
    "anxiety": "Anxiety can be overwhelming. Try grounding exercises like deep breathing or a short walk to help ease it.",
    "fear": "It's natural to feel fear. Consider facing it gradually and seeking support from friends or family.",
    "disgust": "Feeling disgust is valid. Reflect on what you can change in your environment to feel better.",
    "surprise": "Surprises can be exciting! Embrace them as opportunities for growth.",
    "trust": "Building trust takes time. Communicate openly and engage in shared experiences.",
    "anticipation": "Use your excitement to motivate yourself for the future. Plan for what you're looking forward to.",
    "contentment": "Feeling content is wonderful. Take a moment to appreciate your achievements and the present.",
    "frustration": "Frustration can be challenging. Identify the source and develop a plan to tackle it.",
    "confusion": "It's okay to feel confused. Break down the situation and ask for help if needed.",
    "guilt": "Guilt can weigh heavy. Reflect on the situation and consider steps to move forward positively.",
    "shame": "Remember that everyone makes mistakes. Focus on self-forgiveness and growth.",
    "overwhelm": "Feeling overwhelmed is common. Break tasks into manageable steps and take breaks.",
    "hope": "Focus on positive outcomes and surround yourself with supportive people.",
    "loneliness": "I'm sorry you're feeling lonely. Reach out to friends or engage in community activities.",
    "embarrassment": "It’s natural to feel embarrassed sometimes. Try to laugh it off and remember you’re not alone.",
    "nostalgia": "Cherish the good memories while focusing on creating new ones.",
    "relief": "Identify the actions that brought you relief and incorporate them into your routine.",
    "boredom": "Use this time to explore new interests or revisit old hobbies.",
    "excitement": "Channel your excitement into something productive and share it with others.",
    "interest": "Engage in discussions or activities that explore your interests further.",
    "envy": "Identify what you admire in others and set goals to achieve those traits.",
    "disappointment": "Look for lessons in disappointment and consider it a stepping stone to growth.",
    "satisfaction": "Reflect on your accomplishments and set new goals to maintain this feeling.",
    "regret": "Focus on what you can do moving forward instead of dwelling on the past.",
    "peace": "Engage in mindfulness practices or activities that promote tranquility.",
    "neutral": "You're feeling neutral. That's a balanced place to be. Is there anything on your mind that you’d like to talk about?"
}

# Function to call Gemini API
def get_gemini_response(user_input):
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"API Key: {api_key}")  # Debug line
    api_url = "https://api.gemini.com/v1/chat"  # Replace with actual Gemini API endpoint
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    data = {'message': user_input}
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get('response', 'Sorry, I didn’t get that.')
        else:
            return f'Error: {response.status_code} - {response.text}'
    except Exception as e:
        return f'An error occurred while connecting to the API: {str(e)}'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    
    # Call the API function
    bot_response = get_gemini_response(user_input)
    
    return jsonify({'response': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
