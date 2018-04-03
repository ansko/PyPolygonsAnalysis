#!/usr/bin/env python3
#coding=utf-8


import sys


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


fname = sys.argv[1]
a = volReader(fname)
a.readPoints()
a.readVolumes()
a.calculateVolumeFractions()
vols = a.volumes()
string = (str(vols[1] / vols[0]) + ' ' +
          str(vols[2] / vols[0]) + ' ' +
          str(vols[3] / vols[0]))
print(string)
