#!/usr/bin/env python3


import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


def make_clusters_from_intersections(intersections):
    print('intersections:')
    pprint(intersections)
    num = len(intersections)
    clusters = [] # a list of sets

    for i in range(num):
        for intersection in intersections:
            left = intersection[0]
            right = intersection[1]
            existance_flag = False # the cluster with such intersection
                                   # accounted does not exist yet
            new_cluster = list()
            for cluster in clusters:
                if left in cluster:
                    cluster.update((right,))
                    existance_flag = True
                elif right in cluster:
                    cluster.update((left,))
                    existance_flag = True
            if not existance_flag:
                clusters.append(set((left, right)))

    print('clusters:')
    for cluster in clusters:
        print(cluster)
    return clusters


def analyze():
    taus = ['1.5', '2.5', '5']
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    # tmp for testing
    taus = ['5', ]
    Ns = [30]

    general_counter = 0
    for tau in taus:
        for N in Ns:
            for attempt in range(5):
                if general_counter > 0:
                    return None
                general_counter += 1
                intersections = []
                f_crosses = ('Crosses/tau' + tau + 'N' + str(N) +
                             '_' + str(attempt))
                f_ranges = ('ParticleRanges/tau' + tau + 'N' + str(N) +
                             '_' + str(attempt))
                fout = ('Clusters/tau' + tau + 'N' + str(N) +
                         '_' + str(attempt))
                print(f_crosses)
                print(f_ranges)
                fi = open(f_crosses, 'r')
                fo = open(fout, 'w')
                for line in fi:
                    ls = line.split(':')
                    print(ls)
                    me = int(ls[0])
                    with_whom = [int(ls[i]) for i in range(1, len(ls) - 1)]
                    pairs_with_me = [[me, neighbor] for neighbor in with_whom]
                    for pair in pairs_with_me: 
                        intersections.append(pair)
                pprint(intersections)
                clusters = make_clusters_from_intersections(intersections)
                pprint(clusters)
                fi.close()


def test():
    intersections = [[1, 1], [1, 2], [1, 3],
                     [2, 1], [2, 2],
                     [3, 1], [3, 3],
                     [4, 4]]
    make_clusters_from_intersections(intersections)
    return None


#test()
analyze()
