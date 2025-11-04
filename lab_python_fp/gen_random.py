import random
def gen_random_inf(num_count, begin, end):
    for _ in range(num_count):
        yield random.randint(begin, end)
def gen_random(num_count, begin, end):
    for item in gen_random_inf(num_count, begin, end):
        print(item)


def main():
    gen_random(5, 1, 3)





if __name__ == "__main__":
    main()