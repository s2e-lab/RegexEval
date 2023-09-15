# %%
import json
import openai


# %%
with open("./config.json") as f:
    config_data = json.loads(f.read())

OPENAI_KEY = config_data['OPENAI_KEY']
openai.api_key = OPENAI_KEY
print(OPENAI_KEY)

    


# %%
def gpt35_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt["refined_prompt"]
                    + "\nGenerate a RegEx for this description:\n\n",
                }
            ],
            temperature=0.8,
            max_tokens=128,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=10,
        )
        prompt['gpt3.5_output'] = response
        print(response)
        return prompt
    except Exception as e:
        print(e)
        prompt['gpt3.5_output'] = e
        return prompt



# %%
with open('./DatasetCollection/RegexEval.json') as f:
    data = json.loads(f.read())

len(data)

# %%
new_data = []
for item in data:
    item = gpt35_response(item)
    new_data.append(item)
    break


# %%
with open('./GPT3.5_Refined_Output.json', "w") as f:
   json.dump(new_data, f, indent=4)
