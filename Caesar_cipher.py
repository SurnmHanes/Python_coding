text = input("Enter your message: ")

try:
    shift_value = int( input('Enter a shift value between 1 and 25: ') )
except (ValueError, TypeError):
    print('Invalid input. Please enter a value between 1 and 25')
else:
    if 1 <= shift_value < 26:
        cipher = ''
        for char in text:
            if not char.isalpha():
                 cipher +=chr(ord(char))
            else:
                char_upper = char.upper()
                code = ord(char_upper) + shift_value
                if code > ord('Z'):
                    code = code - ord('Z') + ord('A') - 1
                if char_upper == char:
                    cipher += chr(code)
                else:
                    cipher += chr(code).lower()
        print(cipher)
    else:
        print('Invalid input. Please enter a value between 1 and 25')
