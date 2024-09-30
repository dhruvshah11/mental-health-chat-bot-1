// Add event listener to the send button
document.getElementById('send-button').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the default form submission
    
    const userInput = document.getElementById('user-input').value;

    if (userInput.trim() === '') {
        alert('Please enter a message.');
        return;
    }

    // Append the user's message to the chat box
    appendMessage('user', userInput);
    
    // Send the user input to the server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'message': userInput // Send the user's input to the server
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const botResponse = data.response;  // Retrieve the bot's response
        appendMessage('bot', botResponse);
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('bot', 'An error occurred while communicating with the server.');
    });

    // Clear the input box after sending the message
    document.getElementById('user-input').value = '';
});

// Function to append messages to the chat box
function appendMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}
