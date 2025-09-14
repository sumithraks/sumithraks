import java.util.*;
import java.io.*;

public class CarFueling {
    static int computeMinRefills(int dist, int tank, int[] stops) {
        int numFuels = 0;
        int refuelingPoint = 0;
        int travelled = 0;
        int currentStop=0;
        int currentFuel=tank;
        if (dist < tank) {
            return 0;
        }
        do {
            travelled=stops[currentStop];
            currentFuel=tank-(travelled-refuelingPoint);
            //System.out.println("Current stop "+stops[currentStop]+" "+currentFuel+" "+travelled+" "+refuelingPoint);
            if (currentFuel < 0)
            {
                return -1;
            }
            if (currentFuel == 0 || (currentStop+1 < stops.length && currentFuel<(stops[currentStop+1]-stops[currentStop]))||
                    (currentStop+1 >= stops.length && currentFuel< dist-stops[currentStop])) {
                numFuels++;
                refuelingPoint=stops[currentStop];
                //System.out.println("Refueling at "+stops[currentStop]);
            } 
            currentStop++;
        }while(travelled<dist && currentStop<stops.length);
        if (travelled<dist) {
            currentFuel=tank-(travelled-refuelingPoint);
            travelled+=currentFuel;
        }
        //System.out.println("Travelled "+travelled);
        if (travelled < dist) 
            return -1;
        return numFuels;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int dist = scanner.nextInt();
        int tank = scanner.nextInt();
        int n = scanner.nextInt();
        int stops[] = new int[n];
        for (int i = 0; i < n; i++) {
            stops[i] = scanner.nextInt();
        }

        System.out.println(computeMinRefills(dist, tank, stops));
    }
}

