import json



def sample2fixture(regex_sample):
	"""
	Convert a regex sample to the Django database's fixture format.
	
	:param regex_sample: the regex sample with the prompt and regex
	:type regex_sample: dict
	:returns: the regex sample converted into the fixture format
	:rtype: {dict}
	"""
	return {
		    "model": "regex_eval.regexsample",
		    "pk": regex_sample["id"],
		    "fields": {
		        "expression": regex_sample["expression"],
		        "raw_prompt": regex_sample["description"],
		        "refined_prompt": None
	    }
	}



def str2fixture(pk, match_string, regex_sample, table_name):
	return {
	    "model": table_name,
	    "pk": pk,
	    "fields": {
	        "string": match_string,
	        "prompt": regex_sample["id"]
	    }
	}

def match2fixture(pk, match_string, regex_sample):
	return str2fixture(pk, match_string, regex_sample, "regex_eval.matchstring")

def non_match2fixture(pk, match_string, regex_sample):
	return str2fixture(pk, match_string, regex_sample, "regex_eval.nonmatchstring")

def main():
	with open(f"RegexEval_v1.json") as f:
		data = json.load(f)



	regex_samples = [] # regex_eval.regexsample
	match_strings = [] # regex_eval.matchstring
	non_match_strings = [] # regex_eval.nonmatchstring	
	stress_test_strings = [] # regex_eval.stressteststring

	pk_matches, pk_non_matches = 1, 1

	for sample in data:
		regex_samples.append(sample2fixture(sample))
		for m in sample["matches"]:
			match_strings.append(match2fixture(pk_matches, m, sample))
			pk_matches += 1

		for m in sample["non_matches"]:
			non_match_strings.append(non_match2fixture(pk_non_matches, m, sample))
			pk_non_matches += 1





	filename = 'RegexEval_v1_fixture.json'
	with open(filename, 'w') as f:
	    json.dump(regex_samples + match_strings + non_match_strings, f, indent=4)


	print("Converted", len(regex_samples), "prompts")
	print("Converted", len(match_strings), "match strings")
	print("Converted", len(non_match_strings), "non-match strings")
	print("Saved to", filename)
	

if __name__ == '__main__':
	main()