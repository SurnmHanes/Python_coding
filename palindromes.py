#Testing for palindromes

text = input("Enter your message: ")


text_adj = text.replace(" ", "")
text_adj = text_adj.upper()

try:
   # print(text_adj)
    if text == " ":
        print( "It's not a palindrome" )
    elif text_adj[::-1]  == text_adj:
        print( "It's a palindrome" )
    else:
        print( "It's not a palindrome" )
    
            
except (ValueError, TypeError):
     print('Invalid input. Please try again')