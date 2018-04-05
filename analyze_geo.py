#!/usr/bin/env python3


import math

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


def analyze_particles(tau=None, N=None, attempt=None, n=None):
    folder = '/home/anton/FEMFolder3/results_archive/'
    folder += 'Отчёт - результаты/geofiles/tau'
    if None in [tau, N, attempt, n]:
        tau = '1.5'
        attempt = 0
        N = 4
        n = 6
    fname = folder + tau + 'N' + str(N) + '_' + str(attempt) + '.geo'
    # Actions
    f = open(fname, 'r')
    particles = []
    filler_h = 0
    filler_edge = 0
    filler_r = 0
    shell_h = 0
    shell_edge = 0
    shell_r = 0
    counter = 0
    flag_filler = False
    flag_shell = False
    shells = []
    fillers = []
    planes = []
    for line in f:
        if counter == 8:
            if flag_filler:
                fillers.append(planes)
                flag_filler = False
            else:
                shells.append(planes)
                flag_shell = False
            counter = 0
            planes = []
        if line.startswith('algebraic'):
            continue
        if line.startswith('solid ce'):
            continue
        if line.startswith('solid po'):
            flag_filler = True
            counter = 0
            continue
        if line.startswith('solid pc'):
            flag_shell = True
            counter = 0
            continue
        if flag_filler and counter < n + 2:
            counter += 1
            ls = line.split('plane(')[1].split(';')[0].split(', ');
            point = [float(ls[0]), float(ls[1]), float(ls[2])]
            planes.append(point)
        if flag_shell and counter < n + 2:
            counter += 1
            ls = line.split('plane(')[1].split(';')[0].split(', ');
            point = [float(ls[0]), float(ls[1]), float(ls[2])]
            planes.append(point)
    for filler in fillers:
        top = filler[0]
        bot = filler[1]
        filler_h += ((top[0] - bot[0])**2 +
                     (top[1] - bot[1])**2 +
                     (top[2] - bot[2])**2)**0.5
        filler.pop(1)
        filler.pop(0)
        centerx = 0
        centery = 0
        centerz = 0
        for i in range(n):
            pt1 = filler[i]
            pt2 = filler[i - 1]
            filler_edge += ((pt2[0] - pt1[0])**2 +
                            (pt2[1] - pt1[1])**2 +
                            (pt2[2] - pt1[2])**2)**0.5
    for shell in shells:
        top = shell[0]
        bot = shell[1]
        shell_h += ((top[0] - bot[0])**2 +
                    (top[1] - bot[1])**2 +
                    (top[2] - bot[2])**2)**0.5
        shell.pop(1)
        shell.pop(0)
        for i in range(n):
            pt1 = shell[i]
            pt2 = shell[i - 1]
            shell_edge += ((pt2[0] - pt1[0])**2 +
                           (pt2[1] - pt1[1])**2 +
                           (pt2[2] - pt1[2])**2)**0.5
    filler_h /= N
    shell_h /= N
    filler_edge /= 2 * N * n
    shell_edge /= 2 * N * n
    central_angle_half = math.pi / (2 * n)
    filler_R = filler_edge / (2 * math.sin(central_angle_half)) # inner r
    shell_R = shell_edge / (2 * math.sin(central_angle_half))   # inner r
    outer_filler_R = filler_R / math.cos(central_angle_half)  # outer r
    outer_shell_R = shell_R / math.cos(central_angle_half)    # outer r
    return (outer_filler_R / filler_h * 2, outer_shell_R / shell_h * 2)


def main():
    # configuring
    n = 6    # VERTICES_NUMBER in CppPolygons/options.ini
    # running
    ave_filler_AR = 0
    for tau in ['1.5', '2.5', '5']:
        ave_shell_AR = 0
        for N in [4, 8, 12, 16, 20, 24, 28, 30]:
            for attempt in range(5):
                ARs = analyze_particles(tau, N, attempt, n)
                ave_shell_AR += ARs[1]
                ave_filler_AR += ARs[0]
        print('tau = ', ' ' * abs(3 - len(tau)) + tau + ';', 'shell AR =', ave_shell_AR / 40)
    print('Filler AR =', ave_filler_AR / 120) 


main()
