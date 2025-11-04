from gen_random import gen_random_inf
class Unique(object):
    def __init__(self, items, **kwargs):
        self.ignore_case = kwargs.get('ignore_case', False)
        self.items = iter(items)
        self.seen = set()
        

    def __next__(self):
        while True:
            item = next(self.items)

            if self.ignore_case and isinstance(item, str):
                key = item.lower()
            else:
                key = item
            
            if key not in self.seen:
                self.seen.add(key)
                return item

    def __iter__(self):
        return self
def main():
    data1 = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    for item in Unique(data1):
        print(item)
    print("____________________")
    data2 = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    for item in Unique(data2, ignore_case=True):
        print(item)
    print("____________________")
    for item in Unique(data2):
        print(item)
    print("____________________")
    for item in Unique(gen_random_inf(10, 1, 3)):
        print(item)
    print("____________________")




if __name__ == "__main__":
    main()