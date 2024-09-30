package point_in_triangle;

import java.lang.Math;
import java.util.Scanner;

public class Main {

	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		double x,y;
		
		// Create the triangle using user input
		Triangle t = new Triangle();
		
		while(determinant(t.getA(),t.getB(),t.getC()) == 0) {
			System.out.println("Point are coolinear, therefore cannot form a triangle.\n"); // Loop until valid triangle
			t = new Triangle();
		}
		
		// Input for the point M
		System.out.print("Enter the coordinates for point M:\nx = ");
		x = scan.nextFloat();
		System.out.print("y = ");
		y = scan.nextFloat();
			
		Point m = new Point(x,y);
		
		// Check if point M is one of the vertices of the triangle
		if(m.getX() == t.getA().getX() && m.getY() == t.getA().getY()) { System.out.println("Point M is actually point A on the triangle."); }
		if(m.getX() == t.getB().getX() && m.getY() == t.getB().getY()) { System.out.println("Point M is actually point B on the triangle."); }
		if(m.getX() == t.getC().getX() && m.getY() == t.getC().getY()) { System.out.println("Point M is actually point C on the triangle."); }
			
		// Calculate determinants to determine if the point is inside, on the edge, or outside
		if(determinant(t.getA(),t.getB(),t.getC()) < 0) {
			int d1 = determinant(m,t.getA(),t.getC());
			int d2 = determinant(m,t.getC(),t.getB());
			int d3 = determinant(m,t.getB(),t.getA());
			if(d1 > 0 && d2 > 0 && d3 > 0) {
				System.out.println("Point M is inside the triangle.");
			}
			else if (d1 == 0 || d2 == 0 || d3 == 0) {
				System.out.println("Point M is on one of the sides of the triangle");
			}
			else System.out.println("Point M is outside the triangle");
		}
		else {
			int d1 = determinant(m,t.getA(),t.getB());
			int d2 = determinant(m,t.getB(),t.getC());
			int d3 = determinant(m,t.getC(),t.getA());
			if(d1 > 0 && d2 > 0 && d3 > 0) {
				System.out.println("Point M is inside the triangle.");
			}
			else if (d1 == 0 || d2 == 0 || d3 == 0) {
				System.out.println("Point M is on one of the sides of the triangle");
			}
			else System.out.println("Point M is outside the triangle");
		}
		GUI g = new GUI(t,m); // Draw the triangle and the point
	}
	
	// Method to compute the determinant of three points (a, b, c)
	private static int determinant (Point a, Point b, Point c) {
		int d;
		
		d = (int) Math.floor(a.getX() * b.getY() + b.getX() * c.getY() + c.getX() * a.getY() - b.getY() * c.getX() - c.getY() * a.getX() - a.getY() * b.getX());
		
		return d;
	}

}
