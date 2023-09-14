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
def openai_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt["refined_prompt"]
        + "\nGenerate a RegEx for this description:\n\n",
        temperature=0.8,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=10,
    )
    print(response)
    prompt['text_davinci_003_output'] = response
    return prompt
    


# %%
with open('../DatasetCollection/RegexEval.json') as f:
    data = json.loads(f.read())

len(data)

# %%
new_data = []
for item in data:
    item = openai_response(item)
    new_data.append(item)
    break


# %%
with open("./Text_DaVinci_Output.json", "w") as f:
    json.dump(new_data, f, indent=4)


