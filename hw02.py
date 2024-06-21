from concurrent.futures import ProcessPoolExecutor
from logging import DEBUG, getLogger, StreamHandler, Formatter
from multiprocessing import cpu_count
from time import perf_counter

Numbers = list[int]
Divisors = list[Numbers]

logger = getLogger()
handler = StreamHandler()
handler.setFormatter(Formatter('%(processName)s %(levelname)s: %(message)s'))
logger.addHandler(handler)
logger.setLevel(DEBUG)


def factorize(*number: Numbers) -> Divisors:
    '''
    Find divisors for each number in the list that are divisible without a
    remainder.

    :param number: Numbers

    :return: Divisors
    '''

    logger.debug('Looking for divisors of the following divisibles: %s.',
                 ', '.join(map(str, number)))

    all_divisors: Divisors = []

    for divisible in number:
        if divisible < 1:
            raise ValueError(f'The number {divisible} should be greater than '
                             'or equal to one.')

        divisors: Numbers = [1]

        if divisible > 1:
            if divisible > 3:
                divisors.extend(
                    filter(lambda divisor: divisible % divisor == 0,
                           range(2, round(divisible / 2) + 1)))

            divisors.append(divisible)

        logger.debug('The divisors of divisible %i are: %s.',
                     divisible,
                     ', '.join(map(str, divisors)))

        all_divisors.append(divisors)

    return all_divisors


def main() -> None:
    numbers = list(map(int, input('Numbers split by a comma: ').split(',')))

    MESSAGE = '%s code execution time: %f seconds.'

    start = perf_counter()
    factorize(*numbers)
    logger.info(MESSAGE, 'Synchronous', perf_counter() - start)

    processes = min(len(numbers), cpu_count())
    logger.info(f'Processes: {processes}')

    start = perf_counter()

    with ProcessPoolExecutor(processes) as executor:
        executor.map(factorize, numbers)

    logger.info(MESSAGE, 'Asynchronous', perf_counter() - start)


if __name__ == '__main__':
    main()
