# coding=utf-8
"""
Reversible Hash Algorithm: 8-bit

Compiled with <3 by an anonymous coder.

GitHub repository: https://github.com/An-anonymous-coder/RHA8

FUNCTIONS
---------
encrypt(file_path, password, decryption_key, verbose): Encrypts any file. Returns nothing.

decrypt(file_path, password, verbose): Decrypts any file. Returns nothing.
"""
import os
import time
import typing

import numpy  # https://numpy.org/install/


def encrypt(file_path: typing.Union[str, None] = None, password: typing.Union[str, None] = None,
            decryption_key: typing.Union[str, None] = None, verbose: bool = False) -> None:
    """
    This function encrypts any file.
    :param file_path: This is the file path for the file to be encrypted. If none is provided, you will be prompted for
        one. Defaults to None.
    :type file_path: str or None
    :param password: This is the password used to encrypt the file. If none is provided, you will be prompted for one.
        Defaults to None.
    :type password: str or None
    :param decryption_key: This is a key used to decrypt the file and to randomize the encryption. If none is provided,
        one is generated for you, but you can use this if you would like to use your own. Defaults to None.
    :type decryption_key: str or None
    :param bool verbose: If this is set to True, this will print what the function is doing at each step. Otherwise,
        those print statements are hidden. Defaults to False.
    """
    if not file_path:
        if verbose:
            print('[v] No file provided.')
        file_path = input('Enter the path of the file to encrypt: ')
    elif verbose:
        print('[v] File provided.')
    while True:
        if verbose:
            print('[v] Checking file...')
        if os.path.isfile(file_path) and os.path.exists(file_path):
            if verbose:
                print('[v] File is valid.')
            break
        else:
            print('File is invalid.')
            file_path = input('Enter the path of the file to encrypt: ')
    decrypted_file_name = os.path.basename(file_path)
    if not password:
        if verbose:
            print('[v] Password not provided.')
        password = input('Enter the password to encrypt the file: ')
    elif verbose:
        print('[v] Password provided.')
    if decryption_key:
        print('[v] Decryption key provided.')
    else:
        if verbose:
            print('[v] Decryption key not provided.')
            print('[v] Generating decryption key...')
        decryption_key = str(numpy.random.random())  # This generates a random decryption key.
        if verbose:
            print('[v] Decryption key: {key}'.format(key=decryption_key))
    if verbose:
        print('[v] Opening file... ({path})'.format(path=file_path))
    with open(file_path, 'rb') as decrypted_file:
        encrypted_file_name = decrypted_file_name + '.RHA8'
        # This generates a file name compatible with the `decrypt` function.
        encrypted_file_path = file_path.rstrip(decrypted_file_name) + encrypted_file_name
        # This generates the file path used to store the encrypted file.
        if os.path.exists(encrypted_file_path):
            print('[!] File {path} already exists.\n'.format(path=encrypted_file_path))
        if verbose:
            print('[v] Creating file... ({path})'.format(path=encrypted_file_path))
        with open(encrypted_file_path, 'wb') as encrypted_file:
            try:
                encrypted_file.write((decryption_key + ';').encode())
                # The semicolon is used to separate the decryption key from the rest of the file.
                numpy.random.seed(bytearray((password + decryption_key).encode()))
                # This randomizes the outcome of the encryption in a reversible way.
                if verbose:
                    file_size = os.path.getsize(file_path)
                    print('[v] Encrypting file... ({size} bytes)'.format(size=file_size))
                    start = time.perf_counter()  # This starts a timer to time the encryption.
                noise = numpy.random.randint(0, 257, file_size, dtype=numpy.uint8)
                encrypted_file.write(
                    bytearray(numpy.array(bytearray(decrypted_file.read()), dtype=numpy.uint8) + noise))
                # This is the algorithm that encrypts the file.
                end = time.perf_counter()
                if verbose:
                    seconds = end - start
                speed = round(file_size / seconds)
                print('[v] Encrypted in {seconds} seconds. ({speed:,} bytes per second)'.format(
                    seconds=round(seconds, 2),
                    speed=speed))
            except Exception as exception:
                encrypted_file.close()
                os.remove(encrypted_file_path)  # This removes the partially encrypted file.
                raise exception
        if verbose:
            print('[v] Closing files...')
        encrypted_file.close()
    decrypted_file.close()
    if verbose:
        print('[v] Cleaning up...')
    os.remove(file_path)  # This removes the decrypted file.
    print('Encrypted as: {name}'.format(name=encrypted_file_name))
    if verbose:
        print('[v] Done!\n')


def decrypt(file_path: typing.Union[str, None] = None, password: typing.Union[str, None] = None,
            verbose: bool = False) -> None:
    """
    This function decrypts a file encrypted with the `encrypt` function.
    :param file_path: This is the file path for the file to be decrypted. If none is provided, you will be prompted for
        one. Defaults to None.
    :type file_path: str or None
    :param password: This is the password used to decrypt the file. If none is provided, you will be prompted for one.
        Defaults to None.
    :type password: str or None
    :param bool verbose: If this is set to True, this will print what the function is doing at each step. Otherwise,
        those print statements are hidden. Defaults to False.
    """
    if not file_path:
        if verbose:
            print('[v] No file provided.')
        file_path = input('Enter the path of the file to decrypt: ')
    elif verbose:
        print('[v] File provided.')
    while True:
        if verbose:
            print('[v] Checking file...')
        if os.path.isfile(file_path) and os.path.exists(file_path) and file_path.endswith('.RHA8'):
            if verbose:
                print('[v] File is valid.')
            break
        else:
            print('File is invalid.')
            file_path = input('Enter the path of the file to decrypt: ')
    if not password:
        if verbose:
            print('[v] No password provided.')
        password = input('Enter the password to decrypt the file: ')
    elif verbose:
        print('[v] Password provided.')
    decrypted_file_name = os.path.splitext(os.path.basename(file_path))[0]
    decrypted_file_path = file_path.rstrip(os.path.basename(file_path)) + decrypted_file_name
    # This generates the file path used to store the decrypted file.
    if os.path.exists(decrypted_file_path):
        print('[!] File {path} already exists.\n'.format(path=decrypted_file_path))
        return
    if verbose:
        print('[v] Opening file...')
    with open(file_path, 'rb') as encrypted_file:
        if verbose:
            print('[v] Building decryption key...')
        decryption_key = ''
        character = encrypted_file.read(1)
        while character != b';':
            decryption_key += character.decode()
            character = encrypted_file.read(1)
        numpy.random.seed(bytearray((password + decryption_key).encode()))
        # This sets the random outcome to reverse the encryption.
        if verbose:
            print('[v] Creating file... ({path})'.format(path=decrypted_file_path))
        with open(decrypted_file_path, 'wb') as decrypted_file:
            try:
                if verbose:
                    file_size = os.path.getsize(file_path) - len(str(decryption_key)) - 1
                    print('[v] Decrypting file... ({size} bytes)'.format(size=file_size))
                    start = time.perf_counter()  # This starts a timer to time the decryption.
                noise = numpy.random.randint(0, 257, file_size, dtype=numpy.uint8)
                decrypted_file.write(
                    bytearray(numpy.array(bytearray(encrypted_file.read()), dtype=numpy.uint8) - noise))
                # This is the algorithm that decrypts the file.
                end = time.perf_counter()
                if verbose:
                    seconds = end - start
                    speed = round(file_size / seconds)
                    print('[v] Decrypted in {seconds} seconds. ({speed:,} bytes per second)'.format(
                        seconds=round(seconds, 2),
                        speed=speed))
            except Exception as exception:
                decrypted_file.close()
                os.remove(decrypted_file_path)  # This removes the partially decrypted file.
                raise exception
        if verbose:
            print('[v] Closing files...')
        decrypted_file.close()
    encrypted_file.close()
    if verbose:
        print('[v] Cleaning up...')
    os.remove(file_path)  # This removes the encrypted file.
    print('Decrypted as: {name}'.format(name=decrypted_file_name))
    if verbose:
        print('[v] Done!\n')
