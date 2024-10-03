import os
import uuid
from openai import OpenAI
from pydub import AudioSegment
import requests
import json
from pathlib import Path
import re

# Load API key from environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Initialize OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to generate the conversation using OpenAI
def generate_podcast_conversation(topic):
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
    max_tokens=500,
    n=1,
    stop=None, # stop=["Emma:", "Chris:"]
    temperature=0.7)

    conversation = response.choices[0].message.content.strip()
    # Remove markdown formatting using regex
    cleaned_conversation = re.sub(r'[*_`#]', '', conversation)
    return cleaned_conversation

# Function to convert text to speech using ElevenLabs (or similar)
def text_to_speech(conversation, speaker_name):
    # Generate audio using OpenAI's API
    if speaker_name == "Emma":
        voice = "alloy"
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

        # Generate audio for the current line
        audio_content = text_to_speech(text, speaker)
        
        # Save audio to a temporary file
        temp_audio_file = f"{speaker}_temp.mp3"
        with open(temp_audio_file, 'wb') as audio_file:
            audio_file.write(audio_content)

        # Load the generated audio file and append it to the combined audio
        current_audio = AudioSegment.from_file(temp_audio_file)
        combined_audio += current_audio

        # Remove the temporary file
        os.remove(temp_audio_file)

    return combined_audio

# Main function to generate podcast for a given topic
def generate_podcast(topic):
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

    # # Save Emma's lines
    # with open(os.path.join(history_folder, folder_name, f"emma_lines_{topic}.txt"), "w") as f:
    #     f.write(emma_lines)

    # # Save Chris's lines
    # with open(os.path.join(history_folder, folder_name, f"chris_lines_{topic}.txt"), "w") as f:
    #     f.write(chris_lines)

    
if __name__ == "__main__":
    user_topic = input("What's the hot topic for today's podcast? ")
    generate_podcast(user_topic)