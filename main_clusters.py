#!/usr/bin/env python3


import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from options_parser import OptionsParser


def main_clusters():
    # config
    taus = ['1.5', '2.5', '5']
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    box_size = 5.0
    options = OptionsParser().options
    folder_clusters = options['folder_clusters']
    folder_crosses = options['folder_crosses']
    folder_minmax = options['folder_minmax'] # min_x:min_y:min_z:max_x:max_y:max_z
    f = open('clusters', 'w')
    # Analyzing info about clusters
    clusters_info = {
               tau: {
                    str(N): [None for _ in range(5)] for N in Ns
                    } for tau in taus
               }
    for tau in taus:
        for N in Ns:
            for attempt in range(5):
                structure_name = 'tau' + tau + 'N' + str(N) + '_' + str(attempt)
                fname_minmax = folder_minmax + '/' + structure_name
                fname_crosses = folder_crosses + '/' + structure_name
                fname_cluster = folder_clusters + '/' + structure_name
                intersections = get_intersections(fname_crosses)
                clusters = get_clusters(intersections)
                unique_clusters = get_unique_clusters(clusters)
                system_entry = {
                    'clusters_number': len(unique_clusters),
                    'clusters':
                    [
                        {
                        'cluster_size': None,
                        'cluster_x_len': None,
                        'cluster_y_len': None,
                        'cluster_z_len': None 
                        } for _ in range(len(unique_clusters))
                    ]
                }
                for cluster_number, cluster in enumerate(unique_clusters):
                    min_x = min_y = min_z = box_size
                    max_x = max_y = max_z = 0
                    f = open(fname_minmax, 'r')
                    ranges = []
                    for line in f:
                        ranges.append([float(line.split(':')[1]),
                                       float(line.split(':')[2]),
                                       float(line.split(':')[3]),
                                       float(line.split(':')[4]),
                                       float(line.split(':')[5]),
                                       float(line.split(':')[6])])
                    for particle in cluster:
                        min_x = min(min_x, ranges[particle][0])
                        min_y = min(min_y, ranges[particle][1])
                        min_z = min(min_z, ranges[particle][2])
                        max_x = max(max_x, ranges[particle][3])
                        max_y = max(max_y, ranges[particle][4])
                        max_z = max(max_z, ranges[particle][5])
                    entry = system_entry['clusters'][cluster_number] 
                    entry['cluster_size'] = len(cluster)
                    entry['cluster_x_len'] = max_x - min_x
                    entry['cluster_y_len'] = max_y - min_y
                    entry['cluster_z_len'] = max_z - min_z
                clusters_info[tau][str(N)][attempt] = system_entry
    # raw output
    # pprint(clusters_info)
    # pretty output
    # pretty_print_clusters_info(clusters_info)
    return clusters_info


def get_intersections(fname):
    f = open(fname, 'r')
    intersections = list()
    for line in f:
        ls = line.split(':')
        particle_num = int(ls[0])
        for i in range(1, len(ls) - 1): # -1 is to skip terminating '\n'
            intersections.append([particle_num, int(ls[i])])
    return intersections


def get_clusters(intersections, debug_flag=False):
    clusters = list()
    for i in range(len(intersections)):
        for intersection in intersections:
              left = intersection[0]
              right = intersection[1]
              flag_existance_left = False
              flag_existance_right = False
              ids_left = list() # in this clusters left is met;
              ids_right = list() # same for right
              for i, cluster in enumerate(clusters):
                  if left in cluster:
                      flag_existance_left = True
                      ids_left.append(i)
                  if right in cluster:
                      flag_existance_right = True
                      ids_right.append(i)
              # both left and right are not met
              if flag_existance_left and flag_existance_right:
                  continue
              elif (not flag_existance_left) and (not flag_existance_right):
                  clusters.append(set((left, right)))
              # right is met somewhere, left is not
              elif flag_existance_right:
                  for idx in ids_right:
                      clusters[idx].update(set((left,)))
              # left is somewhere, right is not
              elif flag_existance_left:
                  for idx in ids_left:
                      clusters[idx].update(set((right,)))
    return clusters


def get_unique_clusters(clusters):
    result = dict(clusters_number=None,
                  max_cluster_size=None,
                  ave_cluster_size=None)
    unique_clusters = list()
    for i, cluster in enumerate(clusters): 
        existance_flag = False # True if cluster already exists in unique_clusters
        for unique_cluster in unique_clusters:
            if len(cluster) == len(unique_cluster):
                if len(cluster - unique_cluster) == 0:
                    existance_flag = True
        if not existance_flag:
            unique_clusters.append(cluster)
    return unique_clusters


def analyze_clusters(unique_clusters, structure_name):
    # Initial values got from the first cluster
    lengths = [len(cluster) for cluster in unique_clusters]
    if len(lengths) == 0:
        lengths.append(0)
    clusters_description = dict(clusters_number=len(unique_clusters),
                                max_cluster_size=max(lengths),
                                ave_cluster_size=sum(lengths) / len(lengths))
    result = 'system ' + structure_name
    result += ' clusters_number ' + str(len(unique_clusters))
    result += ' max_cluster ' + str(max(lengths))
    result += ' ave_cluster ' + str(sum(lengths) / len(lengths))
    result += '\n'
    return result


def pretty_print_clusters_info(clusters_info):
    taus = list(clusters_info.keys())
    Ns = list(clusters_info[taus[0]].keys())
    cluster_key = ['cluster_size',
                   'cluster_x_len',
                   'cluster_y_len',
                   'cluster_z_len']
    for tau in taus:
        for N in Ns:
            for attempt in range(5):
                entry = clusters_info[tau][N][attempt]
                for cluster_number in range(len(entry['clusters'])):
                    cluster = entry['clusters'][cluster_number]
                    print(tau, N,
                          cluster_number,
                          cluster['cluster_size'],
                          cluster['cluster_x_len'],
                          cluster['cluster_y_len'],
                          cluster['cluster_z_len'])
    return


if __name__ == '__main__':
    main_clusters()
