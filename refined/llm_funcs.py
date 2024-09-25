import ollama
import json




def get_llm_response(prompt):
    response = ollama.chat(model='dolphin-llama3', messages=[ #llama3
    {
    'role': 'user',
    'content': prompt}])#, options={"temperature":.5}
    output = response['message']['content']
    return output



################################################################################################################
#? EXAMPLE for extract_info_json()
################################################################################################################

#     input_llm = f"""
#     You extract the title from the first part of this chunk, ignoring the author names afterward### Template:
#     {json.dumps(json.loads(schema), indent=4)}
#     ### Example:
#     {{"title": "Amazing new discovery"}}
#     ### Text:
#     {text}
# """
################################################################################################################

def extract_info_json(prompt_with_schema):
    response = ollama.chat(model='nuextract', messages=[ #llama3
    {
    'role': 'user',
    'content': prompt_with_schema}])

    output = response['message']['content']
    
    return output.replace("<|end-output|>","")

