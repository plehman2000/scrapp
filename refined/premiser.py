


from llm_funcs import get_llm_response, extract_info_json
import json


json_extraction_prompt = f"""
    You extract the title from the first part of this chunk, ignoring the author names afterward### Template:
    {{"premises":["statement"]}}

    ### Text:\n"""
def get_conclusion_premise(conclusion):
    prompt = f"""
    Give 3-5 premises that must be true for the following conclusion to hold:
    {conclusion}
    """
    premises = get_llm_response(prompt)
    return premises

def get_inversion(conclusion, premises):
    prompt = f"""
    Given the following premises that must be true for the following conclusion to hold:
    {conclusion}\n
    {premises}
    Create a skeptical, reasonable inversion for each premise:
    """
    premises = get_llm_response(prompt)
    return premises

conclusion = "Kamala Harris is the best person to vote for for the U.S. Presidential Race"
premises = get_conclusion_premise(conclusion)
inverted_premises = get_inversion(conclusion, premises)
premises_json = extract_info_json(json_extraction_prompt+premises)
inverted_premises_json = extract_info_json(json_extraction_prompt+inverted_premises)

print(premises)
print(inverted_premises)
print(premises_json)
print(inverted_premises_json)