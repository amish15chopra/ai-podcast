# AI-Generated Podcast Application

This Python application allows users to generate a podcast by providing a topic. The app uses OpenAI to create a dynamic conversation between two speakers, Emma and Chris, and leverages a text-to-speech API to produce the final audio output. The user can guide the conversation by introducing new ideas or perspectives, creating an interactive podcast experience.

## Features
- **Script Generation**: Automatically generate a conversational podcast script between two distinct speakers based on a user-provided topic.
- **Dynamic Text-to-Speech**: Convert the generated text into realistic speech using a text-to-speech API.
- **Single Audio Track**: Output a single combined audio file with alternating dialogue between Emma and Chris.
- **Interactive Guidance**: Users can introduce new ideas mid-conversation, influencing the direction of the podcast.

## Prerequisites
- Python 3.x
- OpenAI API Key

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ai-podcast.git
   cd ai-podcast
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the required API keys as environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## Usage
1. Activate the virtual environment (optional)
   ```bash
   source ai_podcast_env/bin/activate
   ```

3. Run the script:
   ```bash
   python main.py
   ```

4. The app will generate a podcast script and create a single audio file for the podcast.

### Interactive Mode
To guide the podcast in real-time:
- After entering a topic, you can suggest new ideas or perspective to shape the conversation as it progresses.

## Project Structure
```
ai-podcast-generator/
│
├── main.py                  # Main script to generate podcast
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── history/                 # Folder to store conversation history and audio files
    └── [generated_files]    # Auto-generated content
```  
