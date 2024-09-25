


from llm_funcs import get_llm_response, extract_info_json
import json


json_extraction_prompt = f"""
    You extract the premises from the following list of premises
    ### Template:
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
    Given the following premises and conclusion:
    {conclusion}\n
    {premises}
    Create a skeptical, reasonable opposition/inversion for each premise:
    """
    premises = get_llm_response(prompt)
    return premises

conclusion = "Jorbo Collins is the best person to vote for for the U.S. Presidential Race"
# premises = get_conclusion_premise(conclusion)
# inverted_premises = get_inversion(conclusion, premises)
# premises_json = extract_info_json(json_extraction_prompt+premises)
# inverted_premises_json = extract_info_json(json_extraction_prompt+inverted_premises)

# print(premises)
# print(inverted_premises)
# print("\n\nJSON\n")
# print(premises_json)
# print(inverted_premises_json)


from langchain_community.tools import DuckDuckGoSearchResults

tool = DuckDuckGoSearchResults()
results = tool.invoke("Obama")
print(results)