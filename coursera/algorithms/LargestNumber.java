import java.util.*;

public class LargestNumber {
    private static String largestNumber(String[] a) {
        
        Arrays.sort(a, new Comparator<String>() {
            @Override
            public int compare(String o1, String o2) {
               Integer opt1 = Integer.valueOf(o1+o2);
               Integer opt2 = Integer.valueOf(o2+o1);
               return opt2.compareTo(opt1);
            }
        });
        /*System.err.println("After sorting");
        for (int i = 0; i < a.length; i++) {
            System.err.println(a[i]);
        }*/
        //write your code here
        String result = "";
        for (int i = 0; i < a.length; i++) {
            result += a[i];
        }
        return result;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        String[] a = new String[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.next();
        }
        System.out.println(largestNumber(a));
    }
}

