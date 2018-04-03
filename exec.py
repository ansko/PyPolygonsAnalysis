#!/usr/bin/env python3
#coding=utf-8


import math
import subprocess

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

REPEATS = 1
CONC_RUNS = 100
STEP = 1000


exf_opts = {
            'CUBE_EDGE_LENGTH': 10.0,
            'MAX_ATTEMPTS': 1000.0,
            'VERTICES_NUMBER': 8.0,
            'THICKNESS': 0.1,
            'OUTER_RADIUS': 0.5,
            'SHELL_THICKNESS': 0.1
}


def percolationConcentration():
    h = exf_opts['THICKNESS']
    n = exf_opts['VERTICES_NUMBER']
    r = exf_opts['OUTER_RADIUS'] * math.cos(math.pi / n)
    sh = exf_opts['SHELL_THICKNESS']
    diskVolume = math.pi * r ** 2 * h
    l = exf_opts['CUBE_EDGE_LENGTH']
    f = open('tmp/stdout_polygonal.log', 'w')
    log = open('tmp/logExec.log', 'w')
    for i in range(1, CONC_RUNS):
        percRates = [0, 0, 0]
        concentration = diskVolume * i * STEP / l**3
        print("%.4f" % concentration, end=" ")
        for r in range(REPEATS):
            ff = open('tmp/stdout_int_an.log', 'w')
            fopt = open('tmp/options.ini', 'w')
            for key, val in exf_opts.items():
                fopt.write(key + ' ' + str(val) + '\n')
            fopt.write('DISKS_NUM ' + str(i * STEP) + '\n')
            fopt.write('FNAME geofiles/' + str(i) + '_' + str(r) + '.geo\n')
            fopt.close()
            subprocess.call(['./polygonal', ], stdout=f)
            subprocess.call(['./int_an.py', ], stdout=ff)
            ff.close()
            fff = open('tmp/stdout_int_an.log', 'r')
            flagx = flagy = flagz = False
            for line in fff:
                if line.split()[0] == 'True':
                    flagx = True
                if line.split()[1] == 'True':
                    flagy = True
                if line.split()[2] == 'True':
                    flagz = True
            if flagx:
                percRates[0] += 1
            if flagy:
                percRates[1] += 1
            if flagz:
                percRates[2] += 1
            log.write(str(i) + '_' + str(r) + ' ')
            log.write(str(flagx) + str(flagy) + str(flagz) + '\n')
        percRates[0] /= REPEATS
        percRates[1] /= REPEATS
        percRates[2] /= REPEATS
        averageRate = (percRates[0] + percRates[1] + percRates[2]) / 3
        print(averageRate)


def crystRate():
    results = []
    totalResults = []
    genMesh = '/home/anton/FEMFolder3/gen_mesh.x'
    volfolder = '/home/anton/FEMFolder3/'
    geofolder = '/home/anton/Projects/CppPolygons/geofiles/'
    h = exf_opts['THICKNESS']
    n = exf_opts['VERTICES_NUMBER']
    r = exf_opts['OUTER_RADIUS'] * math.cos(math.pi / n)
    sh = exf_opts['SHELL_THICKNESS']
    diskVolume = math.pi * r ** 2 * h
    l = exf_opts['CUBE_EDGE_LENGTH']
    for i in range(1, 2):
        subprocess.call(['mkdir', 'tmp'])
        subprocess.call(['mkdir', 'tmp/tmp'])
        subprocess.call(['mkdir', 'tmp/tmp/'+ str(i) + '_AR_' + str(int(2 * r / h))])
        tmpdir = 'tmp/tmp/' + str(i) + '_AR_' + str(int(2 * r / h)) + '/'
        out_p = open(tmpdir + 'out_poly.log', 'w')
        out_g = open(tmpdir + 'out_genmesh.log', 'w')
        out_ia = open(tmpdir + 'out_int_an.log', 'w')
        flog = open(tmpdir + 'log', 'w')
        out_va = open('tmp/out_va.log', 'w')
        print(i/1000)
        fillerVolume = i / 1000 * l**3
        particlesNumber = fillerVolume // diskVolume
        for r in range(REPEATS):
            ff = open(tmpdir + 'stdout_int_an.log', 'w')
            fopt = open(tmpdir + 'options.ini', 'w')
            for key, val in exf_opts.items():
                fopt.write(key + ' ' + str(val) + '\n')
            fopt.write('DISKS_NUM ' + str(particlesNumber) + '\n')
            fopt.write('PERC_FNAME perc/' + str(i * STEP) + 'perc\n')
            geofname = geofolder + str(i/100) + '.geo'
            fopt.write('FNAME ' + geofname + '\n')
            fopt.close()
            subprocess.call(['./polygonal',], stdout=out_p)
            subprocess.call([genMesh, geofname, '0.15', '2', '2'], stdout=out_g)
            volfname = 'generated.vol'
            subprocess.call(['./volAnalyzer.py', volfname])#, stdout=out_va)
            subprocess.call(['./int_an.py', ])#, stdout=out_ia)
        out_va.close()
        ffff = open(tmpdir + 'out_va.log', 'r')
        for line in ffff:
            words = line.split()
            floats = []
            for word in words:
                word = float(word)
                floats.append(word)
            results.append([i/1000, floats])
            totalResults.append([i/1000, floats])
        f = open(tmpdir + 'results.txt', 'w')
        for result in results:
            f.write(str(result) + '\n')
    f = open(tmpdir + 'gr.log', 'w')
    for line in results:
        print(line[0], line[1][0], line[1][1], line[1][2])


#percolationConcentration()
crystRate()
