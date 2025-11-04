def field_gen(items, *args):
    assert len(args) > 0
    if len(args)==1:
        for item in items:
            value=item.get(args[0])
            if value is not None:
                yield value
    else:
        for item in items:
            result = {}
            for arg in args:
                value = item.get(arg)
                if value is not None:
                    result[arg] = value
            if result:
                yield result
def field(items, *args):
    for item in field_gen(items,*args):
        print(item)
    
def main():
    goods = [
        {'title': 'Ковер', 'price': 2000, 'color': 'green'},
        {'title': 'Диван для отдыха', 'color': 'black'}
    ]
     
    field(goods, 'title', 'price')
     

if __name__ == "__main__":
    main()