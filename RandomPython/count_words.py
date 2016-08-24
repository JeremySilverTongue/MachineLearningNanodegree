"""Count words."""

import collections

def count_words(s, n):
    """Return the n most frequently occuring words in s."""
    
    # TODO: Count the number of occurences of each word in s
    
    split = collections.Counter(s.split())



    # TODO: Sort the occurences in descending order (alphabetically in case of ties)
    
    # TODO: Return the top n words as a list of tuples (<word>, <count>)
    return sorted(split.items(), cmp=compare, reverse = True )[:n]

def compare(x, y):
    if (x[1] < y[1]):
        return -1
    elif (x[1] > y[1]):
        return 1
    else:
        if x[0] > y[0]:
            return -1
        else: 
            return 1

def test_run():
    """Test count_words() with some inputs."""
    print count_words("cat bat mat cat bat cat", 3)
    print count_words("betty bought a bit of butter but the butter was bitter", 3)


if __name__ == '__main__':
    test_run()
