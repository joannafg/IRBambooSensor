import java.io.*;
import java.util.*;

public class MyClass { 
 public static void main(String args[]) {
                readFile();
                
		        
	}

	private static void writeFile(List<String> inputArray, String nameOfFile) {
	    String fileName = "/myfiles/" +nameOfFile+ ".txt";
	        try {
	
	            BufferedWriter bufferedWriter =
	                new BufferedWriter(new FileWriter(fileName));
	
	            for (int i = 0; i < inputArray.size(); i++) {
	                bufferedWriter.write(inputArray.get(i)); 
	                bufferedWriter.newLine();
	                
	            }
	
	            bufferedWriter.close();
	        }
	        catch(IOException ex) {
	            System.out.println("Error writing....");
	            ex.printStackTrace();
	        }
	}
	
	
	private static void readFile() {
	     String txt = null;
	     List<String> meanRaw = new ArrayList<String>();
	     List<String> methodOne = new ArrayList<String>();
	     List<String> methodTwo = new ArrayList<String>();
	     List<String> methodThree = new ArrayList<String>();
	     List<String> methodFour = new ArrayList<String>();
	
	        try {
	            
	            BufferedReader bufferedReader = 
	                new BufferedReader(new FileReader("/uploads/4_20_6_38pm.txt"));
	
	            while((txt = bufferedReader.readLine()) != null) {
	               // System.out.println(txt.substring(25, 33));
	                meanRaw.add(txt.substring(25, 33)); 
	                txt = bufferedReader.readLine(); 
	               // System.out.println(txt.substring(27, 33));
	               methodOne.add(txt.substring(27, 33));
	                txt = bufferedReader.readLine(); 
	               // System.out.println(txt.substring(27, 33));
	               methodTwo.add(txt.substring(27, 33));
	                txt = bufferedReader.readLine(); 
	               // System.out.println(txt.substring(29, 32)); 
	               methodThree.add(txt.substring(29, 32));
	                txt = bufferedReader.readLine(); 
	               // System.out.println(txt.substring(28, 34));
	               methodFour.add(txt.substring(28, 34));
	            }   
	
	            bufferedReader.close();         
	        }
	        catch(FileNotFoundException ex) {
	            System.out.println("Unable to read...");                
	        }
	        catch(IOException ex) {
	            System.out.println("Unable to read...");
	        }
	    writeFile(meanRaw, "meanRaw");
	    writeFile(methodOne, "methodOne");
	    writeFile(methodTwo, "methodTwo");
	    writeFile(methodThree, "methodThree");
	    writeFile(methodFour, "methodFour");
	}
}