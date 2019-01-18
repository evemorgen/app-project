__author__ = "Konrad Najder"

import os
import json


greppers = ["servers", "diskspace", "loadavg", "opal", "gb_percentfree", "zookeeper", "cpu", "idle", "inodes_percentfree", "processes_total", "scoreboard", "listendrops", "vms", "ipx", "repo_backup", "backup1", "nginx", "uptime", "error", "agent_missing", "unmanaged", "process", "null_size", "errors", "403", "waiting", "limit", "failedtestcount", "web", "http", "status-code", "request", "backup", "policy_worker", "missing_reports", "failure", "ok_count", "crit", "err_count", "499", "500", "501", "502", "503", "disabled_time", "duration", "not_processed", "rx_drop", "salting", "memory_exhausted", "load15min", "agent_errors", "400", "mem_free", "active"]

json_dir = "metrics"
output_dir_bad = "0-50"
output_dir_ok = "50-99"
output_dir_good = "100"

try:
    os.mkdir(output_dir_bad)
    os.mkdir(output_dir_ok)
    os.mkdir(output_dir_good)
except Exception:
    pass

json_paths = os.listdir(json_dir)

done_files = set(os.listdir(output_dir_bad) + os.listdir(output_dir_good) + os.listdir(output_dir_ok))
all_nulls = 0
grep_skips = 0

for i, json_path in enumerate(json_paths):
    if json_path in done_files or "txt" not in json_path:
        print(f"{json_path} is already done, skipping...")
        continue
    print(f"[{i}/{len(json_paths)}] Processing {json_path}...")
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
            for grep in greppers:
                if grep in target:
                    break
            else:
                print(f"skipping {target} by filter")
                grep_skips += 1
                continue
            total = len(datapoints)
            if len(datapoints) == len([1 for val in datapoints if val[0] is None]):
                print(f"all nulls for {target}")
                all_nulls += 1
                continue
            bad = len([1 for d in datapoints if d[0] is None])
            percent = (1 - (bad / total)) * 100.0
            values = [x for x, _ in datapoints]
            min_v = min([val for val in values if val is not None])
            max_v = max([val for val in values if val is not None])
            normalized_v = []
            if (max_v - min_v) == 0:
                normalized_v = [x for x in values]
            else:
                normalized_v = [(x - min_v) / (max_v - min_v) if x is not None else x for x in values]
            timestamps = [t for _, t in datapoints]
            data_normalized = list(map(list, zip(normalized_v, timestamps)))  # glupie
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

print("all_nulls: " + str(all_nulls))
print("grep_skips: " + str(grep_skips))
