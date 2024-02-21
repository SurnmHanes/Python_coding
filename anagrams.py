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
 
    # call first string word1 and convert it to upper case
    # call second string word2 and convert to upper case
    word1 = words[0].upper()
    word2 = words[1].upper()

    # iterate through word1 testing whether the characters exist in word2
    # when you find the first one that doesn't, print message to user and exit program
    for ch in word1:
        if ch not in word2:
            print("No, no dice. Not anagrams") 
            exit()
            
    # all characters in word1 appear in word2. Now need to check the opposite
    # iterate through word1 testing whether character exists in word2
    # when found a character that doesn't, then can't be anagrams. 
    # print message to user and exit program
    for ch in word2:
        if ch not in word1:
            print("No, no dice. Not anagrams")
            exit()
    
    # all characters in word1 appear in word2 and vice versa
    print("Yes! These are anagrams")
