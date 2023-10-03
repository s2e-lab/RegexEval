# Re(gEx|DoS)Eval
This repository contains the source code for the paper: **Re(gEx|DoS)Eval: Evaluating Generated Regular Expressions and their Proneness to DoS AttackS**.

## Abstract
With the recent development of the large language model-based
text and code generation, users are utilizing them for a vast range
of tasks. RegEx generation is one of them. Despite the efforts of
generating RegEx from natural language, there is no prompt bench-
mark for LLMs with real-world data and robust test sets. In addition
to that RegEx can be prone to the Denial of Service (DoS) attack
because of the catastrophic backtracking. Hence, we need a prompt
dataset and a systemic evaluation process for the RegEx generated
by the language models. We proposed Re(gEx|DoS)Eval which includes a dataset with raw prompts from real users, refined prompts
with examples, and a robust set of tests. We introduced pass@k and
vulnerable@k metrics to evaluate the generated RegEx based on
the functional correctness and ReDoS vulnerability. In this short
paper, we demonstrated the Re(gEx|DoS)Eval with language models i.e., T5, Phi-1.5, and GPT-3, and described the plan for the future
extension of this infrastructure.

## Project Structure

This project contains four folders:
 - DatasetCollection
 - Generation
 - Evaluation
 - ReDoSEvaluation

In the following sections, we will describe the purpose of each folder and how to use them.

### DatasetCollection

1. Prerequesties(Tested on)
   - Python 3.9.4
   - selenium 4.11.2
   - beautifulsoup4 4.11.1
2. Run the Data_Collection.ipynb file to collect the data. Output: **RegexEval_Init.json**.
3. **RegexEval.json** contains the filtered data with the additional tests and will be used in the next steps.

### Generation
There are four python files for four models.
For GPT35.py and Text_DaVinci.py, you need to install the following packages:
- openai

You will also need a OpenAI API key and have to create a **config.json** file as the **example.json** file. Update your API key in the **config.json** file.

For T5_RegexGen.py and Phi_RegexGen.py, you need to install the following packages:
- transformers 
- torch
- tqdm

You have to run the each code twice: once for raw and once for refined prompts. These codes will generate {Model_name}_{Prompt_type}_Output.json files except for the Phi_RegexGen.py which will generate {Model_name}_{Prompt_type}_Output_Original.json files. You have to run Phi_data_filter.ipynb on them.

### Evaluation
You need to install the following packages:
- subprocess
- timeout_decorator
- collections

**Compilation.ipynb** will compile the Regexes and tests with the corresponding tests. It will generate {Model_name}_{Prompt_type}_Output_Compiled_Result.json. Then, you can run **Pass_at_k_Evaluation.ipynb** to get the pass@k score.

**DFA_Equ_Evaluation.ipynb** will use regex_dfa_equals.jar to find out the DFA match and calculate the DFA-EQ@k score.


**EM_Evaluation.ipynb** will calculate the Exact match ratio.

**Notes**:
You need to change the code depends on the model to get the generated regex.

For T5:
```
for i in range(len(item['t5_output'])):
    predicted_expression = item['t5_output'][i]['generated_text']
```

For Phi:
```
for i in range(len(item['phi_output'])):
    expression = item['phi_output'][i]['text']
```

For GPT-3.5:
```
for i in range(len(item['gpt3.5_output']['choices])):
    expression = item['gpt3.5_output']['choices][i]['message']['content']
```


For Text DaVinci:
```
for i in range(len(item['text_davinci_003_output']['choices])):
    expression = item['text_davinci_003_output']['choices][i]['text']
```

### ReDoSEvaluation
**ReDoS_Dataset_Creation.ipynb** will create text files and every text file will contain all the generated regex line by line. It will be the input for [ReDoSHunter](https://github.com/yetingli/ReDoSHunter) and [ReScue](https://github.com/2bdenny/ReScue). Check the corresponding link about running it.

**ReDoSHunter_Result_Analysis.ipynb** and **ReScure_Result_Analysis.ipynb** will create the ReDoS vulnerability@k score for each model.