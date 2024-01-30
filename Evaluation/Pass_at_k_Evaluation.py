# %%
import json
from typing import List, Union
import itertools

import numpy as np
from collections import defaultdict


# %%
def estimate_pass_at_k(
    num_samples: Union[int, List[int], np.ndarray],
    num_correct: Union[List[int], np.ndarray],
    k: int
) -> np.ndarray:
    """
    Estimates pass@k of each problem and returns them in an array.
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
names = ["Phi_Raw_Output","Phi_Refined_Output","Text_DaVinci_Raw_Output","Text_DaVinci_Refined_Output","GPT3.5_Raw_Output","GPT3.5_Refined_Output", "T5_Raw_Output","T5_Refined_Output"]


matrix = "Compiled"
for name in names:
    filename = f'../Generation/Output/{name}.json'
    outfilename = f'./Output/{name}_{matrix}_Result.json'

    with open(outfilename, 'r') as f:
        result = json.load(f)

    results = defaultdict(list)

    for r in result:
        results[r['id']].append(r)

    # Calculate pass@k.
    total, correct = [], []
    for result in results.values():
        passed = [r["passed"] for r in result]
        total.append(len(passed))
        correct.append(sum(passed))
    total = np.array(total)
    correct = np.array(correct)
    # print(total, correct)
    ks = [1,3,10]
    pass_at_k = {f"pass@{k}": (estimate_pass_at_k(total, correct, k).mean())*100
                        for k in ks if (total >= k).all()}
    print(pass_at_k)



