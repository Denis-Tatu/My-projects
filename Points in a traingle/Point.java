package point_in_triangle;

public class Point {
	
	private double x,y;
	
	public Point(double x,double y) { // Constructor to initialize the point with x and y coordinates
		this.x = x;
		this.y = y;
	}
	
	public double getX() { // Getter for x coordinate
		return this.x;
	}
	
	public double getY() { // Getter for Y coordinate
		return this.y;
	}

}
