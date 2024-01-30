# %%
import json
import tqdm

import argparse

# %%
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text2text-generation", model="rymaju/KB13-t5-base-finetuned-en-to-regex", device_map="auto")

# %%
def t5_response(prompt, prompt_type):
    response = pipe(prompt["refined_prompt"] if prompt_type == 'refined' else prompt["raw_prompt"], num_return_sequences = 10, early_stopping=True, do_sample = True,
      temperature=0.8, max_length=128 )
    
    prompt['t5_output'] = response
    return prompt

# %%

parser = argparse.ArgumentParser(description='Phi1.5')
parser.add_argument('--prompt_type', type=str, default='raw', help='Enter prompt type: raw, refined. Default is raw.')
args = parser.parse_args()

prompt_type = args.prompt_type

print(prompt_type)

if prompt_type not in ['raw', 'refined']:
    raise ValueError('Invalid prompt type. Please enter raw or refined.')



# %%
with open('../DatasetCollection/RegexEval.json') as f:
    data = json.loads(f.read())

print(len(data))

# %%
new_data = []
for item in tqdm.tqdm(data):

    item = t5_response(item, prompt_type)
    new_data.append(item)


# %%
    
if prompt_type == 'refined':
    with open('./Output/T5_Refined_Output.json', 'w') as f:
        json.dump(new_data, f, indent=4)
else:
    with open('./Output/T5_Raw_Output.json', 'w') as f:
        json.dump(new_data, f, indent=4)


