# TESH Voice Bot

## Overview

TESH is an advanced conversational voice bot developed using the Gemma model with 2 billion parameters, deployed locally using Ollama. It leverages LangChain and a web speech recognition toolkit to facilitate natural and interactive conversations. The bot is designed to offer a wide range of functionalities and deliver high-quality, context-aware responses.

## Features

- **Conversational AI**: Engage in natural language conversations with the voice bot.
- **Contextual Understanding**: Provides context-aware responses using the Gemma model.
- **Local Deployment**: Deployed locally using Ollama for enhanced performance and privacy.
- **Speech Recognition**: Utilizes web speech recognition for accurate voice input handling.
- **Domain Access**: The bot can be accessed via the public domain `https://tesh.loca.lt`, allowing for easy remote access during development.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/tesh-voice-bot.git
   cd tesh-voice-bot
   ```

2. **Install Dependencies:**

   Ensure you have Python 3.8 or higher installed. Create a virtual environment and install the required packages:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Install Ollama:**

   Download and install Ollama from the [Ollama website](https://ollama.com/download). Follow the installation instructions provided.

4. **Configure Ollama:**

   Once installed, follow the configuration steps in the [Ollama documentation](https://ollama.com/docs) to ensure proper setup and integration with your system.

5. **Setup Gemma Model:**

   Follow the setup instructions for the Gemma model provided in its documentation to ensure proper configuration.

6. **Run the Bot:**

   Use the provided `run.sh` script to start both the Django server and the LocalTunnel instance:

   ```bash
   ./run.sh
   ```

   The bot will be accessible locally, and the LocalTunnel will generate a public URL (`https://tesh.loca.lt`) that you can use to access the bot remotely.

## Usage

- **Start Interaction**: Once the bot is running, it will start listening for voice inputs.
- **Remote Access**: The bot is accessible via the `https://tesh.loca.lt` domain, allowing for remote interaction.
- **Voice Commands**: Speak naturally, and the bot will process and respond based on the given context.

## Configuration

You may configure various aspects of the bot by modifying the configuration files located in the `config/` directory:

- `config/settings.yml`: Adjust model parameters and other settings.
- `config/ollama_config.json`: Configure Ollama deployment settings.

## Contributing

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes**

   ```bash
   git commit -am 'Add new feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**

   Submit a pull request to the main repository for review.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/theshashank1/tesh-voice-bot?tab=MIT-1-ov-file) file for details.

## Contact


For any questions or support, please contact [shashankgundas1@gmail.com](mailto:shashankgundas1@gmail.com).

---
