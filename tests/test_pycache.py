from pycache import pyCache, PyObjectCache

def test_pycache():
    def doubler(n):
        return n * 2
    
    cache = PyObjectCache(doubler)
    for k in range(1, 4):
        cache[k]
    
    assert len(cache) == 3

def test_pycache_decorator_recursive():
    calls = [ ]

    @pyCache()
    def fib(n):
        calls.append(n)
        if n < 0:
            raise ValueError()
        if n in (0,1): 
            return n
        
        return fib(n - 1) + fib(n - 2)
    
    item = fib(1)
    assert item == 1
    assert len(calls) == 1
    item = fib(4)
    assert len(calls) == 5
    item = fib(5)
    assert len(calls) == 6
    item = fib(9)
    assert len(calls) == 10

def test_pycache_decorator_simple():
    val = [ ]
    
    @pyCache(comment='After')
    def get_mirror(item, comment = ''):
        if comment:
            val.append(comment)
        return item
    
    item = get_mirror(123)
    assert item == 123
    assert 'After' in val
    assert len(val) == 1
    item = get_mirror(1234)
    assert item == 1234
    assert len(val) == 2
    item = get_mirror(123)
    assert item == 123
    assert len(val) == 2

if __name__ == '__main__':
    test_pycache()