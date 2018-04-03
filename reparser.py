#!/usr/bin/env python3

import sys

from mypymath.geometry.figures import PolygonRegular
from mypymath.geometry.functions import DistanceCalculator
from geo_reader import GeoReader
from regular_prism_from_geo_planes import RegularPrismFeomGeoPlanes


def reparse():
    """
    Reads geofile and outputs something that is easy to read with cpp code.
    """
    taus = [1.5, 2.5, 5]
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]

    for tau in taus:
        for N in Ns:
            for attempt in range(5):
                fname = 'Structures/tau' + str(tau) + 'N' + str(N) + '_' + str(attempt) + '.geo'
                fout = 'Reparsed/tau' + str(tau) + 'N' + str(N) + '_' + str(attempt) + '.geo'
                reader = GeoReader(fname)
                reader.read_polygonal_cylinders_raw()
                shells = reader.shells
                shell_prisms = []
                f = open(fout, 'w')
                for shell in shells:
                    shell_prism = RegularPrismFeomGeoPlanes(shell).prism_regular
                    shell_prisms.append(shell_prism)
                    top = shell_prism.top_facet
                    bottom = shell_prism.bottom_facet
                    for pt in top.vertices:
                        s = 'top ' + str(pt.x) + ' ' + str(pt.y) + ' ' + str(pt.z) + '\n'
                        f.write(s)
                    for pt in bottom.vertices:
                        s = 'bottom ' + str(pt.x) + ' ' + str(pt.y) + ' ' + str(pt.z) + '\n'
                        f.write(s)
                    top_poly = PolygonRegular(top.vertices)
                    bot_poly = PolygonRegular(bottom.vertices)
                dc = DistanceCalculator()

reparse()
