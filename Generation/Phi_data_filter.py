# %%
import json

for prompt_type in ['Raw', 'Refined']:

    # %%
    with open(f"./Output/Phi_{prompt_type}_Output_Original.json") as f:
        data = json.loads(f.read())

    print(len(data))

    # %%
    def make_clear(text):
        text = text.split('<|endoftext|>')[0]
        text = text.split('\n\n')[0].replace('\n','').strip()
        return text

    # %%
    new_data = []
    for item in data:

        for i in range(len(item['phi_output'])):
            text = item['phi_output'][i]['text']
            item['phi_output'][i]['text']  = make_clear(str(text))
        new_data.append(item)

    # %%
    with open(f"./Output/Phi_{prompt_type}_Output.json", "w") as f:
        json.dump(new_data, f, indent=4)


