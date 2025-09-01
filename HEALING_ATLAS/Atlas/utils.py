import requests
from django.conf import settings



def analyze_sentiment(entry_text):
    api_url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    payload = {"inputs": entry_text}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        result = response.json()

        # Defensive check for expected structure
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list) and len(result[0]) > 0:
            sentiment = result[0][0].get('label', 'unknown')
            score = result[0][0].get('score', 0.0)
        else:
            print("Unexpected response format:", result)
            sentiment = 'unknown'
            score = 0.0

    except Exception as e:
        print("Sentiment analysis error:", e)
        sentiment = 'error'
        score = 0.0

    return {"sentiment": sentiment, "score": score}


def suggest_tone(text):
    soft_keywords = ['gentle', 'soothing', 'calm', 'healing', 'affirming']
    alert_keywords = ['trigger', 'urgent', 'warning', 'crisis', 'unsafe']

    text_lower = text.lower()
    if any(word in text_lower for word in alert_keywords):
        return 'alert'
    elif any(word in text_lower for word in soft_keywords):
        return 'soft'
    else:
        return 'neutral'
