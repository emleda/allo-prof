from openai import OpenAI
import json

client = OpenAI(api_key="") #add your own api key here

#introduction
user_connected = False

while user_connected == False:
    print("Hello, have you chatted with me before? If you have, reply with your username, if not, reply 'No'.")
    user_id = input()

    if user_id == "No":
        #create profile
        print("Pleased to meet you! What language are you learning?")
        profile = {}
        profile['language'] = input()
        print("What level are you?")
        profile['level'] = input()
        print("Now create a username")
        user_id = input().strip()

        #save profile
        with open(f'profiles/{user_id}.json', 'w') as f:
            json.dump(profile, f)
        
        #bool flag
        user_connected = True

    else:
        try:
            with open(f"profiles/{user_id}.json") as f:
                profile = json.load(f)
            user_connected = True
        except FileNotFoundError:
            print("We do not have any records, please try again.")

#chat!
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", exit]:
        break

    prompt = f"You are a {profile['level']} level {profile.get('language', 'French')} tutor. Adjust your language to match my level. After you speak, briefly note any mistakes (not only spelling, grammar, but inappropriate word usage too) made in my message, along with their corrections."

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": user_input}]
    )

    print("Tutor:", resp.choices[0].message.content)