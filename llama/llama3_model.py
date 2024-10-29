from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")

tokenizer.pad_token = tokenizer.eos_token

def generate_response(user_message):
    inputs = tokenizer(user_message, return_tensors="pt", padding=True, truncation=True)

    outputs = model.generate(
        **inputs,
        max_length=150,
        pad_token_id=tokenizer.pad_token_id
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
