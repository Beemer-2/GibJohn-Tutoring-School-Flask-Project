import string
import random
import bcrypt
import hashlib

# string_for_hash = string.ascii_letters + string.digits + string.punctuation

# salt = "".join([y for y in string_for_hash[random.randint(0, len(string_for_hash)-1)]])
# print(salt)

# print("".join([x + "".join([y for y in salt]) for x in "abcHitEmWithThe123"])) 


# hashlib.sha512("abc".encode()).hexdigest()

salt = bcrypt.gensalt()

for i in range(0, 100):


    my_hash = bcrypt.hashpw("abc".encode("utf-8"), salt)


    print(my_hash)


for i in range(0, 100):
    print(hashlib.sha512("abc".encode()).hexdigest())