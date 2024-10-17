import ollama
import json




def get_llm_response(prompt):
    response = ollama.chat(model='dolphin-llama3', messages=[ #llama3
    {
    'role': 'user',
    'content': prompt}], options={'json':True})#, options={"temperature":.5}
    output = response['message']['content']
    return output

def reword_query(naive_claim):
    #reword logic
    query = get_llm_response(
        f""" Write a search query to find sources that support the following claim, by rewording the following claim into a question:{naive_claim}                             
        """
                             )
    return query

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
    response = ollama.generate(model='nuextract', prompt= prompt_with_schema)['response']
    output = response[response.find("<|end-output|>")+len("<|end-output|>"):]
    print("output")
    print("========================")
    print(output)
    print("========================")

    try:
        return json.loads(output)
    # except json.JSONDecodeError:
    #     print(output)
    #     try:
    #         response = ollama.chat(model='dolphin-llama3', messages=[ #llama3
    #         {
    #         'role': 'user',
    #         'content': prompt_with_schema}])

    #         output = response['message']['content']
            # output = output.replace("<|end-output|>","")

    #         return json.loads(output)
    except json.JSONDecodeError:
        return {"error": "Error in JSON output"}
