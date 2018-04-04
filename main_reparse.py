#!/usr/bin/env python3


import sys

from options_parser import OptionsParser


def main_reparse():
    taus = ['1.5', '2.5', '5']
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    options = OptionsParser().options
    folder_geofiles = options['folder_geofiles']
    folder_reparsed = options['folder_reparsed']
    folder_mypymath = options['folder_mypymath']
    # imports
    sys.path.append(folder_mypymath)
    import mypymath
    from src.geo_reader import GeoReader
    from src.regular_prism_from_geo_planes import RegularPrismFromGeoPlanes
    # reparse .geo files
    for tau in taus:
        for N in Ns:
            for attempt in range(5):
                structure_name = '/tau' + tau + 'N' + str(N) + '_' + str(attempt)
                fname_geo = folder_geofiles + structure_name + '.geo'
                fin = open(fname_geo, 'r')
                fname_reparsed = folder_reparsed + structure_name
                fout = open(fname_reparsed, 'w')
                reader = GeoReader(fname_geo)
                reader.read_polygonal_cylinders_raw()
                shells = reader.shells
                shell_prisms = []
                for shell in shells:
                    shell_prism = RegularPrismFromGeoPlanes(shell).prism_regular
                    shell_prisms.append(shell_prism)
                    top = shell_prism.top_facet
                    bottom = shell_prism.bottom_facet
                    for pt in top.vertices:
                        fout.write('top ' +
                                   str(pt.x) + ' ' + 
                                   str(pt.y) + ' ' +
                                   str(pt.z) + '\n')
                    for pt in bottom.vertices:
                        fout.write('bottom ' +
                                   str(pt.x) + ' ' + 
                                   str(pt.y) + ' ' +
                                   str(pt.z) + '\n')


if __name__ == '__main__':
    main_reparse()
