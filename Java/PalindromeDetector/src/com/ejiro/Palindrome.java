package com.ejiro;

import java.util.Scanner;

/**
 * Write a function that determines if a given string is a palindrome. A
 * palindrome is a word or phrase that is spelled exactly the same forwards 
 * or backwards, like "pop" or "Ah, Satan sees Natasha". For this question, 
 * ignore all non-alphanumeric characters and assume that upper-and lower-
 * case characters are identical. The function should output whether or not 
 * the string is a palindrome and return a boolean.
 * 
 * @author Ejiro
 *
 */
public class Palindrome {

	
	public static void main(String[] args) {
		//get a handle to the standard input
		Scanner scanner = new Scanner(System.in);
		System.out.print("Enter a word or phrase: ");
		System.out.flush();
		
		//get the input word or phrase
		String input = scanner.nextLine();
		
		//determines if the input word or phrase is palindrome
		System.out.println(Palindrome.isPalindrome(input));
		
		//close the scanner
		scanner.close();
	}
	
	/**
	 * Write a function that determines if a given string is a palindrome.
	 * @param input
	 * @return output whether or not the string is a palindrome.
	 */
	private static boolean isPalindrome(String value){
		//removes all non-alphanumeric characters
		value = value.replaceAll("[^A-Za-z0-9 ]", "");
		int length = value.length();
		int left = 0;
		int right = length-1;
		
		//iterate half the length of the input value
		//comparing left half char to right half char
		//note: if space is found, it skips to the next valid character
		for(int j = 0; j < length/2; j++){
			char leftChar = Character.toLowerCase(value.charAt(left));
			if(leftChar == ' '){
				//increment left index and continue
				left++;
				continue;
			}
			char rightChar = Character.toLowerCase(value.charAt(right));
			if(rightChar == ' '){
				//decrement right index and continue
				right--;
				continue;
			}
			//increment left index and continue
			left++;
			//decrement right index and continue
			right--;
			
			//once any char do not match, it exit the loop by returning false
			if(leftChar != rightChar){
				return false;
			}
		}
		return true;
	}
}
