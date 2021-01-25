import pygame

import Core.geo
import Core.tools


def _superTriangle(points):
    __boundingRect = Core.geo.polygonBoundingRect(points)

    __boundingRect.x -= 100
    __boundingRect.y -= 100
    __boundingRect.w += 200
    __boundingRect.h += 200

    __side1 = Core.geo.lineFromPointSlope(__boundingRect.topleft, -1)
    __side2 = Core.geo.lineFromPointSlope(__boundingRect.topright, 1)

    __side3 = Core.geo.seg_toLine(Core.geo.makeSegment(__boundingRect.bottomright, __boundingRect.bottomleft))
    return Core.geo.line_intersection(__side1, __side2), Core.geo.line_intersection(__side2, __side3), \
           Core.geo.line_intersection(__side3, __side1)


def _cleanSuperTriangle(triangles, superTriangle):
    __i = 0
    __len = len(triangles)
    while __i < __len:
        __triangle = triangles[__i]
        for __point in __triangle:
            if __point in superTriangle:
                del triangles[__i]
                __i -= 1
                __len -= 1
                break
        __i += 1


"""
https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
function BowyerWatson (pointList)
   // pointList is a set of coordinates defining the points to be triangulated
   triangulation := empty triangle mesh data structure
   add super-triangle to triangulation // must be large enough to completely contain all the points in pointList
   for each point in pointList do // add all the points one at a time to the triangulation
      badTriangles := empty set
      for each triangle in triangulation do // first find all the triangles that are no longer valid due to the insertion
         if point is inside circumcircle of triangle
            add triangle to badTriangles
      polygon := empty set
      for each triangle in badTriangles do // find the boundary of the polygonal hole
         for each edge in triangle do
            if edge is not shared by any other triangles in badTriangles
               add edge to polygon
      for each triangle in badTriangles do // remove them from the data structure
         remove triangle from triangulation
      for each edge in polygon do // re-triangulate the polygonal hole
         newTri := form a triangle from edge to point
         add newTri to triangulation
   for each triangle in triangulation // done inserting points, now clean up
      if triangle contains a vertex from original super-triangle
         remove triangle from triangulation
   return triangulation
   """

"""
I think there is a way to make the function runs faster.
1. create a dict that indicate the another 2 point of a point to build a triangle
2.Sort the points in x and y. 3.Insert the points in the heap and find the where the new point would be in the heap.
4.Use the 2 index to find the first bad triangle.  5. Bad triangles shares edges use the first bad 
triangle to find other triangles
I might implicate it on the module that contains the function that is related to graph (data structure) because 
its faster to gives a graph rather than triangles when you use the step above to create a function.
"""


def updateTriangulation(triangles: list, newPoint):
    __badTriangles = list()
    for __triangle in triangles:
        __circle = Core.geo.triangleCircumcircle(*__triangle)
        if Core.geo.circleContains(__circle, newPoint):
            __badTriangles.append(__triangle)

    __newTriangleEdges = Core.geo.polygonUnsharedSides(__badTriangles)
    for __triangle in __badTriangles:
        triangles.remove(__triangle)
    for __edge in __newTriangleEdges:
        triangles.append((__edge[0], __edge[1], newPoint))


def triangulate(points: list):
    """
    :param points:
    :type pointsSortedByXY: typing.Tuple[list,list]
    :return:
    """

    __superTriangle = _superTriangle(points)

    __triangles = [__superTriangle]
    __points = list(__superTriangle)
    for __i in points:
        updateTriangulation(__triangles, __i)
    _cleanSuperTriangle(__triangles, __superTriangle)
    return __triangles
def buildGraph(points,):
    pass
#
# def pointLinkages(triangles: list):
#     __linkages = {}
#     for __triangle in triangles:
#         for __i in (0, 1, 2):
#             if __triangle[__i] in __linkages:
#                 __linkages[__i].update((__triangle[__i - 1], __triangle[__i - 1]))
#             else:
#                 __linkages.update({__i: {__triangle[__i - 1], __triangle[__i - 1]}})
#     return __linkages
