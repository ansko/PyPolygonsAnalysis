#!/usr/bin/env python3


import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from options_parser import OptionsParser


def main_clusters():
    taus = ['1.5', '2.5', '5']
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]

    taus = ['1.5', ]
    Ns = [4, ]

    options = OptionsParser().options
    folder_clusters = options['folder_clusters']
    folder_crosses = options['folder_crosses']
    folder_minmax = options['folder_minmax'] # min_x:min_y:min_z:max_x:max_y:max_z
    for tau in taus:
        for N in Ns:
            for attempt in range(1):#5):
                structure_name = '/tau' + tau + 'N' + str(N) + '_' + str(attempt)
                fname_minmax = folder_minmax + '/' + structure_name
                fname_crosses = folder_crosses + '/' + structure_name
                fname_cluster = folder_clusters + '/' + structure_name
                intersections = get_intersections(fname_crosses)
                print(intersections)
                clusters = get_clusters(intersections)


def get_intersections(fname):
    f = open(fname, 'r')
    intersections = list()
    for line in f:
        ls = line.split(':')
        particle_num = int(ls[0])
        for i in range(1, len(ls) - 1): # -1 is to skip terminating '\n'
            intersections.append([particle_num, int(ls[i])])
    return intersections


def get_clusters(intersections):
    print(len(intersections), 'intersections')
    clusters = list()
    for i in range(len(intersections)):
        for intersection in intersections:
              #print(intersection)
              left = intersection[0]
              right = intersection[1]
              flag_existance_left = False
              flag_existance_right = False
              ileft = -1  # in this cluster left is met;
                          # -1 means that it is not met
              iright = -1 # same for right
              for i, cluster in enumerate(clusters):
                  if left in cluster:
                      flag_existance_left = True
                      ileft = i
                  if right in cluster:
                      flag_existance_right = True
                      iright = i
              if flag_existance_left:
                  clusters[ileft].update((right,))
              else:
                  clusters.append(set((left,)))
              if flag_existance_right:
                  clusters[iright].update((left,))
              else:
                  clusters.append(set((right,)))
        print(clusters)
    print('result:')
    print(clusters)


if __name__ == '__main__':
    main_clusters()
