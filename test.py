from matchers import *
from sklearn import decomposition
import pandas as pd
import timeit




if __name__ == '__main__':
    test_size = [100, 200, 400, 800, 1600, 3200, 6400, 12800]
    test_image = "lfw/Aaron_Eckhart/Aaron_Eckhart_0001.jpg"
    for n in test_size:
        try:
            os.remove(f"{index_name}_{n}.data")
            os.remove(f"{index_name}_{n}.index")
        except Exception:
            pass

    for n in test_size:
        print(f'Building index for {n}')
        idx = build_index(labels, pca_data, index_name, n)
        print(f'Starting test for {n}')

        knn = timeit.timeit(lambda: closest_matches_rtree(test_image, K, idx), number=10)
        print(f'{knn=}')
        
        range = timeit.timeit(lambda: closest_matches_sequential(test_image, K, idx), number=10)
        print(f'{range=}')

        
        
        
