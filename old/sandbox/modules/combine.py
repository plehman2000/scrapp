import ollama
def extract_info(text, facts):
    PROMPT = f"""

Given a set of factual statements from diverse sources, synthesize them into a single, concise insight that captures the key information and any underlying connections. Your task is to:

Analyze the provided statements for common themes or related concepts.
Identify the most crucial information from each statement.
Combine these elements into a coherent, unified insight.
Ensure the final insight is succinct yet comprehensive, ideally no longer than 1-2 sentences.
Maintain factual accuracy while avoiding redundancy.

Your synthesized insight should provide a clear, focused understanding of the collective information, highlighting any significant relationships or conclusions that can be drawn from the combined facts.
Facts: {facts}
"""


    response = ollama.chat(model='dolphin-llama3', messages=[ #llama3
    {
    'role': 'user',
    'content': PROMPT}])#, options={"temperature":.5}

    output = response['message']['content']

    return output