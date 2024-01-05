# %%
import json
from typing import List, Union
import itertools

import numpy as np
from collections import defaultdict


# %%
def estimate_vul_at_k(
    num_samples: Union[int, List[int], np.ndarray],
    num_correct: Union[List[int], np.ndarray],
    k: int
) -> np.ndarray:
    """
    Estimates vul@k of each problem and returns them in an array.
    """

    def estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).
        """
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array([estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)])


# %%
def parse_rescue(text, offset=0):
    # Split the text into sections using "id:" as a delimiter

    sections = text.split('-------------------------')
    
    # Initialize a list to store the parsed data
    parsed_data = []
    
    # Iterate through each section (excluding the first empty section)
    for section in sections:
        # Initialize a dictionary to store the parsed information for this section
        section_data = {}
        
        current_data = section.split('\n')
        # print(current_data)
        if current_data[0] == '':
            current_data = current_data[1:]
        
        if len(current_data) < 3:
            continue
        
        
        # Extract the ID
        section_data['id'] = (offset + int(current_data[0].split(":")[-1].strip())-1)//10

        # Extract the status 1
        section_data['pattern'] = current_data[1].strip()
        
        # Extract the status 1
        section_data['status'] = current_data[2].strip()
        
        if section_data['status'] == "RESULT-TRUE":
            section_data['status'] = True
        else:
            section_data['status'] = False
        

        # Append the parsed data for this section to the list
        parsed_data.append(section_data)
    
    return parsed_data

# %%
names = ["Phi_Raw_Output","Phi_Refined_Output","Text_DaVinci_Refined_Output","GPT3.5_Raw_Output","GPT3.5_Refined_Output", "T5_Raw_Output","T5_Refined_Output"]
for name in names:
    print(name)
    outfilename = f'./ReDoSHunter_Results/{name}_full_result.txt'

    with open(outfilename, 'r') as f:
        result = f.read()
    redoshunter_data = parse_rescue(result)

    # print(rescue_data[0])


    results = defaultdict(list)

    for r in redoshunter_data:
        results[r['id']].append(r)
    

    # Calculate pass@k.
    total, correct = [], []
    for result in results.values():
            passed = [r["status"] for r in result]
            # print(passed)
            total.append(len(passed))
            correct.append(sum(passed))
    total = np.array(total)
    correct = np.array(correct)

    ks = [1,3,10]
    pass_at_k = {f"pass@{k}": (estimate_vul_at_k(total, correct, k).mean())*100
                        for k in ks if (total >= k).all()}
    print(pass_at_k)