from points import Point2D, Point3D, Segment2D


def main():
    print("Z1")
    point2d = Point2D(3, 5)
    point2d.print()
    point2d.reset()
    point2d.print()
    print()

    print("Z2")
    point3d = Point3D(3, 5, 2)
    point3d.print()
    point3d.reset()
    point3d.print()
    print()

    print("Z3")
    a = Point2D(0, 0)
    b = Point2D(3, 4)
    ab = Segment2D(a, b)
    a.print()
    b.print()
    print(F"Length = {ab.length()}")
    print()


if __name__ == "__main__":
    main()
