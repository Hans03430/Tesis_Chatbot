import multiprocessing

from typing import Callable, Iterable, Iterator

def parallelize_function(threads: int, func: Callable, arguments: Iterator, multiple_arguments: bool) -> Iterable:
    """
    This is a helper function that parallelizes a function call.

    Parameters:
    threads(int): The amount of workers to use.
    func(Callable): The function that will be parallelized.
    arguments(Iterator): The arguments for each function call.
    multiple_arguments(bool): Indicates if the function takes multiple parameters or a single parameter.
    
    Returns:
    Iterable: A list with the answers for each argument passed to the function.
    """
    pool = multiprocessing.Pool(threads)
    if multiple_arguments:
        results = pool.starmap(func, arguments)
    else:
        results = pool.map(func, arguments)
    pool.close()
    pool.join()
    return results