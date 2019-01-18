import os
import sys
import json


directory = sys.argv[1]
metric_files = os.listdir(directory)

for i, f in enumerate(metric_files):
    try:
        metrics = json.loads(open(f'{directory}/{f}', 'r').read())
        letters = dict()
        for j, (path, values) in enumerate(metrics):
            print(f'[{i}/{len(metric_files)}] {j}/{len(metrics)} - {f} - {path}')
            part = path.split('.')[1][0].lower()
            if part not in letters:
                letters[part] = []
            letters[part].append((path, values))
        for letter in letters:
            part_file =  letter + ".csv"
            for path, values in letters[letter]:
                open(f'{directory}/{part_file}', 'a').write(f"{path},{json.dumps(values)}\n")
    except:
        print(f"========= BAD FILE {f} ===========")
