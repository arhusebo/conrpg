def get_key(string='', echo=False):
    import msvcrt
    print(string, end='')
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key in u'\x00\xe0':  # arrow or function key prefix?
                key = msvcrt.getwch()  # second call returns the actual key code
                key = {
                    'H' : 'w',
                    'K' : 'a',
                    'P' : 's',
                    'M' : 'd',
                }.get(key)
            if echo:
                msvcrt.putwch(key)
            return {
                '\x1b' : 'ESC',
            }.get(key, key)