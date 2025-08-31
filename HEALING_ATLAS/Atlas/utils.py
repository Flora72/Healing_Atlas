import requests

def analyze_sentiment(entry_text):
    api_url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    headers = {"Authorization": f"Bearer YOUR_HUGGINGFACE_API_KEY"}
    payload = {"inputs": entry_text}

    response = requests.post(api_url, headers=headers, json=payload)
    result = response.json()

    sentiment = result[0][0]['label']
    score = result[0][0]['score']
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
