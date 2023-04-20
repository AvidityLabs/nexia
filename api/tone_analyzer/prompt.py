import json
from api.utilities.openai import create_completion

def get_prompt(text):
    return f"Please analyze the following text and provide the following metrics in percentage form:\n"\
            "- Sentiment\n"\
            "- Emotion (Anger, Fear, Joy, Sadness)\n"\
            "- Subjectivity\n"\
            "- Language style (Formality)\n"\
            "- Readability\n"\
            "- Intent\n"\
            "- Personality\n"\
            "Text: {text}\n"\
            "---"


def analyze_text(text):
    response = create_completion("text-davinci-002", text, 1024, 0.5, 0, 1,0,0,None)

    result = response.choices[0].text.strip()

    # Parse the JSON data returned by OpenAI
    data = json.loads(result)

    # Extract the analysis results from the JSON data
    analysis = {
        "sentiment": data["data"][0]["value"],
        "emotion": {
            "anger": data["data"][1]["value"],
            "fear": data["data"][2]["value"],
            "joy": data["data"][3]["value"],
            "sadness": data["data"][4]["value"]
        },
        "subjectivity": data["data"][5]["value"],
        "language_style": data["data"][6]["value"],
        "readability": data["data"][7]["value"],
        "intent": data["data"][8]["value"],
        "personality": data["data"][9]["value"]
    }

    return analysis
