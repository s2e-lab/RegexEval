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
def parse_rescue(text):
    # Split the text into sections using "id:" as a delimiter

    sections = text.split('\n')
    
    # Initialize a list to store the parsed data
    parsed_data = []
    
    # Iterate through each section (excluding the first empty section)
    for section in sections:
        # Initialize a dictionary to store the parsed information for this section
        section_data = {}

        current_data = section.split(':')

        
        # Extract the ID
        if "failed" in current_data[0]:
            section_data['id'] = (int(current_data[0].strip().split(" ")[0])-1)//10
        else:
            section_data['id'] = (int(current_data[0].strip())-1)//10
        
        if "failed" in current_data[0]:
            section_data['status1'] = False
        else:

            # Extract the status 1
            section_data['status1'] = current_data[1].strip()
            
            if section_data['status1'] == "success":
                section_data['status1'] = True
            else:
                section_data['status1'] = False
        
        # Append the parsed data for this section to the list
        parsed_data.append(section_data)
    
    return parsed_data

# %%
names = ["Phi_Raw_Output","Phi_Refined_Output","Text_DaVinci_Raw_Output","Text_DaVinci_Refined_Output","GPT3.5_Raw_Output","GPT3.5_Refined_Output", "T5_Raw_Output","T5_Refined_Output"]
# names = ["Phi_Raw_Output","Phi_Refined_Output"]
for name in names:
    print(name)
    outfilename = f'./ReScue_Results/{name}_full_result.txt'

    with open(outfilename, 'r') as f:
        result = f.read()
    rescue_data = parse_rescue(result)
    # print(rescue_data[0])


    results = defaultdict(list)

    for r in rescue_data:
        results[r['id']].append(r)
    

    # Calculate pass@k.
    total, correct = [], []
    for result in results.values():
            passed = [r["status1"] for r in result]
            # print(passed)
            total.append(len(passed))
            correct.append(sum(passed))
    total = np.array(total)
    correct = np.array(correct)

    ks = [1,5,10]
    vul_at_k = {f"pass@{k}": (estimate_vul_at_k(total, correct, k).mean())*100
                        for k in ks if (total >= k).all()}
    print(vul_at_k)


