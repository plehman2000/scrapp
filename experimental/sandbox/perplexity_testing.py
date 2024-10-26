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
 "Living Morally includes leading a non-harming and benevolent lifestyle",
"An aspect of moral training dedicates oneself to rigorous spiritual practice",
"An aspect of moral training dedicates oneself to rigorous spiritual practice nebloid!!",
"a well- Adjusted life does not necessarily equate to one filled with wealth and extravagance, but rather refers to a lifestyle that benefits both oneself and others without causing harm."
]

# res = asyncio.run(chatv(facts))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import math

def calculate_perplexity(text, model_name="FacebookAI/roberta-base"):
    # Load pre-trained model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name, is_decoder=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Encode the text
    encodings = tokenizer(text, return_tensors="pt")

    # Ensure the input_ids tensor is on the same device as the model
    input_ids = encodings.input_ids.to(model.device)

    # Calculate perplexity
    max_length = model.config.max_position_embeddings
    stride = 512

    nlls = []
    for i in range(0, input_ids.size(1), stride):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = min(i + stride, input_ids.size(1))
        trg_len = end_loc - i
        input_ids_chunk = input_ids[:, begin_loc:end_loc].to(model.device)
        target_ids = input_ids[:, i:end_loc].to(model.device)

        with torch.no_grad():
            outputs = model(input_ids_chunk, labels=target_ids)
            neg_log_likelihood = outputs.loss

        nlls.append(neg_log_likelihood * trg_len)

    ppl = torch.exp(torch.stack(nlls).sum() / end_loc)
    
    return ppl.item()


# for fact in facts:
#     perplexity = calculate_perplexity(fact)
#     print(fact)
#     print(f"{perplexity:.2e}")

# You can try with different models, for example:
# result = analyze_text(text, model_name="distilgpt2")
# result = analyze_text(text, model_name="gpt2-medium")


# Load model directly

from modules.ingest_docs import read_pdf



content = read_pdf(r'C:\GH\scrapp\sandbox\documents\nnpaper.pdf')
print(content)