import ollama
def extract_info(facts):
    PROMPT = f"""

Given a set of factual statements from diverse sources, synthesize them into a single, concise insight that captures any underlying connections. Your task is to:

Analyze the provided statements for common themes or related concepts.
Identify the most crucial information from each statement.
Combine these elements into a coherent, unified insight.
Ensure the final insight is succinct yet comprehensive, no longer than 1 sentence.
Maintain factual accuracy while avoiding redundancy.

Your synthesized insight should provide a clear, focused understanding of the collective information, highlighting
 any significant relationships or conclusions that can be drawn from the combined facts.Only return the insight, in the form of a sentence
Facts: {facts}
"""


    response = ollama.chat(model='dolphin-llama3', messages=[ #llama3
    {
    'role': 'user',
    'content': PROMPT}])#, options={"temperature":.5}

    output = response['message']['content']

    return output












async def chatv(facts):

    PROMPT = f"""
    Given a set of factual statements from diverse sources, synthesize them into a single, concise insight that captures any underlying connections. Your task is to:

    Analyze the provided statements for common themes or related concepts.
    Identify the most crucial information from each statement.
    Combine these elements into a coherent, unified insight.
    Ensure the final insight is succinct yet comprehensive, no longer than 1 sentence.
    Maintain factual accuracy while avoiding redundancy.

    Your synthesized insight should provide a clear, focused understanding of the collective information, highlighting
    any significant relationships or conclusions that can be drawn from the combined facts.Only return the insight, in the form of a sentence
    Facts: {facts}
    """


    # response = ollama.chat(model='dolphin-llama3', messages=[ #llama3
    # {
    # 'role': 'user',
    # 'content': PROMPT}])#, options={"temperature":.5}
  

    msg = ""
    async for part in await AsyncClient().chat(model='dolphin-llama3', messages=[ {'role': 'user','content': PROMPT}], stream=True):
        print(part['message']['content'], end='', flush=True)
        msg +=part['message']['content']

    return msg





import asyncio
from ollama import AsyncClient


import math
facts = [
 "Living Morally includes leading a non-harming and benevolent lifestyle"
"An aspect of moral training dedicates oneself to rigorous spiritual practice"
"a well- Adjusted life does not necessarily equate to one filled with wealth and extravagance, but rather refers to a lifestyle that benefits both oneself and others without causing harm."
]

res = asyncio.run(chatv(facts))


# def calc_number_calls(num_facts, facts_per_call):
#     facts_left = num_facts
#     calls = 0
#     while facts_left > 1:
#         n = math.ceil(facts_left/facts_per_call)
#         calls += n
#         facts_left = facts_left // facts_per_call
#     print((calls*5)//60)


# calc_number_calls(10000,3)
