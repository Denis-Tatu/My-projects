package point_in_triangle;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;

import javax.swing.JFrame;
import javax.swing.JPanel;

//Constructor that initializes the GUI frame and sets up the drawing panel
public class GUI extends JPanel {
	private Triangle t;
	private Point m;
	
	public GUI(Triangle t, Point m) {
		this.t = t;
		this.m = m;
		
		JFrame root = new JFrame();
		root.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		root.setResizable(false);
		root.setLocationRelativeTo(null);
		
		this.setPreferredSize(new Dimension(750,750));
		root.add(this);
		root.pack();
		
		root.setVisible(true);
	}
	
	// Overridden Method to handle the actual drawing of the triangle and point
	public void paint(Graphics g) {
		Graphics2D g2D = (Graphics2D) g;
		
		// Draw the triangle using the vertices scaled by 100 for visibility
		g2D.setStroke(new BasicStroke(5));
		int[] xPoints = {(int) (this.t.getA().getX()* 100),(int) (this.t.getB().getX()* 100),(int) (this.t.getC().getX()* 100)};
		int[] yPoints = {(int) (this.t.getA().getY()* 100),(int) (this.t.getB().getY()* 100),(int) (this.t.getC().getY()* 100)};
		g2D.drawPolygon(xPoints,yPoints,3);
		
		// Draw vertices A, B, and C
		g2D.setStroke(new BasicStroke(10));
		g2D.setPaint(Color.blue);
		g2D.drawLine((int) this.t.getA().getX() * 100, (int) this.t.getA().getY() * 100, (int) this.t.getA().getX() * 100, (int) this.t.getA().getY() * 100);
		g2D.drawLine((int) this.t.getB().getX() * 100, (int) this.t.getB().getY() * 100, (int) this.t.getB().getX() * 100, (int) this.t.getB().getY() * 100);
		g2D.drawLine((int) this.t.getC().getX() * 100, (int) this.t.getC().getY() * 100, (int) this.t.getC().getX() * 100, (int) this.t.getC().getY() * 100);
		
		// Draw triangle labels
		g2D.setPaint(Color.magenta);
		g2D.setFont(new Font("Arial",Font.BOLD,25));
		g2D.drawString("A", (int) this.t.getA().getX() * 100, (int) this.t.getA().getY() * 100);
		g2D.drawString("B", (int) this.t.getB().getX() * 100, (int) this.t.getB().getY() * 100);
		g2D.drawString("C", (int) this.t.getC().getX() * 100, (int) this.t.getC().getY() * 100);
		
		// Draw point M
		g2D.setPaint(Color.red);
		g2D.drawLine((int) this.m.getX()*100, (int) this.m.getY()*100, (int) this.m.getX()*100, (int) this.m.getY()*100);
		g2D.drawString("M", (int) this.m.getX() * 100, (int) this.m.getY() * 100);
	}
}
