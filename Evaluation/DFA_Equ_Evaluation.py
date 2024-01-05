# %%
import subprocess
import json
from collections import defaultdict

# %%
def regex_equiv(gold, predicted):
    if gold == predicted:
        return True
    try:
        out = subprocess.check_output(['java', '-jar', 'regex_dfa_equals.jar', '{}'.format(gold), '{}'.format(predicted)])
#          print("out: {}".format(out))
        #print(out.decode('utf-8'))
        if '\n1' in out.decode('utf-8'):
            return True
        else:
            return False
    except Exception as e:
        return False


# %%

names = ["Phi_Raw_Output","Phi_Refined_Output","Text_DaVinci_Raw_Output","Text_DaVinci_Refined_Output","GPT3.5_Raw_Output","GPT3.5_Refined_Output", "T5_Raw_Output","T5_Refined_Output"]
for name in names:
    print("Starting: ", name)
    filename = f'../Generation/Output/{name}.json'
    outfilename = f'./Output/{name}_DFA_Result.json'

    with open(filename, 'r') as f:
        data = json.load(f)
    print(len(data))

    dfa_result = []
    for item in data:
        print("Starting item: ", item['id'])
        id = item['id']
        gold_expression = item['expression']
        # print ("Expression: ", gold_expression)

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
            item['completion'] = predicted_expression
            passed = regex_equiv(gold_expression, predicted_expression)
            
            dfa_result.append({
                'id': id,
                'completion': predicted_expression,
                'passed': passed
            })  
        print("Ending item: ", item['id'])

    with open(outfilename, 'w') as f:
        json.dump(dfa_result, f, indent=4)

# %%
def dfa_at_k(results, ks):
    total = len(results)
    for k in ks:
        correct = 0
        for result in results.values():
            passed = [r["passed"] for r in result[:k]]
            correct += (1 if sum(passed)!=0 else 0)
        print(f"DFA-EQ@{k}: {(correct/total)*100}")

        

    

# %%
names = ["Phi_Raw_Output","Phi_Refined_Output","Text_DaVinci_Raw_Output","Text_DaVinci_Refined_Output","GPT3.5_Raw_Output","GPT3.5_Refined_Output", "T5_Raw_Output","T5_Refined_Output"]
matrix = "DFA"
for name in names:
    print(name)
    filename = f'../Generation/Output/{name}.json'
    outfilename = f'./Output/{name}_{matrix}_Result.json'

    with open(outfilename, 'r') as f:
        result = json.load(f)

    results = defaultdict(list)


    for r in result:
        results[r['id']].append(r)

    dfa_at_k(results, [1,3,10])




