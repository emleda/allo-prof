from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_KEY')) #api key stored in environment variable for security

def save_profile(user_id, profile):
    user_dir = f"profiles/{user_id}"
    os.makedirs(user_dir, exist_ok=True)
    profile_path = f"{user_dir}/{user_id}.json"
    with open(profile_path, 'w') as f:
        json.dump(profile, f)

def create_profile():
    '''Takes initial details: 
    target language, level, username.
    Creates profile.'''

    print("Pleased to meet you! What language are you learning?")
    profile = {}
    profile['language'] = input()
    print("What level are you?")
    profile['level'] = input()
    print("Now create a username")
    user_id = input().strip()
    profile['grammar'] = []
    profile['vocab'] = []

    save_profile(user_id, profile)

    return profile, user_id

def introduction():
    ''' Initialises conversation, loading or creating new profile.
    '''
    user_connected = False

    while user_connected == False:
        print("Hello, have you chatted with me before? If you have, reply with your username, if not, reply 'No'.")
        user_id = input().strip()

        if user_id.lower() == "no":
            profile, user_id = create_profile()
            user_connected = True

        else:
            try:
                with open(f"profiles/{user_id}/{user_id}.json") as f:
                    profile = json.load(f)
                user_connected = True
            except FileNotFoundError:
                print("We do not have any records, please try again.")
    
    return profile, user_id

def summarise_session(profile, conversation, user_id):
    prompt = f"""You are a {profile['level']} level {profile['language']} tutor.
    From our conversation, extract the following from the user
    1. Mistakes (with corrections). Ignore trivial spelling or capitalisation errors.
    2. Vocabulary that may be unfamiliar,  this can be words you introduce in the conversation.
    Respond in JSON. Vocabulary should have key 'vocab' and return a list of new words. 
    Grammar should be a list of dictionaries with key 'grammar', each dictionary entry represents a mistake with keys 'mistake' and 'correction'.
    """

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(conversation)}
        ],
        temperature=0.0
    )

    reply = resp.choices[0].message.content
    print(reply)

    try:
        summary_data = json.loads(reply)
    except json.JSONDecodeError:
        summary_data = {"grammar": [], "vocab": []}

    profile["grammar"].extend(summary_data.get("grammar", []))
    profile["vocab"].extend(summary_data.get("vocab", []))

    save_profile(user_id, profile)

    try:
        with open("profiles/{user_id}/session_history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    history.append({"conversation": conversation, "summary": summary_data})
    with open(f"profiles/{user_id}/session_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print("\n--- Session Summary ---")
    print("Mistakes:")
    for m in summary_data.get("grammar", []):
        print("-", m)
    print("Vocabulary:")
    for v in summary_data.get("vocab", []):
        print("-", v)

def tutor_chat(profile, user_id):
    ''' Chat with tutor. 
    profile (dict): Characteristics of user, 
    '''
    conversation = []
    grammar_context = "\n".join(f"- {item}" for item in profile.get("grammar", []))
    vocab_context = "\n".join(f"- {item}" for item in profile.get("vocab", []))

    while True:
        #student input
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        conversation.append({"role": "user", "content": user_input})

        system_prompt = f"""You are a {profile['language']} tutor. 
        Your student says they have {profile['level']} level, but you also know the mistakes they've made and vocabulary they've learned in this conversation and in previous ones.
        Adjust your language the student's actual level, but try to challenge them with words they may not know.
        """
        assistant_prompt = f"""FYI, here are the student's past mistakes and learned vocabulary:
                                    "Grammar mistakes:\n{grammar_context or 'None'}
                                    Vocabulary learned:\n{vocab_context or 'None'}"""

        #llm response
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt},
            {"role": "assistant", "content": assistant_prompt}] 
            + conversation
        )

        reply = resp.choices[0].message.content
        print("Tutor:", reply)

        conversation.append({"role": "assistant", "content": reply})

    summarise_session(profile, conversation, user_id)

if __name__ == "__main__":
    profile, user_id = introduction()
    tutor_chat(profile, user_id)