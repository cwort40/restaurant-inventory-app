import openai
import os

openai.api_key = os.environ.get('OPENAI_KEY')


def fetch_density(ingredient_name):
    # Define your prompt here. Modify as necessary.
    prompt = f"What is the density of {ingredient_name}? Only answer with just a number with two decimal places e.g. " \
             f"0.75"

    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=50)
    answer = response.choices[0].text.strip()

    # Parse the answer to extract the density value.
    # NOTE: This will require further refinement based on the type of responses you receive.
    try:
        density_value = float(answer.split()[0])
        return density_value
    except:
        return None
