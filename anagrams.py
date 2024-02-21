 # Testing for anagrams

# get the two words from the user
text = input("Enter your two words separated by a space: ")


# strip out the whitespace and then check the length of the text object
# if 0, then nothing has been entered so is not an anagram
if len(text.strip()) == 0:
     print( "It's not an anagram" )
else:
    # split the words by the space between them into a list of 2 strings called words
    words = text.split(" ")
 
    # convert the words in the list to upper case
    word1 = words[0].upper()
    word2 = words[1].upper()

    # check the words are the same length
    if len(word1) != len(word2):
        print(f"Not anagrams as first word has {len(word1)} characters and second word has {len(word2)} characters.")
    
    # iterate through word1 testing whether the characters exist in word2
    else:
        for ch in word1:
            # if a certain charater doesn't appear in word2, print message to user and exit program
            if ch not in word2:
                print(f"No, no dice. Not anagrams. {ch} not in second word") 
                exit()
            # if they all appear, check that they appear the same number of times
            elif word1.count(ch) != word2.count(ch):  
                print(f"No, no dice. Not anagrams. Frequency of character {ch} different in the two words. ") 
                exit()
            
    # all characters in word1 appear in word2 in the same frequency 
        print("Yes! These are anagrams")
