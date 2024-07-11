// // Get elements
// const startButton = document.getElementById('mic-button');
// const cancelButton = document.getElementById('cancel-button');
// const output = document.getElementById('status-message');
// const card = document.getElementById('card');
// const botImage = document.getElementById('bot-image');
//
// // Create SpeechRecognition instance
// const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
//
// // Configure recognition
// recognition.lang = 'en-US';
// recognition.interimResults = false;
// recognition.maxResults = 10;
//
// // Event listeners
// recognition.onresult = handleResult;
// recognition.onend = handleEnd;
//
// startButton.addEventListener('click', startRecognition);
// cancelButton.addEventListener('click', cancelRecognition);
//
// // Functions
// function handleResult(event) {
//     const transcript = event.results[0][0].transcript;
//     output.textContent = `You said: ${transcript}`;
//     fetchResponse(transcript);
// }
//
// function handleEnd() {
//     card.classList.remove('listening');
// }
//
// function startRecognition() {
//     card.classList.add('listening');
//     recognition.start();
// }
//
// function cancelRecognition() {
//     recognition.abort();
//     card.classList.remove('listening');
// }
//
// function fetchResponse(transcript) {
//     fetch('/api/process', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ text: transcript }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         output.textContent += `\nAssistant: ${data.response}`;
//         speakResponse(data.response);
//     });
// }
//
// function speakResponse(text) {
//     const utterance = new SpeechSynthesisUtterance(text);
//     window.speechSynthesis.speak(utterance);
// }


const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
const startButton = document.getElementById('startButton');
const messageElement = document.querySelector('.message');
const statusMessageElement = document.querySelector('.status-message');

recognition.lang = 'en-US';
recognition.interimResults = false;

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    messageElement.textContent = `You said: ${transcript}`;
    fetchResponse(transcript);
};

recognition.onstart = () => {
    statusMessageElement.textContent = "Listening...";
};

recognition.onend = () => {
    statusMessageElement.textContent = "";
};

function startVoiceRecognition() {
    recognition.start();
}

function cancelVoiceRecognition() {
    recognition.stop();
    statusMessageElement.textContent = "Voice recognition canceled.";
}

function fetchResponse(transcript) {
    fetch('/api/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: transcript }),
    })
    .then(response => response.json())
    .then(data => {
        messageElement.textContent += `\nAssistant: ${data.response}`;
        speakResponse(data.response);
    });
}

function speakResponse(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}