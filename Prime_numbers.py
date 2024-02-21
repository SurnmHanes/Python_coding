def is_prime(num):
    prime = True
    number = int( num**0.5 ) + 1
    for i in range (2,number):
        if num % i == 0:
            prime = False
        else:
            continue
    return prime