import requests

def get_response(user_input):
    try:
        payload = {
            "model": "llama3.1",  # Change if using a different model
            "prompt": user_input,
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        output = response.json()
        return output.get("response", "No response received.")
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    print("Welcome to the Local LLaMA Chatbot! (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
            
        response = get_response(user_input)
        print(f"Bot: {response.strip()}")
        print("-" * 50)

if __name__ == "__main__":
    main()
