#!/usr/bin/env python3


import os

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from main_clusters import (main_clusters, get_intersections, get_clusters,
                           get_unique_clusters, analyze_clusters)

def main():
    """
    Marges info about Young's moduli and about clusters.
        folder_geofiles - folder with geofiles
        folder_moduli - folder with stress/strain output
        clusters_fname - file with info about clusters
    """
    # Config
    folder_geofiles = '/home/anton/Projects/FEM/geofiles'
    folder_moduli = '/home/anton/Projects/FEM/moduli'
    taus = ['1.5', '2.5', '5']
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    # Getting Young's moduli for all systems
    moduli = {
             tau: {
                  str(N): [None for attempt in range(5) ] for N in Ns
                  } for tau in taus
             }
    for tau in taus:
        for N in Ns:
            folder_name = 'tau' + tau + 'N' + str(N)
            full_path = folder_moduli + '/' + folder_name
            file_names = os.listdir(full_path)
            modulus_entries = [{'Exx': None,
                                'Eyy': None,
                                'Ezz': None,
                                'attempt': None,
                                'fname': None} for i in range(5)]
            for fname in file_names:
                # Getting attempt number from fname
                for part in fname.split('_'):
                    if len(part) != 1:
                        continue
                    try:
                        attempt = int(part)
                    except:
                        pass
                modulus_entry = modulus_entries[attempt]
                modulus_entry['fname'] = fname
                modulus_entry['attempt'] = attempt
                full_fname = full_path + '/' + fname
                f = open(full_fname, 'r')
                for line_number, line in enumerate(f):
                    if line_number != 14:
                        continue
                    ls = line.split()
                    for idx in [0, 4, 8]:
                        strain = float(ls[idx])
                        stress = float(ls[idx + 9])
                        if strain < 0.0099:
                            continue
                        modulus = stress / strain
                        if idx == 0:
                            modulus_entry['Exx'] = modulus
                        elif idx == 4:
                            modulus_entry['Eyy'] = modulus
                        else:
                            modulus_entry['Ezz'] = modulus
                moduli[tau][str(N)][attempt] = modulus_entries[attempt]
    # Getting clusters info
    clusters_info = main_clusters()
    # Output
    full_output(moduli, clusters_info)
    return None

def full_output(moduli, clusters_info):
    taus = ['1.5', '2.5', '5']
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    for tau in taus:
        str_tau = tau
        if len(tau) < 3:
            str_tau += '  '
        for N in Ns:
            str_N = str(N)
            if N < 10:
                str_N += ' '
            for attempt in range(5):
                clusters = clusters_info[tau][str(N)][attempt]['clusters']
                Exx = moduli[tau][str(N)][attempt]['Exx']
                Eyy = moduli[tau][str(N)][attempt]['Eyy']
                Ezz = moduli[tau][str(N)][attempt]['Ezz']
                Exx_corr = ''
                if Exx < 10:
                   Exx_corr = ' '
                Eyy_corr = ''
                if Eyy < 10:
                   Eyy_corr = ' '
                Ezz_corr = ''
                if Ezz < 10:
                   Ezz_corr = ' '
                if len(clusters) == 0:
                    print(str_tau, str_N, attempt,
                          Exx_corr, "%.3f" % Exx,
                          Eyy_corr, "%.3f" % Eyy,
                          Ezz_corr, "%.3f" % Ezz,
                          0,
                          0,
                          ' 0',
                          "%.3f" % float(0),
                          "%.3f" % float(0),
                          "%.3f" % float(0))
                for cluster_number, cluster in enumerate(clusters):
                    str_cluster_size = str(cluster['cluster_size'])
                    if len(str_cluster_size) < 2:
                        str_cluster_size = ' ' + str_cluster_size
                    print(str_tau, str_N, attempt,   # system params
                          Exx_corr, "%.3f" % Exx,    # system mechanical props
                          Eyy_corr, "%.3f" % Eyy,    #
                          Ezz_corr, "%.3f" % Ezz,    #
                          cluster_number,            # props of cluster
                          len(clusters),             # for every cluster
                          str_cluster_size,          ##########
                          "%.3f" % cluster['cluster_x_len'],  #
                          "%.3f" % cluster['cluster_y_len'],  #
                          "%.3f" % cluster['cluster_z_len'])  #
    return None


main()
