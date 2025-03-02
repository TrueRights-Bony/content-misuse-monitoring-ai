import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def compare_texts(contract_text, social_media_text):
    """Compares contract text with social media content using ChatGPT"""
    prompt = f"""
    Compare the following two texts and determine if the social media content violates the contract terms.

    Contract Terms:
    {contract_text}

    Social Media Post:
    {social_media_text}

    Analysis:
    - Identify any clauses violated
    - Highlight key phrases from both texts that match or contradict
    - Provide a percentage similarity score

    Return the response in a structured JSON format.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response["choices"][0]["message"]["content"]
