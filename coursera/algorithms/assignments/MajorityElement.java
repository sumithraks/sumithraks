import java.util.*;
import java.io.*;

public class MajorityElement {
   
    private static long getMajorityElement(long[] a, int left, int right) {
        if (left == right) {
            System.err.println("Left "+left+" Right "+right+" Returning "+a[left]);
            return -1;
        }

        int mid = left+(right-left)/2;
        System.err.println("Left "+left+" Right "+right+" mid "+mid);
        
        
        long leftReturn = getMajorityElement(a,left,mid);
        long rightReturn = getMajorityElement(a,mid+1,right);
        System.err.println("After recursion: left mjority " + leftReturn+ " Right majority "+rightReturn);
        {
            System.out.println("Counting left and right majoirty. left "+left+" right "+right);
            if (leftReturn!=-1 && (right-left)>1) {
                int count=0;
                for (int i=left; i <=right;i++) {
                    if (a[i]==leftReturn) {
                        count++;
                    }
                    if (count > Math.ceil((right-left)/2) ) {
                        System.err.println("Returning left majority"+leftReturn);
                        return leftReturn;
                    }
                }
            }
            if (rightReturn!=-1 && (right-left)>1) {
                int count=0;
                for (int i=left; i <=right;i++) {
                    if (a[i]==rightReturn) {
                        count++;
                    }
                    if (count > Math.ceil((right-left)/2)) {
                        System.err.println("Returning left majority"+leftReturn);
                        return rightReturn;
                    }
                }            
            }
        }
        //write your code here
        return -1;
    }
    
    public static void main(String[] args) {
        FastScanner scanner = new FastScanner(System.in);
        int n = scanner.nextInt();
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }
        long element = getMajorityElement(a, 0, a.length-1);
        System.err.println("---- ");
        System.err.println("Majority Element "+element);
        System.err.println("---- ");
        if ( element != -1) {
            System.out.println(1);
        } else {
            System.out.println(0);
        }
    }
    static class FastScanner {
        BufferedReader br;
        StringTokenizer st;

        FastScanner(InputStream stream) {
            try {
                br = new BufferedReader(new InputStreamReader(stream));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        String next() {
            while (st == null || !st.hasMoreTokens()) {
                try {
                    st = new StringTokenizer(br.readLine());
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return st.nextToken();
        }

        int nextInt() {
            return Integer.parseInt(next());
        }
    }
}

