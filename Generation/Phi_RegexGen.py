# %%
import json
import tqdm

# %%
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
torch.set_default_device('cuda')

model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", trust_remote_code=True, torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5", trust_remote_code=True, torch_dtype="auto")


# %%
def phi_response(prompt, tokenizer,model):
    prompt_text = prompt["refined_prompt"]+ "Generate a RegEx for this description. \nAnswer:"
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
        prompt["phi_output"][i]["text"] = tokenizer.decode(output).split(prompt_text)[-1].split("\n\n")[0]

    return prompt


# %%
with open('../DatasetCollection/RegexEval.json') as f:
    data = json.loads(f.read())

len(data)

# %%
new_data = []
for item in tqdm.tqdm(data):

    item = phi_response(item, tokenizer,model)
    print(item)
    new_data.append(item)


# %%
with open('./Phi_Refined_Output_Original.json', 'w') as f:
    json.dump(new_data, f, indent=4)


