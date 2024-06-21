Numbers = list[int]
Divisors = list[Numbers]


def factorize(*number: Numbers) -> Divisors:
    '''
    Find divisors for each number in the list that are divisible without a
    remainder.

    :param number: Numbers

    :return: Divisors
    '''

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

        all_divisors.append(divisors)

    return all_divisors
