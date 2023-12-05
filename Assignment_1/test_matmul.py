import pytest
from matmul import matmul

# Things to be tested
# - test cases with valid matrices - last
# - Non-numeric input should result in TypeError
# - Mismatched axes should result in ValueError - matrices but wrong kind
# - Non-matrices - IndexError or TypeError? - catch and change Error 
# Note: we cannot test Type == List since any iterable type should be OK.
# Also, checking all the sublists to see size is probably a waste in general.
# Instead we can rely on the IndexError if we go out of bounds.

def test_non_numeric():
    A = [["a"]]
    B = [[1]]
    with pytest.raises(TypeError):
        matmul(A, B)

def test_axis_mismatch():
    A = [[1, 2]]    # 1x2
    B = [[3, 4]]    # 1x2
    with pytest.raises(ValueError):
        matmul(A, B)

def test_vector():
    A = [[1, 2], [3, 4]]
    B = [5, 6]
    with pytest.raises(TypeError):
        matmul(A, B)

testmats = [
    ([[1]], [[1]], [[1]]),
    ([[1,2], [3,4]], [[5],[6]], [[17], [39]]),
    ([[0.74114938, 0.91905821, 0.50648288],
       [0.52836273, 0.98985418, 0.30677585],
       [0.95278535, 0.15013316, 0.86501502],
       [0.65980878, 0.79062152, 0.54264614]], 
       [[0.86293906, 0.46875851],
       [0.65172811, 0.36619438],
       [0.26499233, 0.70944956]], 
       [[1.3727569 , 1.04329809],
       [1.18235388, 0.82779556],
       [1.14926404, 1.11528868],
       [1.2284421 , 0.9837922 ]])
       ]

def checkdiff(a, b):
    """Assume matrices are of correct dimensions."""
    s = 0
    for i in range(len(a)):
        for j in range(len(a[0])):
            s += abs(a[i][j] - b[i][j])
    return s

@pytest.mark.parametrize("a,b,expected", testmats)
def test_matmul(a, b, expected):
    """Test with various input combinations."""
    assert checkdiff(expected, matmul(a, b)) <= 0.001
