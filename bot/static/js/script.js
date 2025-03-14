// const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
// const startButton = document.getElementById('startButton');
// const messageElement = document.querySelector('.message');
// const statusMessageElement = document.querySelector('.status-message');
//
// recognition.lang = 'en-US';
// recognition.interimResults = false;
//
// recognition.onresult = (event) => {
//     const transcript = event.results[0][0].transcript;
//     messageElement.textContent = `You said: ${transcript}`;
//     fetchResponse(transcript);
// };
//
// recognition.onstart = () => {
//     statusMessageElement.textContent = "Listening...";
// };
//
// recognition.onend = () => {
//     statusMessageElement.textContent = "";
// };
//
// function startVoiceRecognition() {
//     recognition.start();
// }
//
// function cancelVoiceRecognition() {
//     recognition.stop();
//     statusMessageElement.textContent = "Voice recognition canceled.";
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
//         messageElement.textContent += `\nAssistant: ${data.response}`;
//         speakResponse(data.response);
//     });
// }
//
// function speakResponse(text) {
//     const utterance = new SpeechSynthesisUtterance(text);
//     window.speechSynthesis.speak(utterance);
// }




// Add browser compatibility check
function checkBrowserCompatibility() {
    const incompatibilities = [];

    if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
        incompatibilities.push("Speech recognition");
    }

    if (!('speechSynthesis' in window)) {
        incompatibilities.push("Speech synthesis");
    }

    if (incompatibilities.length > 0) {
        const message = `Your browser doesn't support: ${incompatibilities.join(', ')}. Some features may not work.`;
        console.warn(message);
        statusMessageElement.textContent = message;
        return false;
    }

    return true;
}

// Initialize speech recognition with better error handling
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;
const startButton = document.getElementById('startButton');
const messageElement = document.querySelector('.message');
const statusMessageElement = document.querySelector('.status-message');

// Keep track of recognition state
let isListening = false;
let recognitionTimeout;

// Check compatibility before proceeding
if (!recognition) {
    statusMessageElement.textContent = "Speech recognition not supported in your browser.";
    if (startButton) {
        startButton.disabled = true;
    }
} else {
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
        clearTimeout(recognitionTimeout);
        const transcript = event.results[0][0].transcript;
        messageElement.textContent = `You said: ${transcript}`;
        fetchResponse(transcript);
    };

    recognition.onstart = () => {
        isListening = true;
        statusMessageElement.textContent = "Listening...";

        // Set timeout to prevent hanging
        recognitionTimeout = setTimeout(() => {
            if (isListening) {
                recognition.stop();
                statusMessageElement.textContent = "Listening timed out. Please try again.";
            }
        }, 10000); // 10-second timeout
    };

    recognition.onend = () => {
        isListening = false;
        clearTimeout(recognitionTimeout);

        // Only clear status if it's still showing "Listening..."
        if (statusMessageElement.textContent === "Listening...") {
            statusMessageElement.textContent = "";
        }
    };

    recognition.onerror = (event) => {
        clearTimeout(recognitionTimeout);
        console.error("Speech recognition error:", event.error);

        // Provide user-friendly error messages
        switch(event.error) {
            case 'no-speech':
                statusMessageElement.textContent = "No speech detected. Please try again.";
                break;
            case 'aborted':
                statusMessageElement.textContent = "Speech recognition was aborted.";
                break;
            case 'network':
                statusMessageElement.textContent = "Network error. Check your connection.";
                break;
            case 'not-allowed':
            case 'permission-denied':
                statusMessageElement.textContent = "Microphone access denied. Please allow microphone access.";
                break;
            default:
                statusMessageElement.textContent = "Error occurred during speech recognition.";
        }
    };
}

function startVoiceRecognition() {
    // Don't start if already listening
    if (isListening) return;

    if (recognition) {
        try {
            recognition.start();
        } catch (error) {
            console.error("Error starting speech recognition:", error);
            statusMessageElement.textContent = "Error starting recognition. Please try again.";
        }
    } else {
        statusMessageElement.textContent = "Speech recognition not supported in your browser.";
    }
}

function cancelVoiceRecognition() {
    if (recognition && isListening) {
        recognition.stop();
        statusMessageElement.textContent = "Voice recognition canceled.";
    }
}

function fetchResponse(transcript) {
    statusMessageElement.textContent = "Processing...";

    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000); // 15-second timeout

    // Get CSRF token if using Django
    const csrftoken = getCookie('csrftoken');
    const headers = {
        'Content-Type': 'application/json'
    };

    if (csrftoken) {
        headers['X-CSRFToken'] = csrftoken;
    }

    fetch('/api/process', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ text: transcript }),
        signal: controller.signal
    })
    .then(response => {
        clearTimeout(timeoutId);
        if (!response.ok) {
            throw new Error('Server error: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        messageElement.textContent += `\nAssistant: ${data.response}`;
        speakResponse(data.response);
        statusMessageElement.textContent = "";
    })
    .catch(error => {
        clearTimeout(timeoutId);
        console.error('Error:', error);

        if (error.name === 'AbortError') {
            statusMessageElement.textContent = "Request timed out. Please try again.";
        } else {
            statusMessageElement.textContent = "Failed to get response. Please try again.";
        }
    });
}

function speakResponse(text) {
    // Check if speech synthesis is available
    if (!window.speechSynthesis) {
        console.error("Speech synthesis not supported");
        return;
    }

    statusMessageElement.textContent = "Speaking...";

    const utterance = new SpeechSynthesisUtterance(text);

    // Add error handling for speech synthesis
    utterance.onerror = (event) => {
        console.error("Speech synthesis error:", event);
        statusMessageElement.textContent = "";
    };

    // Add timeout to reset UI if synthesis hangs
    const timeout = setTimeout(() => {
        if (statusMessageElement.textContent === "Speaking...") {
            window.speechSynthesis.cancel();
            statusMessageElement.textContent = "";
        }
    }, 15000); // 15 second timeout

    utterance.onend = () => {
        clearTimeout(timeout);
        statusMessageElement.textContent = "";
    };

    // Speak the response
    window.speechSynthesis.speak(utterance);
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Check browser compatibility when the script loads
checkBrowserCompatibility();