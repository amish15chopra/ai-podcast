import os
import uuid
from openai import OpenAI
from pydub import AudioSegment
from pathlib import Path
import re
from flask import Flask, request, jsonify, send_from_directory, render_template, session

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Load API key from environment variables
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

@app.route('/')
def index():
    return render_template('index.html')

# Function to generate the conversation using OpenAI
def generate_podcast_conversation(topic, conversation_history=None, new_idea=None):
    if not conversation_history and not new_idea:
        prompt = f"""
        You are an expert podcast script writer. Your role is to craft engaging and dynamic podcast scripts 
        involving two speakers, Emma and Chris, discussing a topic chosen by the user. Your job is to generate 
        only the dialogue for the script, as it will be read by two AI-generated text-to-speech voices. The 
        conversation should be informative, entertaining, and conversational, ensuring that both hosts engage 
        in meaningful dialogue while breaking down the topic in an approachable way.

        The topic of this podcast is: {topic}.

        Key instructions for the dialogue:

        1. **Tone**:
        - The tone should be casual, friendly, and energetic, engaging listeners while keeping them informed.
        - The dialogue should feel natural and spontaneous, avoiding overly formal or complex language.
        - Use relatable examples and analogies to simplify the topic and make it easy to understand.
        - Ensure both hosts speak in a balanced, back-and-forth conversation to maintain a dynamic interaction.

        2. **Structure**:
        - The dialogue should be divided into the following sections:

        a. **Introduction**:
            - Emma starts by introducing the episode’s topic, {topic}, and what listeners can expect.
            - Chris follows up with enthusiasm and adds a hook or interesting fact to draw in the audience.

        b. **Explaining the Topic**:
            - Emma asks Chris to explain the topic in simple terms.
            - Chris gives a clear, engaging explanation using everyday analogies.
            - Both Emma and Chris discuss why {topic} is relevant and interesting today, in a conversational manner.

        c. **Deep Dive**:
            - Emma asks a follow-up question, encouraging Chris to dive deeper into the topic.
            - Chris elaborates with more technical details, using real-world examples to keep it relatable.
            - They both address any common misconceptions or myths, debunking them in a friendly tone.

        d. **Real-World Applications**:
            - Emma and Chris explore how {topic} is used or applied in real life or specific industries, using 
                examples the audience can relate to.
            - They engage in a back-and-forth conversation, asking each other open-ended questions to keep 
                the discussion lively.

        e. **Conclusion**:
            - Emma wraps up the conversation by summarizing the key takeaways.
            - Chris adds a final thought, potentially a call to action or something for the audience to think about.
            - Both hosts end on a high note, encouraging the audience to explore the topic further.

        3. **Balanced Dialogue**:
        - Alternate between Emma and Chris frequently to keep the energy high and ensure both hosts are 
            actively participating.
        - Avoid long monologues; ensure the dialogue feels dynamic, with questions, responses, and interactive 
            conversation.

        Please generate only the dialogue for this podcast script, using Emma and Chris as the speakers.
        """
        print("Generating initial conversation on: {topic}")

    else:
        prompt = f"""
        You are an expert podcast script writer. Your role is to continue the podcast script 
        involving two speakers, Emma and Chris, discussing a topic chosen by the user. Your job 
        is to generate only the dialogue for the script, as it will be read by two AI-generated 
        text-to-speech voices. The conversation should be informative, entertaining, and conversational, 
        ensuring that both hosts engage in meaningful dialogue while breaking down the topic in an 
        approachable way.

        The conversation history is: {conversation_history}.

        A new idea or perspective has been introduced: {new_idea}

        Please continue the conversation, incorporating this new idea or perspective. You can use the 
        conversation history as context, but focus on exploring the new idea in relation to the original topic. 
        Ensure that the dialogue remains natural and engaging, with both Emma and Chris contributing to the discussion.
        """
        print(f"Continuing conversation on: {new_idea}")

    # Generate the conversation using the more cost-effective gpt-4o-mini
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """You are an expert podcast script writer. 
            Your task is to create engaging, dynamic podcast scripts with two hosts, Emma and Chris, that sound natural when spoken aloud. 
            Ensure the dialogue flows conversationally, focusing on clear explanations of {topic}, balanced with entertainment and information. 
            Keep the tone casual, friendly, and energetic. Structure the podcast with an introduction, in-depth exploration, practical examples, and a strong conclusion. 
            Your job is to make the podcast both educational and entertaining, ensuring high listener engagement."""},
        {"role": "user", "content": prompt}
    ],
    max_tokens=100,
    n=1,
    stop=None, # stop=["Emma:", "Chris:"]
    temperature=0.7)

    conversation = response.choices[0].message.content.strip()
    # Remove markdown formatting using regex
    cleaned_conversation = re.sub(r'[*_`#]', '', conversation)
    return cleaned_conversation

# Function to convert text to speech using OpenAI TTS
def text_to_speech(conversation, speaker_name):
    if speaker_name == "Emma":
        voice = "nova"
    elif speaker_name == "Chris":
        voice = "echo"
    else:
        raise ValueError(f"Invalid speaker name: {speaker_name}")

    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=conversation
    )

    return response.content  # Audio binary


# Function to create a single audio track from alternating dialogue
def generate_podcast_audio(conversation):
    print("Sit tight, voices are warming up...")

    # Initialize an empty audio segment
    combined_audio = AudioSegment.silent(duration=0)  # Start with silence

    # Split the conversation by lines
    lines = conversation.split("\n")

    for line in lines:
        if line.startswith("Emma:"):
            speaker = "Emma"
            text = line.replace("Emma:", "").strip()
        elif line.startswith("Chris:"):
            speaker = "Chris"
            text = line.replace("Chris:", "").strip()
        else:
            continue  # Skip any line that doesn't start with Emma or Chris

        # Check if text is not empty before calling text_to_speech
        if text:
            audio_content = text_to_speech(text, speaker)
            temp_audio_file = f"{speaker}_temp.mp3"
            with open(temp_audio_file, 'wb') as audio_file:
                audio_file.write(audio_content)

            current_audio = AudioSegment.from_file(temp_audio_file)
            combined_audio += current_audio
            os.remove(temp_audio_file)
        else:
            print(f"Warning: Skipping empty text for {speaker}")

    return combined_audio

# Main function to generate podcast for a given topic
# Endpoint to generate a podcast
@app.route('/generate_podcast', methods=['POST'])
def generate_podcast():
    data = request.json
    topic = data.get('topic')

    if not topic:
        return jsonify({"error": "Topic is required"}), 400
    
    print(f"Buckle up! Crafting an epic convo on: {topic}")
    # Generate the conversation
    conversation = generate_podcast_conversation(topic)

    # Generate the combined audio track from the conversation
    combined_audio = generate_podcast_audio(conversation)

    # Create a folder with the name of the topic
    history_folder = "history"
    folder_name = f"{topic.replace(' ', '_')}_{str(uuid.uuid4())[:8]}"  # Replace spaces with underscores and append unique ID
    os.makedirs(os.path.join(history_folder, folder_name), exist_ok=True)

    # Save the final combined audio file
    combined_audio_file = os.path.join(history_folder, folder_name, f"{topic.replace(' ', '_')}.mp3")
    combined_audio.export(combined_audio_file, format='mp3')
    print(f"Podcast magic is complete! Your audio masterpiece is saved as {combined_audio_file}")

    # Save the conversation text file
    with open(os.path.join(history_folder, folder_name, f"conversation_{topic.replace(' ', '_')}.txt"), "w") as f:
        f.write(conversation)
    print(f"Script archived in {folder_name}")

    # Store the folder name in the session for later use
    session['folder_name'] = folder_name

    # Return the URL to the audio file
    audio_file_url = f"/history/{folder_name}/{topic.replace(' ', '_')}.mp3"

    return jsonify({
        "message": "Podcast generated successfully!",
        "audio_file": audio_file_url,
        "conversation_file": os.path.join(history_folder, folder_name, f"conversation_{topic.replace(' ', '_')}.txt")
    }), 200

    # # Save Emma's lines
    # with open(os.path.join(history_folder, folder_name, f"emma_lines_{topic}.txt"), "w") as f:
    #     f.write(emma_lines)

    # # Save Chris's lines
    # with open(os.path.join(history_folder, folder_name, f"chris_lines_{topic}.txt"), "w") as f:
    #     f.write(chris_lines)


# Endpoint to extend the conversation
import time  # Import time for timestamping

@app.route('/extend_conversation', methods=['POST'])
def extend_conversation():
    data = request.json
    topic = data.get('topic')
    new_idea = data.get('new_idea')

    if not topic or not new_idea:
        return jsonify({"error": "Topic and new idea are required"}), 400

    # Load the existing conversation file using the folder name stored in the session
    folder_name = session.get('folder_name')
    if not folder_name:
        return jsonify({"error": "No active podcast session found"}), 400

    conversation_file = os.path.join("history", folder_name, f"conversation_{topic.replace(' ', '_')}.txt")
    if not os.path.exists(conversation_file):
        return jsonify({"error": "Conversation file not found"}), 404

    with open(conversation_file, "r") as f:
        conversation_history = f.read()

    # Pass the new_idea to extend the conversation
    conversation_extended = generate_podcast_conversation(topic, conversation_history, new_idea)

    # Generate the combined audio track from the extended conversation
    combined_audio = generate_podcast_audio(conversation_extended)

    # Create a unique filename for the extended conversation
    timestamp = int(time.time())  # Get the current timestamp
    extended_conversation_file = os.path.join("history", folder_name, f"conversation_{topic.replace(' ', '_')}_{timestamp}.txt")

    # Save the extended conversation text file with a unique name
    with open(extended_conversation_file, "w") as f:
        f.write(conversation_extended)
    print(f"Conversation extended and archived in {folder_name} as {extended_conversation_file}")

    # Save the extended conversation audio file with a unique name
    combined_audio_file = os.path.join("history", folder_name, f"{topic.replace(' ', '_')}_{timestamp}.mp3")
    combined_audio.export(combined_audio_file, format='mp3')
    print(f"Extended conversation audio saved as {combined_audio_file}")

    # Return the URL to the audio file
    audio_file_url = f"/history/{folder_name}/{topic.replace(' ', '_')}_{timestamp}.mp3"

    return jsonify({
        "message": "Conversation extended successfully!",
        "audio_file": audio_file_url,
        "conversation_file": extended_conversation_file
    }), 200 

# Serve static files
@app.route('/history/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('history', filename)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)  # Bind to all IP addresses