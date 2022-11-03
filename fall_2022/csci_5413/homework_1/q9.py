import time
import random
import string
import hashlib

def hash(clear_text) :
    md5_hash = hashlib.md5(clear_text.encode()).hexdigest()
    return md5_hash[:6] + md5_hash[-6:]

start = time.time()
starting_string = ''.join([
    random.choice(string.ascii_letters + string.digits) 
    for _ in range(random.randint(1,10000))])
hare = hash(starting_string)
tortoise = hash(hash(starting_string))

print("Calculating hashes")
while hare != tortoise:
    hare = hash(hare)
    tortoise = hash(hash(tortoise))

print("Found cycle. Finding collision")
collision_1, collision_2 = None, None
hare = hash(starting_string)
tortoise = hash(tortoise)

while hare != tortoise:
    collision_1 = hare
    collision_2 = tortoise
    hare = hash(hare)
    tortoise = hash(tortoise)

end = time.time() 
print("Collision Found in", end - start, "s\n", collision_1, "\n", 
    hashlib.md5(collision_1.encode()).hexdigest(), "\n", collision_2, "\n", 
    hashlib.md5(collision_2.encode()).hexdigest())