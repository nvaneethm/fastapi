# core/gpt_service.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from app.config import MODEL_NAME, DEVICE
from app.core.load_data import load_jira_tickets

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(DEVICE)

# Load Jira tickets once
jira_tickets = load_jira_tickets()

def create_context(user_query: str) -> str:
    # Build the context using the loaded Jira tickets
    context = "Here is the current list of Jira tickets:\n"
    for ticket in jira_tickets:
        context += f"ID: {ticket.id}, Summary: {ticket.summary}, Description: {ticket.description}, Status: {ticket.status}\n"
    context += f"\nUser Query: {user_query}\nA:"
    return context

def generate_response(user_query: str) -> str:
    context = create_context(user_query)

    # Ensure the pad token is set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Tokenize input
    inputs = tokenizer(context, return_tensors="pt", padding=True, truncation=True).to(DEVICE)

    # Generate response
    # with torch.autocast("mps"):
    #     outputs = model.generate(
    #         input_ids=inputs['input_ids'],
    #         attention_mask=inputs['attention_mask'],
    #         max_length=150,
    #         pad_token_id=tokenizer.eos_token_id,
    #         no_repeat_ngram_size=3,
    #         num_beams=3
    #     )

    try:
        outputs = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=150,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            num_beams=3
        )
    except Exception as e:
        print("Error during model generation:", e)


    # Decode output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

    # Remove any unwanted text beyond the answer
    stop_sequence = "\nA:"
    if stop_sequence in generated_text:
        generated_text = generated_text.split(stop_sequence)[0]

    return generated_text
