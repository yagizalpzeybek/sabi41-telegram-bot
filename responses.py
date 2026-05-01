import random
from memory import load_memory, save_memory

user_memory = load_memory()



def handle_response(text: str, user_id: int) -> str:
    processed = text.lower().strip()
    user_id = str(user_id)

    if processed.startswith("my name is"):
        name =  text[11:].strip()
        user_memory[user_id] = name
        save_memory(user_memory)
        return f"Nice to meet you, {name}!"
    
    if "what is my name" in processed:
        if user_id in user_memory:
            return f"Your name is {user_memory[user_id]}."
        return "I don't know your name yet."
    

    if any(word in processed for word in ["hello", "hi", "hey"]):
        return "Hey there!"

    if "how are you" in processed:
        return "I am good! How about you?"
    
    if any(word in processed for word in ["i am good", "i'm fine", "great"]):
        return "Awesome!"

    if "i love python" in processed:
        return "Python is awesome!"
    
    if "ela yagizin neyi?" in processed:
        return "Biricik prensesi"
    

    return "I do not understand what you wrote..."