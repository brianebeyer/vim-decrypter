import os
import threading
import sys
from zipfile import _ZipDecrypter


def run(filename):
    try:
        import lzma
    except ImportError:
        from backports import lzma

    x = lzma.open(filename)
    decompressed = x.read()
    print('decompressed')

    without_vim_header = decompressed[12:]
    print('header stripped')

    # decrypt
    for words_file in sys.argv[1:]:
        try_words(without_vim_header, words_file)


def try_words(without_vim_header, words_file):
    print('guessing passwords from [%s]' % words_file)
    for i, word in enumerate(open(words_file)):
        word = word.strip()
        if i % 5000 == 0:
            print('Testing word #%d' % i)

        zd = _ZipDecrypter(word)
        decrypted = ''.join(zd(c) for c in without_vim_header)

        if 'key' in decrypted:
            print('*' * 80)
            print('Found "key" with password [%s]' % word)
            print decrypted

        dec = is_ascii(decrypted)
        if dec and 'key' in dec:
            print('*' * 80)
            print('Found "key" in ascii decrypted with password [%s]' % word)
            print dec
            os.system('say "Found potential password %s"' % word)


def is_ascii(s):
    try:
        ret = s.decode('ascii')
    except UnicodeDecodeError:
        return None
    else:
        return ret


if __name__ == '__main__':
    run('dogecrypt-b36f587051faafc444417eb10dd47b0f30a52a0b')