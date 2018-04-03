#!/usr/bin/env python3
#coding=utf-8


import copy
import math
import os
import subprocess
import resource

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

REPEATS = 1
CONC_RUNS = 100
STEP = 1000


exf_opts = {
            'CUBE_EDGE_LENGTH': 10.0,
            'MAX_ATTEMPTS': 1000000.0,
            'VERTICES_NUMBER': 8.0,
            'THICKNESS': 0.05,
            'OUTER_RADIUS': 1,
            'SHELL_THICKNESS': 1.0
}


# for gen_mesh.x, processMesh.x and FEM3.x to work:
os.environ['LD_LIBRARY_PATH'] =\
    '/home/anton/FEMFolder3/libs:/home/anton/FEMFolder3/my_libs'

class volReader():
    def __init__(self, fname):
        self.__fname = fname
        self.__pointsStartStringNum = None
        self.__pointsNum = None
        self.__volumesStartStringNum = None
        self.__volumesNum = None
        self.__volumeVertices = []
        self.__volumes = [0, 0, 0, 0] # all, filler, interface, matrix
        self.__phases = []
        self.__points = []
        with open(self.__fname, 'r') as f:
            for i, line in enumerate(f):
                if line.startswith('volumeelements'):
                    self.__volumesStartStringNum = i + 2
                elif line.startswith('points'):
                    self.__pointsStartStringNum = i + 2
                if self.__volumesStartStringNum is not None:
                    if i == self.__volumesStartStringNum - 1:
                        self.__volumesNum = int(line.split()[0])
                if self.__pointsStartStringNum is not None:
                    if i == self.__pointsStartStringNum - 1:
                        self.__pointsNum = int(line.split()[0])

    def readPoints(self):
        with open(self.__fname, 'r') as f:
            for i, line in enumerate(f):
                if self.__pointsStartStringNum is None:
                    continue
                if (i >= self.__pointsStartStringNum and
                    i < self.__pointsStartStringNum + self.__pointsNum):
                    self.__points.append([float(line.split()[0]),
                                          float(line.split()[1]),
                                          float(line.split()[2])])

    def readVolumes(self):
        with open(self.__fname, 'r') as f:
            for i, line in enumerate(f):
                if self.__volumesStartStringNum is None:
                    continue
                if (i >= self.__volumesStartStringNum and
                    i < self.__volumesStartStringNum + self.__volumesNum):
                    self.__volumeVertices.append([int(line.split()[2]),
                                                  int(line.split()[3]),
                                                  int(line.split()[4]),
                                                  int(line.split()[5])])
                    self.__phases.append(int(line.split()[0]))

    def calculateVolumeFractions(self):
        for i, vertices in enumerate(self.__volumeVertices):
            (a11, a12, a13) = (self.__points[vertices[3] - 1][0] - self.__points[vertices[0] - 1][0],
                               self.__points[vertices[3] - 1][1] - self.__points[vertices[0] - 1][1],
                               self.__points[vertices[3] - 1][2] - self.__points[vertices[0] - 1][2])
            (a21, a22, a23) = (self.__points[vertices[3] - 1][0] - self.__points[vertices[1] - 1][0],
                               self.__points[vertices[3] - 1][1] - self.__points[vertices[1] - 1][1],
                               self.__points[vertices[3] - 1][2] - self.__points[vertices[1] - 1][2])
            (a31, a32, a33) = (self.__points[vertices[3] - 1][0] - self.__points[vertices[2] - 1][0],
                               self.__points[vertices[3] - 1][1] - self.__points[vertices[2] - 1][1],
                               self.__points[vertices[3] - 1][2] - self.__points[vertices[2] - 1][2])
            volume = det(a11, a12, a13,
                         a21, a22, a23,
                         a31, a32, a33) / 6
            self.__volumes[0] += abs(volume)
            self.__volumes[self.__phases[i]] += abs(volume)

    def points(self):
        return self.__points

    def volumes(self):
        return self.__volumes


def crystRate():
    results = []
    totalResults = []
    genMeshExe = '/home/anton/FEMFolder3/gen_mesh.x'
    volfolder = '/home/anton/FEMFolder3/'
    geofolder = '/home/anton/Projects/CppPolygons/geofiles'
    tmpfolder = '/home/anton/Projects/CppPolygons/tmp'
    h = exf_opts['THICKNESS']
    n = exf_opts['VERTICES_NUMBER']
    r = exf_opts['OUTER_RADIUS'] * math.cos(math.pi / n)
    sh = exf_opts['SHELL_THICKNESS']
    l = exf_opts['CUBE_EDGE_LENGTH']
    diskVolume = math.pi * r ** 2 * h
    AR = int(2 * r / h)
    print('AR = ', 2 * r / h)
    tmpfolder += str(AR) + '/'
    geofolder += str(AR) + '/'
    subprocess.call(['mkdir', '-p', tmpfolder[:-1:]])
    subprocess.call(['mkdir', '-p', geofolder[:-1:]])
    results = []


    # define concentration as i/10
    for i in range(1, 25):
        s = ''
        print(i)
        subprocess.call(['mkdir', '-p', tmpfolder[:-1:] + '/' + str(i)])
        out_p = open(tmpfolder + '/' + str(i) + '/' + 'out_poly.log', 'w')
        out_g = open(tmpfolder + '/' + str(i) + '/' + 'out_genmesh.log', 'w')
        out_i = open(tmpfolder + '/' + str(i) + '/' + 'out_int_an.log', 'w')
        s += str(i/10) + ' '
        fillerVolume = i / 1000 * l**3
        particlesNumber = fillerVolume // diskVolume
        for r in range(REPEATS):
            ave_vols = [0, 0, 0]
            fopt = open('tmp/options.ini', 'w')
            for key, val in exf_opts.items():
                fopt.write(key + ' ' + str(val) + '\n')
            fopt.write('DISKS_NUM ' + str(particlesNumber) + '\n')
            geofname = geofolder + str(i/100) + '.geo'
            fopt.write('FNAME ' + geofname + '\n')
            fopt.close()
            subprocess.call(['./polygonal',], stdout=out_p)

            resource.setrlimit(resource.RLIMIT_CPU, (100, 100))
            subprocess.call([genMeshExe, geofname, '1', '3', '3'], stdout=out_g)
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (resource.RLIM_INFINITY, resource.RLIM_INFINITY)
            )
            volfname = 'generated.vol'
            vols = analyzeVol(volfname)
            flag = ifPercolate()
            s += str(flag) + ' '
            ave_vols[0] += vols[1] / vols[0]
            ave_vols[1] += vols[2] / vols[0]
            ave_vols[2] += vols[3] / vols[0]
            ave_vols[0] /= REPEATS
            ave_vols[1] /= REPEATS
            ave_vols[2] /= REPEATS
        s += str(ave_vols[0]) +  ' ' + str(ave_vols[1]) + ' ' + str(ave_vols[2])
        results.append(s)
    print('DesConc   PercFlag   VolFil   VolInt   VolMat')
    for s in results:
        print(s)


def det(a11, a12, a13, a21, a22, a23, a31, a32, a33):
    """
          | a11 a12 a13 |
    det = | a21 a22 a23 |
          | a31 a32 a33 |
    """
    m11 = a22 * a33 - a32 * a23
    m12 = a21 * a33 - a31 * a23
    m13 = a21 * a32 - a31 * a22
    d = a11 * m11 - a12 * m12 + a13 * m13
    return float(d)

def ifPercolate():
    ints = []
    minmaxes = []
    chains = []
    percFlag = 0
  # reading numbers of intersecting cylinders
    with open('tmp/intersections.log') as f:
        for line in f:
            ints.append([int(line.split()[0]), int(line.split()[1])]);
  # reading bbox coordinates of cylinders to find if there is percolation
    with open('tmp/coords.log') as f:
        for line in f:
            minmaxes.append(line.split())
    for i in range(len(minmaxes)):
        for j in range(len(minmaxes[i])):
            minmaxes[i][j] = float(minmaxes[i][j])
  # reading cube size from options file
    with open('tmp/options.ini') as f:
        for line in f:
            if line.startswith('CUBE_EDGE_LENGTH'):
                cubeSize = float(line.split()[1])
    for intersection in ints:
        flag1 = False
        flag2 = False
        for chain in chains:
            if intersection[0] in chain:
                chain.update([intersection[1],])
                flag1 = True
            if intersection[1] in chain:
                chain.update([intersection[0],])
                flag2 = True
        if not flag1 and not flag2:
            chains.append(set(intersection))
    chain_minmaxes = [[cubeSize, 0, cubeSize, 0, cubeSize, 0]
                          for i in range(len(chains))]

    for i, chain in enumerate(chains):
        minmax = [cubeSize, 0, cubeSize, 0, cubeSize, 0]
        for pc in chain:
            if minmaxes[pc][0] < minmax[0]:
                minmax[0] = minmaxes[pc][0]
            if minmaxes[pc][1] > minmax[1]:
                minmax[1] = minmaxes[pc][1]
            if minmaxes[pc][2] < minmax[2]:
                minmax[2] = minmaxes[pc][2]
            if minmaxes[pc][3] > minmax[3]:
                minmax[3] = minmaxes[pc][3]
            if minmaxes[pc][4] < minmax[4]:
                minmax[4] = minmaxes[pc][4]
            if minmaxes[pc][5] > minmax[5]:
                minmax[5] = minmaxes[pc][5]
        chain_minmaxes[i] = minmax
    for i, chain in enumerate(chains):
        flagx = flagy = flagz = False
        if chain_minmaxes[i][1] - chain_minmaxes[i][0] > cubeSize:
            flagx = True
        if chain_minmaxes[i][3] - chain_minmaxes[i][2] > cubeSize:
            flagy = True
        if chain_minmaxes[i][5] - chain_minmaxes[i][4] > cubeSize:
            flagz = True
        if True in (flagx, flagy, flagz):
            percFlag += 1
    return percFlag


def analyzeVol(fname):
    a = volReader(fname)
    a.readPoints()
    a.readVolumes()
    a.calculateVolumeFractions()
    vols = a.volumes()
    return vols


crystRate()
