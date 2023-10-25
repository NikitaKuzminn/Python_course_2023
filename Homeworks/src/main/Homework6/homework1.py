"""
# 1. Implement a function that flatten incoming data:
# non-iterables and elements from iterables (any nesting depth should be supported)
# function should return an iterator (generator function)
# don't use third-party libraries

def merge_elems(*elems):
    pass

# example input
a = [1, 2, 3]
b = 6
c = 'zhaba'
d = [[1, 2], [3, 4]]

for _ in merge_elems(a, b, c, d):
    print(_, end=' ')
"""


def merge_elems(*elems):
    for elem in elems:
        if isinstance(elem, (list, tuple)):
            yield from merge_elems(*elem)
        elif hasattr(elem, '__iter__') and not isinstance(elem, str):
            for sub_elem in merge_elems(*elem):
                yield sub_elem
        else:
            yield elem


if __name__ == '__main__':
    a = [1, 2, 3]
    b = 6
    c = 'zhaba'
    d = [[1, 2], [3, 4]]

    for item in merge_elems(a, b, c, d):
        print(item, end=' ')
