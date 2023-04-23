# coding=utf-8
"""
Modified One-Time Pad

Compiled with <3 by an anonymous coder.

GitHub repository: https://github.com/An-anonymous-coder/MOTP

FUNCTIONS
---------
encrypt(file_path, password, verbose): Encrypts any file. Returns nothing.

decrypt(file_path, password, verbose): Decrypts any file. Returns nothing.

destroy(file_path, verbose): Destroys the decryption key for a file. Returns nothing.
"""
import os
import time
import typing

import numpy  # https://numpy.org/install/


def encrypt(file_path: typing.Union[str, None] = None, password: typing.Union[str, None] = None,
            verbose: bool = False) -> None:
    """
    This function encrypts any file.
    :param file_path: This is the file path for the file to be encrypted. If none is provided, you will be prompted for
        one. Defaults to None.
    :type file_path: str or None
    :param password: This is the password used to encrypt the file. If none is provided, you will be prompted for one.
        Defaults to None.
    :type password: str or None
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
        while True:
            password = input('Enter the password to encrypt the file: ')
            if input('Enter the password again to verify it: ') == password:
                if verbose:
                    print('[v] Password verified.')
                break
            print('Passwords do not match.')
    elif verbose:
        print('[v] Password provided.')
    if verbose:
        print('[v] Generating decryption key...')
    decryption_key = str(numpy.random.random())  # This generates a random decryption key.
    if verbose:
        print('[v] Decryption key: {key}'.format(key=decryption_key))
    if verbose:
        print('[v] Opening file... ({path})'.format(path=file_path))
    with open(file_path, 'rb') as decrypted_file:
        encrypted_file_name = decrypted_file_name + '.MOTP'
        # This generates a file name compatible with the `decrypt` function.
        encrypted_file_path = file_path.rstrip(decrypted_file_name) + encrypted_file_name
        # This generates the file path used to store the encrypted file.
        if os.path.exists(encrypted_file_path):
            print('[!] File {path} already exists.\n'.format(path=encrypted_file_path))

        def generate_pad(size: int) -> numpy.ndarray:
            """
            This generates a pseudorandom pad for the encryption.
            :param int size: This is the size of the pad.
            :return: Returns a numpy.ndarray of the pad.
            :rtype: numpy.ndarray
            """
            return numpy.random.randint(0, 256, size, dtype=numpy.uint8)

        def apply_pad(data: bytes, pad: numpy.ndarray) -> bytearray:
            """
            This is the function that encrypts the data.
            :param bytes data: This is the data to encrypt.
            :param numpy.ndarray pad: This is the pad to encrypt the data with.
            :return: Returns the encrypted data.
            :rtype: bytearray
            """
            return bytearray(numpy.array(bytearray(data), dtype=numpy.uint8) ^ pad)

        if verbose:
            print('[v] Creating file... ({path})'.format(path=encrypted_file_path))
        file_size = os.path.getsize(file_path)
        max_size = 1024 * 1024 * 1024
        # This is the maximum size (in bytes) per chunk. This can be higher based on your RAM.
        with open(encrypted_file_path, 'wb') as encrypted_file:
            try:
                encrypted_file.write((decryption_key + '\n').encode())
                # The semicolon is used to separate the decryption key from the rest of the file.
                numpy.random.seed(bytearray((password + decryption_key).encode()))
                # This randomizes the outcome of the encryption in a reversible way.
                if verbose:
                    print('[v] Encrypting file... ({size} bytes)'.format(size=file_size))
                    start = time.perf_counter()  # This starts a timer to time the encryption.
                for _ in range(int(file_size / max_size)):
                    encrypted_file.write(apply_pad(decrypted_file.read(max_size), generate_pad(max_size)))
                excess_size = file_size % max_size
                encrypted_file.write(apply_pad(decrypted_file.read(excess_size), generate_pad(excess_size)))
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
                decrypted_file.close()
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
        print('[v] Done!')
    print()


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
        if os.path.isfile(file_path) and os.path.exists(file_path) and file_path.endswith('.MOTP'):
            if verbose:
                print('[v] File is valid.')
            break
        else:
            print('File is invalid.')
            file_path = input('Enter the path of the file to decrypt: ')
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
        decryption_key = encrypted_file.readlines(1)[0].decode().rstrip()
        try:
            float(decryption_key)
        except ValueError:
            print('[!] Decryption key is invalid or destroyed.')
            return
        if not password:
            if verbose:
                print('[v] No password provided.')
            password = input('Enter the password to decrypt the file: ')
        elif verbose:
            print('[v] Password provided.')

        def generate_pad(size: int) -> numpy.ndarray:
            """
            This generates a pseudorandom pad for the decryption.
            :param int size: This is the size of the pad.
            :return: Returns a numpy.ndarray of the pad.
            :rtype: numpy.ndarray
            """
            return numpy.random.randint(0, 256, size, dtype=numpy.uint8)

        def apply_pad(data: bytes, pad: numpy.ndarray) -> bytearray:
            """
            This is the function that decrypts the data.
            :param bytes data: This is the data to decrypt.
            :param numpy.ndarray pad: This is the pad to decrypt the data with.
            :return: Returns the decrypted data.
            :rtype: bytearray
            """
            return bytearray(numpy.array(bytearray(data), dtype=numpy.uint8) ^ pad)

        if verbose:
            print('[v] Creating file... ({path})'.format(path=decrypted_file_path))
        file_size = os.path.getsize(file_path) - len(decryption_key) - 1
        max_size = 1024 * 1024 * 1024
        # This is the maximum size (in bytes) per chunk. This can be higher based on your RAM.
        with open(decrypted_file_path, 'wb') as decrypted_file:
            try:
                numpy.random.seed(bytearray((password + decryption_key).encode()))
                # This sets the random outcome to reverse the encryption.
                if verbose:
                    print('[v] Decrypting file... ({size} bytes)'.format(size=file_size))
                    start = time.perf_counter()  # This starts a timer to time the decryption.
                for _ in range(int(file_size / max_size)):
                    decrypted_file.write(apply_pad(encrypted_file.read(max_size), generate_pad(max_size)))
                excess_size = file_size % max_size
                decrypted_file.write(apply_pad(encrypted_file.read(excess_size), generate_pad(excess_size)))
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
                encrypted_file.close()
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
        print('[v] Done!')
    print()


def destroy(file_path: typing.Union[str, None] = None, verbose: bool = False) -> None:
    """
    This function destroys the decryption key in an encrypted file, making it impossible to decrypt. This does not
    delete the file. The key could be recovered via brute force. May cause MemoryError for large files.
    :param file_path: This is the path of the file to have the key of destroyed.
    :type file_path: str or None
    :param bool verbose: If this is set to True, this will print what the function is doing at each step. Otherwise,
        those print statements are hidden. Defaults to False.
    """
    if not file_path:
        if verbose:
            print('[v] No file provided.')
        file_path = input('Enter the path of the file to destroy the key for: ')
    elif verbose:
        print('[v] File provided.')
    while True:
        if verbose:
            print('[v] Checking file...')
        if os.path.isfile(file_path) and os.path.exists(file_path) and file_path.endswith('.MOTP'):
            if verbose:
                print('[v] File is valid.')
            break
        else:
            print('File is invalid.')
            file_path = input('Enter the path of the file to destroy the key for: ')
    if verbose:
        print('[v] Opening file...')
    with open(file_path, 'rb') as encrypted_file:
        if verbose:
            print('[v] Finding decryption key...')
        decryption_key = encrypted_file.readlines(1)[0].decode().rstrip()
        try:
            float(decryption_key)
        except ValueError:
            print('[!] Decryption key is invalid or destroyed.')
            return
        decryption_key_length = len(decryption_key)
        data = b'\n' + encrypted_file.read()
    encrypted_file.close()
    file_size = os.path.getsize(file_path) - decryption_key_length - 1
    with open(file_path, 'wb') as encrypted_file:
        try:
            if verbose:
                print('[v] Writing to file... ({size} bytes)'.format(size=file_size))
                start = time.perf_counter()  # This starts a timer to time the writing.
            encrypted_file.write(data)
            end = time.perf_counter()
            if verbose:
                seconds = end - start
                speed = round(file_size / seconds)
                print('[v] Wrote in {seconds} seconds. ({speed:,} bytes per second)'.format(seconds=round(seconds, 2),
                                                                                            speed=speed))
        except Exception as exception:
            encrypted_file.close()
            raise exception
    encrypted_file.close()
    if verbose:
        print('[v] Done!')
    print()
