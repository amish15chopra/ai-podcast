import os
from openai import OpenAI
import requests
import json

# Load API keys from environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
VOICE_API_KEY = os.environ.get('VOICE_API_KEY')
ELEVENLABS_URL = 'https://api.elevenlabs.io/v1/text-to-speech'

# Initialize OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to generate the conversation using OpenAI
def generate_podcast_conversation(topic):
    prompt = f"""
    You are generating a highly engaging podcast conversation about the topic "{topic}". The podcast features two speakers:
    
    Speaker 1: Emma – A curious learner, always asking insightful questions to dig deeper into the topic. Her tone is friendly, engaging, and relatable. She is keen to understand complex topics in simple terms.
    
    Speaker 2: Chris – A highly knowledgeable guest at the podcasts who is inspired by Richard Feynman’s teaching methods. He excels at breaking down difficult concepts into bite-sized, relatable analogies, while also diving into the technical aspects when needed. His tone is approachable, enthusiastic, and encouraging.

    Structure the conversation like this:

    1. **Introduction:**
       - Emma starts by introducing the topic and asking Chris to give a high-level overview.
       - Chris explains the core concept in a simple, engaging way, using a real-world analogy that the audience can relate to.

    2. **Deeper Exploration:**
       - Emma asks more detailed questions, pushing Chris to dive deeper.
       - Chris offers a technical breakdown but keeps it easy to follow. He blends analogies with facts, making sure the listeners don’t get lost in jargon.

    3. **Engagement and Interaction:**
       - Emma responds enthusiastically, asks clarifying questions, and shares her own perspective, making the conversation more interactive.
       - Chris answers these questions in an intuitive way, keeping the conversation dynamic.

    4. **Testing Understanding:**
       - Chris asks Emma some thought-provoking questions, testing her understanding of the topic in a fun and engaging manner.
       - Emma works through the questions, sometimes getting stuck, but Chris offers encouraging feedback and clarifies as needed.

    5. **Conclusion:**
       - Emma summarizes the key takeaways of the discussion in her own words.
       - Chris wraps up with a motivational and forward-looking statement, hinting at how the audience can apply this knowledge in their daily lives or explore the topic further.
    
    The conversation should be lively, filled with back-and-forth dialogue, and paced in a way that keeps listeners engaged and entertained, while learning something new.
    """

    # Generate the conversation using the more cost-effective gpt-4o-mini
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1500,
    n=1,
    stop=None,
    temperature=0.7)

    conversation = response.choices[0].message.content.strip()
    return conversation

# Function to convert text to speech using ElevenLabs (or similar)
def text_to_speech(conversation, speaker_name):
    headers = {
        "Authorization": f"Bearer {VOICE_API_KEY}",
        "Content-Type": "application/json"
    }

    # For simplicity, we split the conversation by speaker and send it to the voice generation API
    data = {
        "voice": speaker_name,
        "text": conversation
    }

    response = requests.post(ELEVENLABS_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.content  # Audio binary
    else:
        raise Exception(f"Failed to generate speech: {response.status_code}, {response.text}")

# Function to save the audio file
def save_audio_file(audio_content, filename):
    with open(filename, 'wb') as audio_file:
        audio_file.write(audio_content)

# Main function to generate podcast for a given topic
def generate_podcast(topic):
    print(f"Generating podcast conversation for topic: {topic}")

    conversation = generate_podcast_conversation(topic)

    # Split conversation by speakers for voice generation
    emma_lines = "\n".join([line for line in conversation.split("\n") if "Emma:" in line])
    chris_lines = "\n".join([line for line in conversation.split("\n") if "Chris:" in line])

    # # Generate speech for both speakers
    # print("Generating voice for Emma...")
    # emma_audio = text_to_speech(emma_lines, "Emma")  # Adjust with the name of Emma's voice
    # save_audio_file(emma_audio, "emma_audio.mp3")

    # print("Generating voice for Chris...")
    # chris_audio = text_to_speech(chris_lines, "Chris")  # Adjust with the name of Chris's voice
    # save_audio_file(chris_audio, "chris_audio.mp3")

    # print("Podcast generation complete. Audio files saved!")

    # Save conversation lines
    with open(f"conversation_{topic}.txt", "w") as f:
        f.write(conversation)

    # Save Emma's lines
    with open(f"emma_lines_{topic}.txt", "w") as f:
        f.write(emma_lines)

    # Save Chris's lines
    with open(f"chris_lines_{topic}.txt", "w") as f:
        f.write(chris_lines)

    print("Conversation text files saved!")



if __name__ == "__main__":
    user_topic = input("Enter the topic for your podcast: ")
    generate_podcast(user_topic)