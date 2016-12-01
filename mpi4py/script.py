n = 10000
size = 4
local_ns = list(n // size + (rank < (n % size)) for rank in range(size))
print local_ns
print sum(local_ns)
