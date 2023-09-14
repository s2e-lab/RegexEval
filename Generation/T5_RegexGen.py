# %%
import json
import tqdm

# %%
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text2text-generation", model="rymaju/KB13-t5-base-finetuned-en-to-regex", device_map="auto")

# %%
def t5_response(prompt):
    response = pipe(prompt["refined_prompt"], num_return_sequences = 10, early_stopping=True, do_sample = True,
      temperature=0.8, max_length=128 )
    
    prompt['t5_output'] = response
    return prompt



# %%
with open('../DatasetCollection/RegexEval.json') as f:
    data = json.loads(f.read())

len(data)

# %%
new_data = []
for item in tqdm.tqdm(data):

    item = t5_response(item)
    new_data.append(item)


# %%
with open('./T5_Refined_Output.json', 'w') as f:
    json.dump(new_data, f, indent=4)


