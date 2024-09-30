package point_in_triangle;

import java.util.Scanner;

public class Triangle {
	
	private Point a,b,c;
	
	// Constructor that prompts the user for the coordinates of the triangle's vertices
	public Triangle() { 
		Scanner scan = new Scanner(System.in);
		int x,y;
		
		System.out.println("Enter the coordinates for the triangle:");
		
		// Input for Point A
		System.out.print("Point A:\nx = ");
		x = scan.nextInt();
		System.out.print("y = ");
		y = scan.nextInt();
		this.a = new Point(x,y);
		
		// Input for Point B
		System.out.print("Point B:\nx = ");
		x = scan.nextInt();
		System.out.print("y = ");
		y = scan.nextInt();
		this.b = new Point(x,y);
		
		// Input for Point C
		System.out.print("Point C:\nx = ");
		x = scan.nextInt();
		System.out.print("y = ");
		y = scan.nextInt();
		this.c = new Point(x,y);
	}
	
	public Point getA() { // Getter for Point A
		return this.a;
	}
	
	public Point getB() { // Getter for Point B
		return this.b;
	}
	
	public Point getC() { // Getter for Point C
		return this.c;
	}

}
