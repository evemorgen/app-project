import json
import time
import statistics
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from multiprocessing import Pool
from itertools import cycle
from sklearn.cluster import AffinityPropagation
from sklearn import metrics


def only_values(values_with_ts):
    return [value for value, _ in values_with_ts]


def nulls_in_a_row(values):
    max_nulls = 0
    for i in range(len(values)):
        val = values[i]
        if val is None:
            nulls = 0
            for j in range(i + 1, len(values)):
                if values[j] is not None:
                    break
                nulls += 1
            max_nulls = max(max_nulls, nulls)
    return max_nulls


def values_in_a_row(values):
    max_values = 0
    for i in range(len(values)):
        val = values[i]
        in_a_row = 0
        for j in range(i + 1, len(values)):
            if values[j] == val and values[j] is not None:
                in_a_row += 1
            else:
                break
        max_values = max(max_values, in_a_row)
    return max_values


def derivative(values):
    return [values[i + 1] - values[i - 1] for i in range(1, len(values) - 1) if values[i + 1] is not None and values[i - 1] is not None]

def dispatcher(length, args):
    i, tup = args
    print(f"[{i}/{length}]")
    metric, values = tup
    return (metric, list(mine_metrics_from_metrics(only_values(json.loads(values))).values()))

def mine_metrics_from_metrics(values):
    npa = np.array([val for val in values if val is not None])
    d1 = derivative(values)
    d2 = derivative(d1)
    return {
        'nulls_count': sum([1 for val in values if val is None]),
        'longest_null_interval': nulls_in_a_row(values),
        'longest_stable_interval': values_in_a_row(values),
        'percentile_90': np.percentile(npa, 90),
        'percentile_95': np.percentile(npa, 95),
        'percentile_99': np.percentile(npa, 99),
        'first_derivative': statistics.mean(d1) if d1 != [] else 0,
        'second_derivative': statistics.mean(d2) if d2 != [] else 0
    }

"""
lines = open('50-99/a.csv').readlines() + \
        open('50-99/d.csv').readlines() + \
        open('50-99/m.csv').readlines() + \
        open('50-99/p.csv').readlines() + \
        open('50-99/r.csv').readlines()
#        open('50-99/q.csv').readlines() + \
#        open('50-99/r.csv').readlines() + \
#        open('50-99/s.csv').readlines()

tuples = [x.split(',', 1) for x in lines]
pool = Pool(4)
data = pool.map(partial(dispatcher, len(tuples)), enumerate(tuples))
#for i, (metric, values) in enumerate(tuples):
#    print(f"[{i}/{len(tuples)}]")
#    data.append()
open('tmp-' + str(time.time()), 'w').write(json.dumps(data))
"""
data = json.loads(open('tmp-1547768474.6103601', 'r').read())
metric_labels = [metric for metric, _ in data]
values = [values for _, values in data]
#padding = max([len(val) for val in values])
#padded_values = [arr + [0 for _ in range(padding - len(arr))] for arr in values]
#print(len(padded_values[0]))

X = np.array(values)

for i in range(100, 10000, 1000):
    af = AffinityPropagation(preference=-i).fit(X)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_
    n_clusters_ = len(cluster_centers_indices)
    print(i, n_clusters_)


print('Estimated number of clusters: %d' % n_clusters_)
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# print("Adjusted Rand Index: %0.3f"
#      % metrics.adjusted_rand_score(labels_true, labels))
# print("Adjusted Mutual Information: %0.3f"
#      % metrics.adjusted_mutual_info_score(labels_true, labels))
# print("Silhouette Coefficient: %0.3f"
#      % metrics.silhouette_score(X, labels, metric='sqeuclidean'))

# #############################################################################
# Plot result
plt.close('all')
plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
    for x in X[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
