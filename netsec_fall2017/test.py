import heapq

a = b"adbfsdbfsdbfsbdbfsbdfbasbdfabsbfdabsdfbasbdfabdfbasfdbasdbfkjkxkzjkz"


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# # print(chunks(a,2))
# print(len(a))
# for i in range(0, len(a), 5):
#     print(i)
#     yield a[i:i+5]

# for i in chunks(a,5):
    # print(i)
#
# a = {}
# a[100] = b"ahahhah"
# a[102] = b"isdfoad"
# a[88] = b'sdfadfb'
# b = a.items()u
#
#
# print (a)
# print(b)

b = []

heapq.heappush(b,1)
heapq.heappush(b,5)
heapq.heappush(b,9)
heapq.heappush(b,0)

print(b)


