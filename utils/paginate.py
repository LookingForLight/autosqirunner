

def paginate(page,size=10):
    if not isinstance(page,int):
        try:
            page = int(page)
        except TypeError:
            page=1

    if not isinstance(size,int):
        try:
            size = int(size)
        except TypeError:
            size=5

    if page > 0:
        page -=1
    data = {

        "limit":size,
        "offset":page*size,
        "before":page,
        "current":page+1,
        "next":page+2
    }

    return data

if __name__ == '__main__':


    result = paginate(3, 20)
    print(result)

