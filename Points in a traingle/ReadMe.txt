This program is designed to determine whether a given point lies inside, on the edge of, or outside a triangle. It consists of four main classes:

Main: The main class that drives the program logic.
GUI: Responsible for drawing the triangle and the point on a graphical interface.
Triangle: Represents the triangle with three vertices.
Point: Represents a 2D point with x and y coordinates.

The logic behind finding whether a point is inside a triangle relies on computing the determinants of the matrices formed by the triangle's vertices and the point in question. By checking the signs of these determinants, we can tell if the point is inside, on the edge, or outside the triangle.
The program calculates the determinant for three points to understand the position of the point relative to the triangle's edges. Positive determinants indicate that the point is inside, zero indicates it's on the edge, and a negative determinant means it's outside.

Breakdown of Each Class:
1. Point.java
This class defines a 2D point with x and y coordinates. It includes a constructor and getter methods for x and y.

2. Triangle.java
This class represents a triangle, where each vertex is an instance of the Point class. The constructor accepts input from the user to define the three vertices. It also provides getter methods to access these points.

3. GUI.java
This class uses Java's Graphics library to draw the triangle and the point on a panel. It also draws labels for the vertices of the triangle and colors the points accordingly.

4. Main.java
This is the main logic that takes input for the point M and determines its position relative to the triangle by computing determinants.
