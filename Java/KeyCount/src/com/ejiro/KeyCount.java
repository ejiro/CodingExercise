package com.ejiro;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

/**
 * Write a function that sums up keys in a text file. The file contains data in
 * the format of "key,count" where key is a string and count is an integer. 
 * Each line will only contain one key-count pair. The output should contain 
 * each key occurring in the file along with the sum of the count for all 
 * occurrences of a given key.
 * 
 * For Example Input:
 * John,2
 * Jane,3
 * John,4
 * Jane,5
 * 
 * Would result in the output: 
 * "The total for John is 6. The total for Jane is 8."
 * 
 * @author Ejiro
 *
 */
public class KeyCount {

	public static void main(String[] args) {
		//get the input file from command line
		File file = null;
		if (args.length > 0) {
			String filename = args[0];
			file = new File(filename);
		}else{
			System.err.println("Invalid command line, exactly one argument required");
			System.err.println("cd into the KeyCount folder and Try:\n$java -cp ./bin com/ejiro/KeyCount input-file.txt");
			System.exit(1);
		}
		
		//sums up keys in a text file
		KeyCount.sumsUpKeys(file);
	}
	
	/**
	 * A function that sums up keys in a text file.
	 * @param file
	 */
	private static void sumsUpKeys(File file){
		BufferedReader br = null;
		try{
			//try to get a buffer reader to the file
			br = new BufferedReader(new FileReader(file));
			
			//use a map to hold the key-total count pair
			Map<String, Integer> outMap = new HashMap<String, Integer>();
			
			// process each line from the input file
			for(String line; (line = br.readLine()) != null; ) {
				String[] data = line.split(",");
				// sanity check, making sure the input format is 
				// valid key-count pair
				if(data.length == 2){
					String key = data[0]; //key
					int count = Integer.parseInt(data[1]); //count
					
					//get the total count for this current key
					Integer totalCount = outMap.get(key);
					if(totalCount == null){
						//if no total found, add count as the total
						outMap.put(key, count);
					}else{
						//add count to the current total value
						outMap.put(key, totalCount+count);
					}
				}
			}
			
			// get an iterator of the map holding the key-total count pairs
			Iterator<Entry<String, Integer>> it = outMap.entrySet().iterator();
			while(it.hasNext()){
				//print out the output according to specification
				Entry<String, Integer> pairs = it.next();
				System.out.println("The total for "+pairs.getKey()+
						" is "+pairs.getValue());
			}
			
			//close the buffer
			if (br != null)
				br.close();
		}catch(Exception e){
			e.printStackTrace();
		}
	}
}
