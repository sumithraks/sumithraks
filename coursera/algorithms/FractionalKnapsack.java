import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class FractionalKnapsack {
    
    public static class Item {
        int index;
        int totalValue;
        int weight;
        Double valuePerUnit;
    }
    
    private static double getOptimalValue(int capacity, ArrayList<Item> items) {
        double value = 0;
        //write your code here
        Collections.sort(items, (Item o1, Item o2) -> o2.valuePerUnit.compareTo(o1.valuePerUnit));
        int currentCapacity = capacity;
        int itemIndex=0;
        do {
            if (currentCapacity - items.get(itemIndex).weight >= 0) {
                value = value + items.get(itemIndex).weight*items.get(itemIndex).valuePerUnit;
                currentCapacity=currentCapacity-items.get(itemIndex).weight;
                itemIndex++;
            } else {
                value = value + items.get(itemIndex).valuePerUnit*currentCapacity;
                currentCapacity=0;
            }
            if (itemIndex >= items.size()) break;
        }while (currentCapacity!=0);
        return value;
    }

    public static void main(String args[]) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int capacity = scanner.nextInt();
        ArrayList<Item> items = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            Item a = new Item();
            a.index=i;
            a.totalValue=scanner.nextInt();
            a.weight=scanner.nextInt();
            a.valuePerUnit=((double)a.totalValue/(double)a.weight);
            items.add(a);
        }
        System.out.println(getOptimalValue(capacity, items));
    }
} 

