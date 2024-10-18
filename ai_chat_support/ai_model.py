from transformers import pipeline

# Load pre-trained GPT model
chatbot_pipeline = pipeline("text-generation", model="gpt2")

def get_ai_response(question):
    result = chatbot_pipeline(question, max_length=50, num_return_sequences=1)
    return result[0]['generated_text']
