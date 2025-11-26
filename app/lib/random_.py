import random


def get_random_seq(size: int = 10):
    digits = "0123456789"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = ""
    chars = digits[:]
    chars += uppercase

    for _ in range(size):
        rand_ids =  random.randint(0, len(chars)-1)
        rand_chr = chars[rand_ids].lower() if rand_ids % 2 == 0 else chars[rand_ids].upper()
        password += rand_chr
    return password