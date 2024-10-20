import ollama
import json




def get_llm_response(prompt):
    response = ollama.chat(model='dolphin-llama3', messages=[ #llama3
    {
    'role': 'user',
    'content': prompt}], options={'json':True})#, options={"temperature":.5}
    output = response['message']['content']
    return output


def get_llm_json_response(prompt):
    response = ollama.chat(model='dolphin-llama3', messages=[ #llama3
    {
    'role': 'user',
    'content': f"Return only JSON.{prompt}"}], options={'json':True})#, options={"temperature":.5}
    output = response['message']['content']
    return output

def determine_informative(chunk, claim):
    json_res = get_llm_json_response(f'Determine if the following statement is useful in supporting the claim "{claim}". Return (as a JSON, {{"response":"true"}}) "true" or "false". Statement: {chunk}')
    try:
        return dict(json.loads(json_res))
    except Exception:
        return {"error": "Error in JSON output"}
    

def reword_query(naive_claim):
    #reword logic
    query = get_llm_response(
        f""" Write a search query to find sources that support the following claim, by rewording the following claim into a question:{naive_claim}                             
        """
                             )
    return query


def combine_claims(claim, chunk1, chunk2):
    #reword logic
    query = get_llm_response(
        f""" Given a claim and related statements, synthesize the statements' main ideas into a single-sentence summary.
            Input:
            Claim: {claim}
            Statements:
            Statement 1: {chunk1}
            Statement 2: {chunk2}
            ...

            Instructions:
            Analyze the claim and statements.
            Synthesize into one clear sentence.
            ONLY RETURN a one-sentence summary encompassing the main points from the claim and statements."""
                             )
    return query


def restate_claim(claim, chunk):
    #reword logic
    query = get_llm_response(
        f""" Given a claim and related statement, synthesize the statement's main ideas into a single-sentence summary.
            Input:
            Claim: {claim}
            Statement:
            {chunk}
            ...

            Instructions:
            Analyze the claim and statements.
            Synthesize into one clear sentence.
            ONLY RETURN a one-sentence summary encompassing the main points from the claim and statement."""
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
