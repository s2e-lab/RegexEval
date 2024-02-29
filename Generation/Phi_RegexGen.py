# %%
import json
import tqdm

import argparse


# %%
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
# torch.set_default_device('cuda')

model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", trust_remote_code=True, torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5", trust_remote_code=True)
# tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5", trust_remote_code=True, torch_dtype="auto")


def make_clear(text):
    text = text.split('<|endoftext|>')[0]
    text = text.split('\n\n')[0].replace('\n','').strip()
    return text

# %%
def phi_response(prompt, tokenizer,model, prompt_type):
    current_prompt = prompt["refined_prompt"] if prompt_type == 'refined' else prompt["raw_prompt"]
    prompt_text = current_prompt + "Generate a RegEx for this description. \nAnswer:"
    inputs = tokenizer(prompt_text, return_tensors="pt")
    x = inputs['input_ids']
    x = x.expand(10, -1)
    generated_token = model.generate(
        x,
        temperature=0.8,
        max_length=128,
        do_sample=True,
    )
    prompt["phi_output"] =[]
    for i in range(10):
        prompt["phi_output"].append({})
        output = generated_token[i].cpu().squeeze()
        prompt["phi_output"][i]["text"] = make_clear(tokenizer.decode(output).split(prompt_text)[-1].split("\n\n")[0])

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

    item = phi_response(item, tokenizer,model, prompt_type)
    new_data.append(item)


# %%
    
if prompt_type == 'refined':
    with open('./Output/Phi_Refined_Output_Original.json', 'w') as f:
        json.dump(new_data, f, indent=4)

else:
    with open('./Output/Phi_Raw_Output_Original.json', 'w') as f:
        json.dump(new_data, f, indent=4)


