from mypymath.linalg.matrix3 import Matrix3
from mypymath.geometry.figures import Point, PolygonRegular, PrismRegular


class RegularPrismFromGeoPlanes:
    """
    Produces a convertion from
      a regular prism made from planes and stored in .geo
    to
      PrismRegular that may be analyzed with mypymath module.
    """
    def __init__(self, planes):
        top = planes[0]
        bottom = planes[1]
        sides = planes[2:]
        top_poly_vertices = []
        bottom_poly_vertices = []
        for i in range(len(sides)):
            # find intersection of side[i], side[i-1] and top and
            #      intersection of side[i],  side[i-1] and bottom
            side_one = sides[i]
            side_two = sides[i - 1]
            # with top:
            det_system_matrix = Matrix3([side_one.a, side_one.b, side_one.c,
                                         side_two.a, side_two.b, side_two.c,
                                         top.a, top.b, top.c]).det()
            det_pt_x_matrix = Matrix3([-side_one.d, side_one.b, side_one.c,
                                       -side_two.d, side_two.b, side_two.c,
                                       -top.d, top.b, top.c]).det()
            det_pt_y_matrix = Matrix3([side_one.a, -side_one.d, side_one.c,
                                       side_two.a, -side_two.d, side_two.c,
                                       top.a, -top.d, top.c]).det()
            det_pt_z_matrix = Matrix3([side_one.a, side_one.b, -side_one.d,
                                       side_two.a, side_two.b, -side_two.d,
                                       top.a, top.b, -top.d]).det()
            if det_system_matrix == 0:
                print('Error in RegularPrismFromGeoPlanes:',
                      'det is null')
                return None
            pt_top = Point(det_pt_x_matrix / det_system_matrix,
                           det_pt_y_matrix / det_system_matrix,
                           det_pt_z_matrix / det_system_matrix)
            # with bottom:
            det_system_matrix = Matrix3([side_one.a, side_one.b, side_one.c,
                                         side_two.a, side_two.b, side_two.c,
                                         bottom.a, bottom.b, bottom.c]).det()
            det_pt_x_matrix = Matrix3([-side_one.d, side_one.b, side_one.c,
                                       -side_two.d, side_two.b, side_two.c,
                                       -bottom.d, bottom.b, bottom.c]).det()
            det_pt_y_matrix = Matrix3([side_one.a, -side_one.d, side_one.c,
                                       side_two.a, -side_two.d, side_two.c,
                                       bottom.a, -bottom.d, bottom.c]).det()
            det_pt_z_matrix = Matrix3([side_one.a, side_one.b, -side_one.d,
                                       side_two.a, side_two.b, -side_two.d,
                                       bottom.a, bottom.b, -bottom.d]).det()
            if det_system_matrix == 0:
                print('Error in RegularPrismFromGeoPlanes:',
                      'det is null')
                return None
            pt_bottom = Point(det_pt_x_matrix / det_system_matrix,
                              det_pt_y_matrix / det_system_matrix,
                              det_pt_z_matrix / det_system_matrix)
            top_poly_vertices.append(pt_top)
            bottom_poly_vertices.append(pt_bottom)
        top_facet = PolygonRegular(top_poly_vertices)
        bottom_facet = PolygonRegular(bottom_poly_vertices)
        self.prism_regular = PrismRegular(top_facet, bottom_facet)
