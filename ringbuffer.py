head = 0
tail = 0
size = 16


def write(bytes):
    global head
    global size
    head = (head + bytes) % size
    print("head: ", head)

def read(bytes):
    global tail
    global size
    tail = (tail + bytes) % size
    print("tail: ", tail)



write(4)
write(4)
read(4)
