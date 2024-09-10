package collinear_points;  

import java.util.Arrays;   
import java.util.Scanner;  

public class CollinearPoints {  

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);  // Creating Scanner object for user input

        int a[], b[], c[], i, j, k = 0, n;

        // Creating the sets as arrays and sorting them in ascending order
        System.out.print("Specify the size for set A: ");
        n = scan.nextInt();
        a = new int[n];

        System.out.println("Enter the numbers of set A: ");
        for (i = 0; i < n; i++) {
            System.out.print("No. " + (i + 1) + ": ");
            int x = scan.nextInt();
            a[i] = x;
        }

        Arrays.sort(a);

        System.out.print("\nSpecify the size for set B: ");
        n = scan.nextInt();  
        b = new int[n];  
        System.out.println("Enter the numbers of set B: ");
        for (i = 0; i < n; i++) {
            System.out.print("No. " + (i + 1) + ": ");
            int x = scan.nextInt();  
            b[i] = x;  
        }

        Arrays.sort(b);  

        System.out.print("\nSpecify the size for set C: ");
        n = scan.nextInt();  
        c = new int[n];  
        System.out.println("Enter the numbers of set C: ");
        for (i = 0; i < n; i++) {
            System.out.print("No. " + (i + 1) + ": ");
            int x = scan.nextInt();  
            c[i] = x;  
        }

        Arrays.sort(c);  

        // Display sorted sets A, B, and C
        System.out.println("\nSet A: " + Arrays.toString(a));
        System.out.println("Set B: " + Arrays.toString(b));
        System.out.println("Set C: " + Arrays.toString(c));

        // Creating set D by doubling the values of set B
        int d[] = new int[b.length];
        for (i = 0; i < b.length; i++) {
            d[i] = 2 * b[i];
        }
        Arrays.sort(d);

        System.out.println("\nSet D: " + Arrays.toString(d));

        // Creating set E by adding elements of set A and set C pairwise
        int e[] = new int[a.length * c.length];  // Initialize array for set E with size A.length * C.length
        for (i = 0; i < a.length; i++) {
            for (j = 0; j < c.length; j++) {
                e[k] = a[i] + c[j];
                k++; 
            }
        }
        Arrays.sort(e);

        System.out.println("Set E: " + Arrays.toString(e));

        j = 0; 
        k = 0;

        // If either set D or set E is empty, no collinear points exist
        if (e.length == 0 || d.length == 0) {
            System.out.println("\nThere are NO collinear points");
            return;
        }

        // Comparing sets D and E to check for collinear points
        while (j < d.length && k < e.length) {
            if (d[j] == e[k]) {  // If a common element is found, collinear points exist
                System.out.println("\nThere are collinear points.");
                break;  // Break the loop once collinear points are found
            }
            if (d[j] < e[k]) {  // If element in D is smaller, increment j to check next
                j++;
                continue;
            }
            if (d[j] > e[k]) {  // If element in E is smaller, increment k to check next
                k++;
                continue;
            }
        }

        // If loop exits without finding any common elements, no collinear points exist
        if (j == d.length || k == e.length)
            System.out.println("\nThere are NO collinear points");
    }
}
