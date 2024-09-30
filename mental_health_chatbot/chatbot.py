import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Follow-up questions and combined advice for various emotions
emotional_advice = {
    'admiration': {
        'followups': [
            "That’s wonderful! Who or what do you admire the most right now?",
            "How does admiring this person/thing inspire you?"
        ],
        'advice': "Channel your admiration into motivation; consider how you can emulate the qualities you appreciate."
    },
    'anger': {
        'followups': [
            "I'm sorry you're feeling angry. Would you like to talk more about what's causing your anger?",
            "What steps can you take to calm down and address the situation?"
        ],
        'advice': "Take deep breaths and step back from the situation. It may help to write down your feelings."
    },
    'sadness': {
        'followups': [
            "It’s okay to feel sad sometimes. Do you want to talk about what’s making you sad?",
            "What can you do to lift your spirits a bit?"
        ],
        'advice': "Consider reaching out to a friend or engaging in an activity you enjoy to help ease your sadness."
    },
    'joy': {
        'followups': [
            "That’s amazing! What’s bringing you joy today?",
            "How can you spread this joy to others around you?"
        ],
        'advice': "Share your joy with someone else; happiness grows when shared."
    },
    'nervousness': {
        'followups': [
            "Nervousness can be tough. What’s making you nervous right now?",
            "Have you tried any relaxation techniques like deep breathing or visualization?"
        ],
        'advice': "Practice grounding techniques or visualization to manage your nervousness."
    },
    'fear': {
        'followups': [
            "I’m here for you. What’s making you feel afraid?",
            "Is there anything specific that helps you feel safe in situations like this?"
        ],
        'advice': "Identify your fear and think of ways to confront it step by step."
    },
    'disgust': {
        'followups': [
            "I understand that feeling. What specifically is making you feel disgusted?",
            "How can you distance yourself from that feeling?"
        ],
        'advice': "Reflect on what you can change in your environment to minimize feelings of disgust."
    },
    'surprise': {
        'followups': [
            "Surprises can be exciting! What surprised you the most recently?",
            "How do you feel about unexpected changes in your life?"
        ],
        'advice': "Embrace the surprise as an opportunity for growth or a new experience."
    },
    'trust': {
        'followups': [
            "Trust is important. Who do you trust the most in your life?",
            "What helps you build trust with others?"
        ],
        'advice': "Foster trust through open communication and shared experiences."
    },
    'anticipation': {
        'followups': [
            "What are you looking forward to?",
            "How does anticipating something make you feel?"
        ],
        'advice': "Use this feeling of anticipation to set goals and prepare for upcoming events."
    },
    'contentment': {
        'followups': [
            "That’s great to hear! What is making you feel content right now?",
            "How can you maintain this feeling of contentment?"
        ],
        'advice': "Take a moment to appreciate your achievements and the present moment."
    },
    'frustration': {
        'followups': [
            "Frustration can be challenging. What’s causing your frustration?",
            "How do you usually cope with feelings of frustration?"
        ],
        'advice': "Try to identify the source of your frustration and develop a plan to tackle it."
    },
    'confusion': {
        'followups': [
            "It’s okay to feel confused. What’s on your mind that’s causing confusion?",
            "Have you tried breaking down the situation into smaller parts?"
        ],
        'advice': "Take a step back and simplify the situation. Ask for help if needed."
    },
    'guilt': {
        'followups': [
            "Guilt can be tough. What’s making you feel guilty?",
            "Is there a way to make amends or learn from this experience?"
        ],
        'advice': "Reflect on the situation and consider what steps you can take to move forward positively."
    },
    'shame': {
        'followups': [
            "Shame can be a heavy burden. What’s making you feel this way?",
            "How can you practice self-compassion in this situation?"
        ],
        'advice': "Remember that everyone makes mistakes. Focus on self-forgiveness and growth."
    },
    'overwhelm': {
        'followups': [
            "Feeling overwhelmed is common. What’s contributing to that feeling?",
            "Would it help to prioritize your tasks or take a break?"
        ],
        'advice': "Break tasks into smaller, manageable steps and give yourself permission to take breaks."
    },
    'hope': {
        'followups': [
            "Hope is a powerful emotion. What gives you hope right now?",
            "How can you nurture this feeling of hope in your life?"
        ],
        'advice': "Focus on positive outcomes and surround yourself with supportive people."
    },
    'loneliness': {
        'followups': [
            "I'm sorry you're feeling lonely. Do you want to talk about it?",
            "What connections can you reach out to right now?"
        ],
        'advice': "Consider reaching out to friends or engaging in community activities."
    },
    'embarrassment': {
        'followups': [
            "It’s natural to feel embarrassed sometimes. What’s making you feel this way?",
            "How can you shift your perspective on this situation?"
        ],
        'advice': "Remember that everyone has embarrassing moments; try to laugh it off."
    },
    'nostalgia': {
        'followups': [
            "Nostalgia can be bittersweet. What memories are you thinking about?",
            "How do these memories affect your current feelings?"
        ],
        'advice': "Cherish the good memories while focusing on creating new ones."
    },
    'relief': {
        'followups': [
            "Relief is a wonderful feeling. What made you feel relieved?",
            "How can you recreate that feeling of relief in the future?"
        ],
        'advice': "Identify the actions that brought you relief and incorporate them into your routine."
    },
    'boredom': {
        'followups': [
            "Boredom can be a sign to explore new interests. What’s been boring you lately?",
            "What new activities would you like to try?"
        ],
        'advice': "Use this time to experiment with new hobbies or revisit old ones."
    },
    'excitement': {
        'followups': [
            "That sounds exciting! What’s making you feel this way?",
            "How can you channel this excitement into something productive?"
        ],
        'advice': "Make plans to pursue what excites you and share it with others."
    },
    'interest': {
        'followups': [
            "It's great to feel interested in something. What has caught your attention?",
            "How can you deepen your understanding or involvement in that area?"
        ],
        'advice': "Engage in discussions or activities that explore your interest further."
    },
    'envy': {
        'followups': [
            "Feeling envious is normal. What are you feeling envious about?",
            "How can you turn that envy into motivation?"
        ],
        'advice': "Identify what you admire in others and set goals to achieve those traits."
    },
    'disappointment': {
        'followups': [
            "Disappointment can be hard to cope with. What’s making you feel disappointed?",
            "How can you reframe this situation to find a silver lining?"
        ],
        'advice': "Look for lessons in the disappointment and consider it a stepping stone to growth."
    },
    'satisfaction': {
        'followups': [
            "Satisfaction is a lovely feeling. What has contributed to your satisfaction?",
            "How can you ensure you continue feeling satisfied?"
        ],
        'advice': "Reflect on your accomplishments and set new goals to maintain this feeling."
    },
    'regret': {
        'followups': [
            "Regret can weigh heavy. What do you wish you had done differently?",
            "Is there a lesson you can take away from this experience?"
        ],
        'advice': "Focus on what you can do moving forward instead of dwelling on the past."
    },
    'peace': {
        'followups': [
            "Peace is wonderful to feel. What brings you peace in your life?",
            "How can you create more moments of peace?"
        ],
        'advice': "Engage in mindfulness practices or activities that promote tranquility."
    },
    'neutral': {
        'followups': [
            "You're feeling neutral. That's a balanced place to be. How can I assist you today?",
            "Is there anything on your mind that you’d like to talk about?"
        ],
        'advice': "Use this time to reflect on your feelings and identify areas of focus."
    }
}

# Function to call Gemini API
def get_gemini_response(user_input):
    api_key = os.getenv('GEMINI_API_KEY')
    api_url = "https://api.gemini.com/v1/chat"  # Replace with actual Gemini API endpoint
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    data = {'message': user_input}
    
    response = requests.post(api_url, headers=headers, json=data)
    return response.json() if response.status_code == 200 else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    gemini_response = get_gemini_response(user_message)

    if gemini_response:
        emotion_detected = gemini_response.get('emotion', 'neutral')
        followup = emotional_advice[emotion_detected]['followups'][0]
        advice = emotional_advice[emotion_detected]['advice']
        response_message = f"{gemini_response['response']} {followup} {advice}"
    else:
        response_message = "I'm sorry, I couldn't understand that."

    return jsonify({'response': response_message})

if __name__ == '__main__':
    app.run(debug=True)
