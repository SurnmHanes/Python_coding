#Testing for palindromes

# obtain the word / phrase from the user
text = input("Enter your message: ")

# remove any whitespace to convert to a string of characters and convert to upper case
text_adj = text.replace(" ", "")
text_adj = text_adj.upper()

try:
  
   # if it is all whitespace i.e. nothing entered confirm not a palindrome
    if text == " ":
        print( "It's not a palindrome" )
  
   # reverse character string and compare to non-reversed version
    elif text_adj[::-1]  == text_adj:
        print( "It's a palindrome" )
    else:
        print( "It's not a palindrome" )
    
            
except (ValueError, TypeError):
     print('Invalid input. Please try again')
