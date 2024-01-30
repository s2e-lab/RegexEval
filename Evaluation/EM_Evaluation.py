# %%
import json

# %%
names = ["Phi_Raw_Output","Phi_Refined_Output","Text_DaVinci_Raw_Output","Text_DaVinci_Refined_Output","GPT3.5_Raw_Output","GPT3.5_Refined_Output", "T5_Raw_Output","T5_Refined_Output"]
for name in names:
    print(name)
    filename = f'../Generation/Output/{name}.json'
    with open(filename) as f:
        data = json.load(f)
    count_matches =0
    for item in data:
        ground_truth = item["expression"]
        predicted_expressions = []
        if 'Phi' in name:
            for i in range(len(item['phi_output'])):
                predicted_expressions.append(item['phi_output'][i]['text'])
        elif 'T5' in name:
            for completion in item['t5_output']:
                predicted_expressions.append(completion['generated_text'])
        elif 'Text_DaVinci' in name:
            for i in range(len(item['text_davinci_003_output']['choices'])):
                predicted_expressions.append(item['text_davinci_003_output']['choices'][i]['text'])
        elif 'GPT3.5' in name:
            for i in range(len(item['gpt3.5_output']['choices'])):
                predicted_expressions.append(item['gpt3.5_output']['choices'][i]['message']['content'])

        for predicted_expression in predicted_expressions:
            if predicted_expression == ground_truth:
                count_matches +=1

    print((count_matches/len(data))*100)

# %%



