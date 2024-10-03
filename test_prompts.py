prompt1 = f"""
Generate a podcast conversation between two engaging hosts, Host 1 (Emma) and Host 2 (Chris), 
in a casual, friendly, and energetic tone. The conversation should feel natural and conversational, 
designed to inform and entertain listeners, while breaking down the topic step by step in an approachable 
yet insightful way. The language should sound smooth and natural for text-to-speech, avoiding overly 
complex or awkward phrasing.

The topic of the podcast is: {topic}.

Structure the conversation as follows:

1. Introduction:
- Emma introduces the episode’s topic, {topic}, with clear, easy-to-follow language, setting the 
    stage for a fun and insightful conversation.
- Chris adds enthusiasm, using a simple hook to engage the audience and make them curious about 
    what’s coming next.

2. Breaking Down the Core Concept:
- Emma asks Chris to break the topic into smaller, more digestible parts. Chris’s explanation should 
    be clear and conversational, avoiding technical jargon where possible.
- Chris uses everyday analogies and examples to make the concept relatable and easy to understand.
- Both hosts discuss why {topic} is important and relevant, keeping the tone light, with friendly 
    back-and-forth dialogue.

3. Deepening the Discussion:
- Emma asks follow-up questions that flow naturally, encouraging Chris to dive a bit deeper into the 
    technical aspects, but without sounding too dense or overly complex.
- Chris explains more detailed aspects using real-world comparisons, ensuring that the explanations 
    are clear but not too formal. Use language that flows well in spoken form.
- Both hosts address common misconceptions or myths, debunking them in a casual, friendly manner 
    that keeps the conversation engaging and approachable.

4. Exploring Real-World Applications:
- Emma and Chris talk about how {topic} applies to real-life situations, industries, or everyday 
    scenarios, making the examples relatable to a broad audience.
- The dialogue between the hosts should be interactive and dynamic, with natural back-and-forth 
    questions that keep the energy high and conversational.

5. Addressing Assumptions & Background Knowledge:
- If there are any foundational ideas or prerequisites for understanding {topic}, the hosts briefly 
    explain them in simple terms, but without interrupting the flow of the conversation.
- Emma and Chris adjust their explanations based on how familiar they assume the audience might 
    be with the topic, keeping everything accessible but informative.

6. Conclusion & Takeaways:
- Emma wraps up the conversation by summarizing the main points of the discussion in a concise, 
    listener-friendly way.
- Chris adds any final thoughts, such as a thought-provoking question or a practical tip for the audience 
    to consider.
- Both hosts end on a positive, enthusiastic note, encouraging the audience to reflect more on {topic} 
    or explore it further on their own.

Key Instructions:
- The conversation should flow smoothly, avoiding awkward phrasing or overly complex sentence 
structures, ensuring it sounds natural when spoken.
- Keep the tone casual and engaging, with hosts speaking as if they’re having a lively conversation, 
not reading from a script.
- Use relatable analogies and examples to make the conversation easy to follow, while still being 
informative.
- Avoid long monologues. Ensure a balanced dialogue with a natural, interactive back-and-forth 
between the hosts.
"""


prompt2 = f"""
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