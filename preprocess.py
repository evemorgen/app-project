__author__ = "Konrad Najder"

import os, json


json_dir = "metrics"
output_dir_bad = "0-50"
output_dir_ok = "50-99"
output_dir_good = "100"

null_value = -10.0

try:
    os.mkdir(output_dir_bad)
    os.mkdir(output_dir_ok)
    os.mkdir(output_dir_good)
except:
    pass

json_paths = os.listdir(json_dir)

done_files = set(os.listdir(output_dir_bad) + os.listdir(output_dir_good) + os.listdir(output_dir_ok))

for json_path in json_paths:
    if json_path in done_files:
        print(f"{json_path} is already done, skipping...")
        continue
    print(f"Processing {json_path}...")
    with open(os.path.join(json_dir, json_path)) as json_file:
        json_text = json.load(json_file)
        output_bad = []
        output_ok = []
        output_good = []
        for datum in json_text:
            if len(datum) == 0:
                continue
            data = datum[0]
            datapoints = data['datapoints']
            target = data['target']
            total = len(datapoints)
            bad = len([1 for d in datapoints if d[0] is None])
            percent = (1 - (bad / total)) * 100.0
            values = [x if x is not None else null_value for x, _ in datapoints]
            min_v = min(values)
            max_v = max(values)
            normalized_v = []
            if (max_v - min_v) == 0:
                normalized_v = [x for x in values]
            else:
                normalized_v = [(x - min_v) / (max_v - min_v) for x in values]
            timestamps = [t for _, t in datapoints]
            data_normalized = list(map(list, zip(normalized_v, timestamps))) # glupie
            # print(f"{data['target']}: {percent}%")
            if percent < 50.0:
                output_bad.append((target, data_normalized))
            elif percent < 100.0:
                output_ok.append((target, data_normalized))
            else:
                output_good.append((target, data_normalized))

        if len(output_bad) != 0:
            with open(os.path.join(output_dir_bad, json_path), "w") as output_file:
                output_file.write(json.dumps(output_bad))
        if len(output_ok) != 0:
            with open(os.path.join(output_dir_ok, json_path), "w") as output_file:
                output_file.write(json.dumps(output_ok))
        if len(output_good) != 0:
            with open(os.path.join(output_dir_good, json_path), "w") as output_file:
                output_file.write(json.dumps(output_good))
