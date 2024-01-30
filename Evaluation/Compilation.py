# %%
import re
import json
from timeout_decorator import timeout

# %%
names = ["Phi_Raw_Output", "Phi_Refined_Output","Text_DaVinci_Raw_Output","Text_DaVinci_Refined_Output","GPT3.5_Raw_Output","GPT3.5_Refined_Output", "T5_Raw_Output","T5_Refined_Output"]

for name in names:
    filename = f'../Generation/Output/{name}.json'
    outfilename = f'./{name}_Compiled_Result.json'

    # %%
    with open(filename, 'r') as f:
        data = json.load(f)
    len(data)

    # %%
    @timeout(60)
    def match_expression(expression, text):
        try:
            return re.search(expression, text) is not None
        except Exception as e:
            print(expression,": ", e)
            return None

    # %%
    compilation_result = []
    for item in data:
        print("Starting item: ", item['id'])
        id = item['id']
        matches = item['matches']
        non_matches = item['non_matches']
        # for completion in item['t5_output']:
        #     expression = completion['generated_text']

        expressions = []
        if 'Phi' in name:
            for i in range(len(item['phi_output'])):
                expressions.append(item['phi_output'][i]['text'])
        elif 'T5' in name:
            for completion in item['t5_output']:
                expressions.append(completion['generated_text'])
        elif 'Text_DaVinci' in name:
            for i in range(len(item['text_davinci_003_output']['choices'])):
                expressions.append(item['text_davinci_003_output']['choices'][i]['text'])
        elif 'GPT3.5' in name:
            for i in range(len(item['gpt3.5_output']['choices'])):
                expressions.append(item['gpt3.5_output']['choices'][i]['message']['content'])


        for expression in expressions:
            item['completion'] = expression
            is_valid = True
            for match in matches:
                for match in matches:
                    try:
                        is_match = match_expression(expression, match)
                    except TimeoutError:
                        print("TimeoutError: ", expression, match)
                        is_match = None
                    if is_match is None or is_match == False:
                        is_valid = False
                        break
            for non_match in non_matches:
                try:
                    is_match = match_expression(expression, non_match)
                except TimeoutError:
                    print("TimeoutError: ", expression, match)
                    is_match = None
                if is_match is None or is_match == True:
                    is_valid = False
                    break
            item['passed'] = is_valid
            compilation_result.append({
                'id': id,
                'completion': expression,
                'passed': is_valid
            })  
        print("Ending item: ", item['id'])

    # %%
    with open(f'./Output/{outfilename}', 'w') as f:
        json.dump(compilation_result, f, indent=4)


