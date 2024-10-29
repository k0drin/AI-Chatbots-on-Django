from transformers import AutoModelForCausalLM, AutoTokenizer
from textblob import TextBlob


tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")

tokenizer.pad_token = tokenizer.eos_token


def analyze_sentiment(user_message):
    """Analyze sentiment of the user's message using TextBlob."""
    analysis = TextBlob(user_message)
    if analysis.sentiment.polarity > 0.1:
        return 'positive'
    elif analysis.sentiment.polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'


def generate_response(user_message):
    sentiment = analyze_sentiment(user_message)

    primed_message = f"User: {user_message}\nAssistant:"
    inputs = tokenizer(primed_message, return_tensors="pt", padding=True, truncation=True)

    outputs = model.generate(
        **inputs,
        max_length=50,
        num_return_sequences=1,
        pad_token_id=tokenizer.pad_token_id,
        temperature=0.5,
        top_p=0.9,
        repetition_penalty=1.2,
        no_repeat_ngram_size=2
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.split("Assistant:")[-1].strip()

    if sentiment == 'positive':
        response += " 😊"
    elif sentiment == 'negative':
        response += " 😔"
    else:
        response += " 🙂"

    return response
