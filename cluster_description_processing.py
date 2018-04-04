#!/usr/bin/env python3


import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


def cluster_description_processing():
    fname_clusters = 'clusters_description'
    fname_young_ave = '/home/anton/Projects/FEM/young_ave'
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    possible_param_names = ['system_name',
                            'tau',
                            'N',
                            'clusters_number',
                            'max_cluster_size',
                            'ave_cluster_size']
    fyoung = open(fname_young_ave, 'r')
    moduli = {tau : {str(N): None for N in Ns} for tau in taus}
    for line in fyoung:
        tau = line.split()[0]
        N = str(int(line.split()[1]))
        E = float(line.split()[2])
        moduli[tau][N] = E
    database = get_database(fname_clusters)
    for entry in database:
        tau = entry['tau']
        N = entry['N']
        entry['modulus'] = moduli[tau][str(N)]
    #for key in possible_param_names:
    #    print(key, end=' ')
    print('tau', '\t', 'N', '\t', 'E')
    for tau in taus:
        for N in Ns:
            system_name = 'tau' + tau + 'N' + str(N)
            params = {'N': N, 'tau': tau}
            averaging = average_by_params(database, params)
            averaging['system_name'] = system_name
            print(tau, '\t', N, '\t', "%.2f" % averaging['modulus'])
            #for key in possible_param_names:
            #    print(averaging[key], end=' ')
            #print()
    return


def get_database(fname):
    f = open(fname, 'r')
    database = []
    for line in f:
        ls = line.split()
        tau = ls[1].split('/tau')[1].split('N')[0]
        N = int(ls[1].split('/tau')[1].split('N')[1].split('_')[0])
        system_name = ls[1][1:]
        clusters_number = float(ls[3])
        max_cluster_size = float(ls[5])
        ave_cluster_size = float(ls[7])
        database_entry = {'system_name': system_name,
                          'tau': tau,
                          'N': N,
                          'clusters_number': clusters_number,
                          'max_cluster_size': max_cluster_size,
                          'ave_cluster_size': ave_cluster_size}
        database.append(database_entry)
    return database


def average_by_params(database, params):
    """
    database - a list(dict(param_name_i: param_value_i)), i <= N
    params - a dict(param_name_i, param_value_i), i <= N
            (may be chosen or all params)
    chosen - result, a list of chosen entries from database with
             satisfying values of chosen parameters
    """
    if len(database) == 0:
        print('error in average_by_params:',
              'database size is zero')
        import sys
        sys.exit()
    param_names = params.keys()
    params_number = len(param_names)
    if params_number == 0:
        print('error in average_by_params:',
              'number of params equals zero')
        import sys
        sys.exit()
    chosen = []
    ave_param_values = {key: 0 for key in database[0].keys()}
    chosen_entries_number = 0
    for entry in database:
        flag_choose = True
        for param in param_names:
            if entry[param] != params[param]:
                flag_choose = False
        if flag_choose:
            chosen.append(entry)
    if len(chosen) == 0:
        print('error in average_by_params:',
              'nothing is chosen')
        import sys
        sys.exit()
    #pprint(chosen)
    #return
    for entry in chosen:
        for param in entry.keys():
            try:
                ave_param_values[param] += float(entry[param])
            except:
                pass
    #pprint(ave_param_values)
    for key in ave_param_values.keys():
        try:
            ave_param_values[key] /= len(chosen)
        except:
            pass
    #pprint(ave_param_values)
    return ave_param_values


cluster_description_processing()
