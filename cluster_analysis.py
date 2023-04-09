#! /usr/bin/env python3
# SPDX-FileCopyrightText: © 2021 Yake Ho Foong
# SPDX-License-Identifier: BSD-3-Clause

import subprocess

# results
inter_cluster_densities = []
intra_cluster_densities = []

# distance measures
distance_measures = ['CosineDistanceMeasure', 'TanimotoDistanceMeasure']

for i, distance_measure in enumerate(distance_measures):

    # initialize with Canopy
    canopy_str = (
        'mahout canopy -i docs-vectors/tfidf-vectors'
        + ' -ow -o docs-canopy-centroids'
        + ' -dm org.apache.mahout.common.distance.'
        + f'{distance_measure}-t1 0.5 -t2 0.3')
    canopy_run_output_lines = (
        subprocess
        .run(canopy_str.split(' '), stdout=subprocess.PIPE)
        .stdout.decode('utf-8').splitlines())

    # key is the K of K Means
    inter_cluster_densities.append(dict())
    intra_cluster_densities.append(dict())

    # run through different Ks
    for k in range(1, 11):
        kmeans_str = (
            'mahout kmeans -i docs-vectors/tfidf-vectors -c'
            + ' docs-canopy-centroids -o docs-kmeans-clusters -dm'
            + ' org.apache.mahout.common.distance'
            + f'.{distance_measure} -cl -cd 0.1 -ow -x 20 -k {k}')
        check_result_str = 'hadoop fs -ls docs-kmeans-clusters'
        collect_result_str_template = (
            'mahout clusterdump -dt sequencefile -d'
            + ' docs-vectors/dictionary.file-* -i'
            + ' docs-kmeans-clusters/clusters-{}-final -o'
            + ' clusters.txt -b 100 -p '
            + 'docs-kmeans-clusters/clusteredPoints -n 20 --evaluate')
        show_result_str = 'tail ./clusters.txt'

        kmeans_run_output_lines = (
            subprocess
            .run(kmeans_str.split(' '), stdout=subprocess.PIPE)
            .stdout.decode('utf-8').splitlines())
        check_run_output_lines = (
            subprocess
            .run(check_result_str.split(' '), stdout=subprocess.PIPE)
            .stdout.decode('utf-8').splitlines())

        last_subfolder = check_run_output_lines[-1].split('/')[-1]
        assert(
            last_subfolder.startswith('clusters-'),
            "Error in K-Means Cluster output, "
            + "no folder name starting with 'clusters-'"
            + "\n" + check_run_output_lines[-1])
        assert(
            last_subfolder.endswith('-final'),
            "Error in K-Means Cluster output, "
            + "no folder name ending with '-final'"
            + "\n" + check_run_output_lines[-1])
        num = int(last_subfolder.split('-')[1])
        collect_result_str = collect_result_str_template.format(num)

        collect_run_output_lines = (
            subprocess
            .run(collect_result_str.split(' '), stdout=subprocess.PIPE)
            .stdout.decode('utf-8').splitlines())
        show_run_output_lines = (
            subprocess
            .run(show_result_str.split(' '), stdout=subprocess.PIPE)
            .stdout.decode('utf-8').splitlines())

        for line in show_run_output_lines:
            if line.startswith('Inter-Cluster Density:'):
                inter_cluster_densities[i][k] = float(line.split(':')[-1])
            if line.startswith('Intra-Cluster Density:'):
                intra_cluster_densities[i][k] = float(line.split(':')[-1])


# print results
for i in range(len(inter_cluster_densities)):
    print(f'Distance measure: {distance_measures[i]}')
    for k in inter_cluster_densities[i].keys():
        print(
            f'k: {k}, inter-cluster density: '
            + f'{inter_cluster_densities[i][k]}, '
            + f'intra-cluster density: {intra_cluster_densities[i][k]}')
