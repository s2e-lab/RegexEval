# %%
names = ["Phi_Raw_Output","Phi_Refined_Output","T5_Raw_Output","T5_Refined_Output","Text_DaVinci_Raw_Output","Text_DaVinci_Refined_Output","GPT3.5_Raw_Output","GPT3.5_Refined_Output"]
for name in names:
    print(name)
    filename = f'../Output/{name}_Compiled_Result.json'
    with open(filename) as f:
        data = f.readlines()
    with open(f'./Input_Data/{name}.txt', 'w') as f:

        for i in range(len(data)):
            if (i-3)%5 == 0:
                line = data[i]
                current_data = line.split(":")[1].strip()[1:-2]
                f.write(f"{current_data}\n")
        # for item in data:
        #     f.write(f"{item['completion']}\n")
    print("Done")


