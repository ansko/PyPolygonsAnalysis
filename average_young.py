#!/usr/bin/env python3


import os

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


def average_young():
    folder = '/home/anton/FEMFolder3/results_archive/'
    folder += 'Отчёт - результаты/Точные сетки/From geofiles (filler'
    folder += ' thickness=0.1)/more_than_2_elements_in_thickness/Young_results_ALL'
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    for tau in taus:
        for N in Ns:
            moduli = [0.0 for i in range(9)]
            additional_folder = 'tau' + tau + 'N' + str(N)
            #print(additional_folder)
            fnames = os.listdir(folder + '/' + additional_folder)
            #print(len(files))
            if len(fnames) < 15:
                continue
            for fname in fnames:
                full_fname = folder + '/' + additional_folder + '/' + fname
                values_started = False
                f = open(full_fname)
                for line in f:
                    if line.startswith('E11'):
                        values_started = True
                        continue
                    if values_started:
                        ls = line.split()
                        for i in [0, 4, 8]:
                            if not (1.01 > 100 * float(ls[i]) > 0.99):
                                #print(ls[i], ls[9 + i])
                                continue
                            #print("%.2f" % (float(ls[9 + i]) / float(ls[i])))
                            moduli[i] += float(ls[9 + i]) / float(ls[i])
            Exx =  (moduli[0] / 5)
            Eyy =  (moduli[4] / 5)
            Ezz =  (moduli[8] / 5)
            E = (Exx + Eyy + Ezz) / 3
            taus = tau
            if len(tau) != 3:
                taus = tau + '  '
            if len(str(N)) == 2:
                print(taus, N, "%.2f" % E)
            else:
                print(taus, N, "%.2f" % E)

if __name__ == '__main__':
    average_young()
