#!/usr/bin/env python3


from contextlib import redirect_stdout
import copy
import math

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


def create_database():
    """
    Creates database from files with data about clusters and systems.
    """
    possible_param_values = {'tau': ['1.5', '2.5', '5'],
                             'N': [4, 8, 12, 16, 20, 24, 28, 30],
                             'attempt': range(5)}
    # Creating empty database for storing clusters
    database_clusters = {
        tau: {
            str(N): [
                [] for attempt in range(5)
            ] for N in possible_param_values['N']
        } for tau in possible_param_values['tau']
    }
    for tau in possible_param_values['tau']:
        for N in possible_param_values['N']:
            for attempt in range(5):
                database_clusters[tau][str(N)][attempt] = {
                    'cluster_number': None,
                    'clusters_amount': None,
                    'cluster_size': None,
                    'cluster_x_len': None,
                    'cluster_y_len': None,
                    'cluster_z_len': None
                }
    # Creating empty database for storing systems
    database_systems = {
        tau: {
            str(N): [
                None for attempt in range(5)
            ] for N in possible_param_values['N']
        } for tau in possible_param_values['tau']
    }
    # Filling both databases with data from files
    f = open('all', 'r')
    for line_number, line in enumerate(f):
        if line_number == 0:
            continue
        tau = line.split()[0]
        N = line.split()[1]
        attempt = int(line.split()[2])
        Exx = float(line.split()[3])
        Eyy = float(line.split()[4])
        Ezz = float(line.split()[5])
        cluster_number = int(line.split()[6])
        clusters_amount = int(line.split()[7])
        cluster_size = int(line.split()[8])
        cluster_x_len = float(line.split()[9])
        cluster_y_len = float(line.split()[10])
        cluster_z_len = float(line.split()[11])
        database_systems[tau][N][attempt] = {
            'Exx': Exx, 'Eyy': Eyy, 'Ezz': Ezz,
            'clusters_amount': clusters_amount
        }
        database_clusters[tau][N][attempt]['cluster_number'] = cluster_number
        database_clusters[tau][N][attempt]['clusters_amount'] = clusters_amount
        database_clusters[tau][N][attempt]['cluster_size'] = cluster_size
        database_clusters[tau][N][attempt]['cluster_x_len'] = cluster_x_len
        database_clusters[tau][N][attempt]['cluster_y_len'] = cluster_y_len
        database_clusters[tau][N][attempt]['cluster_z_len'] = cluster_z_len
    # Making general database
    general_database = []
    for tau in possible_param_values['tau']:
        for N in possible_param_values['N']:
            for attempt in range(5):
                system_entry = database_systems[tau][str(N)][attempt]
                cluster_entry = database_clusters[tau][str(N)][attempt]
                entries = set()
                entry = {
                    'tau': tau,
                    'N': str(N),
                    'attempt': attempt,
                    'clusters_amount': system_entry['clusters_amount'],
                    'Exx': str(system_entry['Exx']),
                    'Eyy': str(system_entry['Eyy']),
                    'Ezz': str(system_entry['Ezz'])
                }
                for cluster_number in range(system_entry['clusters_amount']):
                    new_entry = copy.deepcopy(entry)
                    new_entry['cluster_number'] = cluster_number
                    new_entry['cluster_size'] = cluster_entry['cluster_size']
                    new_entry['cluster_x_len'] = cluster_entry['cluster_x_len']
                    new_entry['cluster_y_len'] = cluster_entry['cluster_y_len']
                    new_entry['cluster_z_len'] = cluster_entry['cluster_z_len']  
                    general_database.append(new_entry)
                if system_entry['clusters_amount'] == 0:
                    entry['cluster_number' ] = None
                    entry['cluster_size'] = None
                    entry['cluster_x_len'] = None
                    entry['cluster_y_len'] = None
                    entry['cluster_z_len'] = None
                    general_database.append(entry)
    for entry in general_database:
        for key in entry.keys():
            entry[key] = str(entry[key])
    return general_database


def select(database, selection_params):
    """
    Performs selection of relevant entries.
    """
    if len(database) == 0:
        print('database is empty, nothing to select')
        return None
    # Selecting relevant entries
    chosen_entries = []
    selection_keys = selection_params.keys()
    selection_params = {key: str(selection_params[key]) for key in selection_keys}
    all_keys = database[0].keys()
    for entry in database:
        new_entry = {}
        flag = True # Becomes false if there exists any key that
                    # entry[key] != selection_params[key]
        for selection_key in selection_keys:
            if selection_params[selection_key] != entry[selection_key]:
                flag = False
                break
        if flag:
            for key in all_keys:
                if key in selection_keys:
                    continue
                new_entry[key] = entry[key]
            chosen_entries.append(new_entry)
    return chosen_entries


def output_database(database, ordered_keys=None, heading=False):
    """
    A kind of "pretty" output of a database.
    """
    field_lengths = {'tau': 3,
                     'N': 2,
                     'Exx': [2, 3],
                     'Eyy': [2, 3],
                     'Ezz': [2, 3],
                     'attempt': 7,
                     'clusters_amount': 15,
                     'cluster_number': 14,
                     'cluster_size': 12,
                     'cluster_x_len': [2, 11],
                     'cluster_y_len': [2, 11],
                     'cluster_z_len': [2, 11]}
    if database is None:
        print('No database')
        return None
    if len(database) == 0:
        print('Empty database')
        return None
    if ordered_keys is None:
        ordered_keys = database[0].keys()
    # Print heading
    if heading:
        for key in ordered_keys:
            str_key = str(key)
            length = field_lengths[key]
            if isinstance(length, list):
                if len(length) == 2:
                    length = length[0] + 1 + length[1]
                else:
                    print('strange format of field length',
                          length)
                    return None
            param = 1
            while len(str_key) < length:
                if param < 0:
                    str_key = ' ' + str_key
                else:
                    str_key += ' '
                param *= -1
            print(str_key, end=' ')
        print()
    # Print entries
    for entry in database:
        for key in ordered_keys:
            if key in field_lengths.keys():
                value = str(entry[key])
                length = field_lengths[key]
                if value == 'None':
                    if isinstance(length, list):
                        if len(length) == 2:
                            length = length[0] + 1 + length[1]
                        else:
                            print('strange format of field length',
                                  length)
                            return None
                    if len(value) < length:
                        value += ' ' * (length - len(value))
                    print(value, end=' ')
                    continue
                if isinstance(length, int):
                    str_length = len(value)
                    if str_length < length:
                        value += ' ' * (length - str_length)
                    print(value, end=' ')
                elif isinstance(length, list) and len(length) == 2:
                    integer_length = length[0]
                    fraction_length = length[1]
                    ls = value.split('.')
                    integer = str(ls[0])
                    if len(integer) == 0:
                        integer = '0'
                    if len(ls) == 1: # entry[key] is integer number
                        fraction = ' ' * fraction_length
                    else:
                        fraction = str(ls[1])
                    if len(integer) < integer_length:
                        integer = ' ' * (integer_length - len(integer)) + integer
                    if len(fraction) < fraction_length:
                        fraction += ' ' * (fraction_length - len(fraction))
                    print(integer + '.' + fraction, end=' ')
                else:
                    print('strange format of field length',
                          length)
                    return None
            else:
                print(entry[key], end=' ')
        print()
    return len(database)


def remove_repeating(database):
    """
    Removes entries from database that repeat more than one time.
    """
    output = []
    if len(database) == 0:
        print('database is empty, nothing to remove')
        return None
    keys = database[0].keys()
    output = database
    # Remove entries that are the same
    non_overlapping_indices = list(range(len(output)))
    for i, entry_i in enumerate(output):
        for j, entry_j in enumerate(output):
            if i == j:
                continue
            repeating_values_number = 0 # number of values that are the same
                                        # in i-th and j-t entries
            for key in keys:
                if entry_i[key] == entry_j[key]:
                    repeating_values_number += 1
            if (repeating_values_number == len(keys) and
                j in non_overlapping_indices and
                i in non_overlapping_indices):
                    non_overlapping_indices.remove(j)
    final_result = [output[idx] for idx in non_overlapping_indices]
    return final_result


def project(database, projection_keys):
    """
    Removes raws from database, only values on projection_keys are stored.
    """
    result = []
#    keys = database[0].keys()
    for entry in database:
        new_entry = {}
        for key in projection_keys:
            new_entry[key] = entry[key]
        result.append(new_entry)
    return result


def main():
    """
    The function is made for tests.
    """
    # Configuring task
    all_possible_keys = set(('tau', 'N', 'attempt', # system params
                             'Exx', 'Eyy', 'Ezz',   # mechanical params
                             'cluster_number',      # cluster params
                             'cluster_size',
                             'cluster_x_len',
                             'cluster_y_len',
                             'cluster_z_len',
                             'clusters_amount'))
    selection_params = {
        'tau': '1.5',
    }
    projection_params = set(('N', 'attempt',
                             'Exx', 'Eyy', 'Ezz',
                             'clusters_amount'))
    ordered_keys = ['N', 'attempt',
                    'Exx', 'Eyy', 'Ezz',
                    'clusters_amount']
    # Performing actions
    database = create_database()
    database = select(database, selection_params)
    database = project(database, projection_params)
    database = remove_repeating(database)
    etnries_number = output_database(database, ordered_keys)
    return 0


def ave_young_vs_tau():
    """
    Select data for plotting E(fi) for all taus.
    """
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    # Configuring task
    box_volume = 125.0
    filler_R = 0.87
    filler_h = 0.1
    sin_central = math.sin(2 * math.pi / 6)
    filler_particle_volume = 6 * filler_R**2 / 2 * sin_central * filler_h
    # Performing actions
    database = create_database()
    for tau_value in taus:
        Es = [0 for i in range(8)]
        shell_h = (float(tau_value) * 2 + 1) * filler_h
        shell_R = (float(tau_value) + 1) * filler_R
        shell_particle_volume = shell_R**2 * math.pi * shell_h
        for i, N in enumerate(Ns):
            for attempt in range(5):
                selection_params = {'tau': tau_value,
                                    'N': str(N),
                                    'attempt': str(attempt)}
                selected = select(database, selection_params)
                Exx = sum([float(entry['Exx']) for entry in selected])
                Eyy = sum([float(entry['Eyy']) for entry in selected])
                Ezz = sum([float(entry['Ezz']) for entry in selected])
                Exx /= len(selected)
                Eyy /= len(selected)
                Ezz /= len(selected)
                Es[i] += (Exx + Eyy + Ezz) / 3
        f = open('ave_young_vs_tau' + tau_value, 'w')
        with redirect_stdout(f):
            print('fi_filler', 'ave_E_xyz')
            for i, E in enumerate(Es):
                filler_fi = filler_particle_volume * Ns[i] / box_volume
                print("%.3f" % filler_fi, '\t\t', "%.3f" % (E / 5))
    return 0


def ave_clusterized_particles_fraction():
    """
    Select data for plotting E(fi) for all taus.
    """
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    # Configuring task
    # Performing actions
    database = create_database()
    for tau_value in taus:
        for i, N in enumerate(Ns):
            print('---', tau_value, N)
            clusters_amount = 0
            clusterized = 0
            for attempt in range(1):#range(5):
                selection_params = {'tau': tau_value,
                                    'N': str(N),
                                    'attempt': str(attempt)}
                selected = select(database, selection_params)
                pprint(selected)
                continue
        #f = open('ave_clusterized' + tau_value, 'w')
        #with redirect_stdout(f):
        if False:
            print('N_particles', 'clusterized_fraction')
            for i in len(clusterized):
                print(N, clusterized[i])
    return 0


ave_clusterized_particles_fraction()
#ave_young_vs_tau()
#main()
