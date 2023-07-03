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
import sys
import time
import typing

import numpy  # https://numpy.org/install/

# I hate `tkinter`'s inconsistency.
if sys.version_info.major < 3 or sys.version_info.minor < 3:  # For Python 3.2.x and below (Untested)
    import tkSimpleDialog as dialog
elif sys.version_info.minor < 6:  # For Python 3.3.x through 3.5.x (Untested)
    from tkinter import simpledialog as dialog
else:  # For Python 3.6.x and above (Tested Python 3.10.6)
    import tkinter
    import tkinter.simpledialog as dialog

    tkinter.Tk().withdraw()  # Someone said this was necessary (It worked without in Python 3.10.6)
red = '\u001b[38;2;255;0;0m'
yellow = '\u001b[38;2;255;255;0m'
green = '\u001b[38;2;0;255;0m'
cyan = '\u001b[38;2;0;255;255m'
blue = '\u001b[38;2;0;127;255m'  # Technically azure
grey = '\u001b[38;2;127;127;127m'
bold = '\u001b[1m'
reset = '\u001b[0m'


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
            print('{blue}[v] {yellow}No file provided.{reset}'.format(blue=blue, yellow=yellow, reset=reset))
        file_path = input('{bold}Enter the path of the file to encrypt: {reset}'.format(bold=bold, reset=reset))
    elif verbose:
        print('{blue}[v] {green}File provided.{reset}'.format(blue=blue, green=green, reset=reset))
    while True:
        if verbose:
            print('{blue}[v] {grey}Checking file...{reset}'.format(blue=blue, grey=grey, reset=reset))
        if os.path.isfile(file_path) and os.path.exists(file_path):
            if verbose:
                print('{blue}[v] {green}File is valid.{reset}'.format(blue=blue, green=green, reset=reset))
            break
        else:
            print('{red}File is invalid.{reset}'.format(red=red, reset=reset))
            file_path = input('{bold}Enter the path of the file to encrypt: {reset}'.format(bold=bold, reset=reset))
    decrypted_file_name = os.path.basename(file_path)
    if not password:
        if verbose:
            print('{blue}[v] {yellow}Password not provided.{reset}'.format(blue=blue, yellow=yellow, reset=reset))
        while True:
            try:
                password = dialog.askstring("Password", 'Enter the password to encrypt the file:', show='*')
                confirmation = dialog.askstring("Password", 'Enter the password again to verify it:', show='*')
            except ModuleNotFoundError:  # Please contact me if this happens
                password = input('{bold}Enter the password to encrypt the file: {reset}'.format(bold=bold, reset=reset))
                confirmation = input(
                    '{bold}Enter the password again to verify it: {reset}'.format(bold=bold, reset=reset))
            if confirmation == password:
                if verbose:
                    print('{blue}[v] {green}Password verified.{reset}'.format(blue=blue, green=green, reset=reset))
                break
            print('{red}Passwords do not match.{reset}'.format(red=red, reset=reset))
    elif verbose:
        print('{blue}[v] {green}Password provided.{reset}'.format(blue=blue, green=green, reset=reset))
    if verbose:
        print('{blue}[v] {grey}Generating decryption key...{reset}'.format(blue=blue, grey=grey, reset=reset))
    decryption_key = str(numpy.random.default_rng().random())  # This generates a random decryption key.
    if verbose:
        print('{blue}[v] {cyan}Decryption key: {reset}{bold}{key}{reset}'.format(blue=blue, cyan=cyan, bold=bold,
                                                                                 reset=reset,
                                                                                 key=decryption_key))
    if verbose:
        print('{blue}[v] {grey}Opening file... ({green}{path}{grey}){reset}'.format(blue=blue, grey=grey, green=green,
                                                                                    reset=reset, path=file_path))
    with open(file_path, 'rb') as decrypted_file:
        encrypted_file_name = decrypted_file_name + '.MOTP'
        # This generates a file name compatible with the `decrypt` function.
        encrypted_file_path = file_path.rstrip(decrypted_file_name) + encrypted_file_name
        # This generates the file path used to store the encrypted file.
        if os.path.exists(encrypted_file_path):
            print(
                '{red}[!] File {green}{path} {red}already exists.{reset}\n'.format(red=red, green=green, reset=reset,
                                                                                   path=encrypted_file_path))

        def generate_pad(seed, size: int) -> numpy.ndarray:
            """
            This generates a pseudorandom pad for the encryption.
            :param seed: This is the default_rng seed to set the random outcome
            :type seed: <class 'numpy.random._generator.Generator'>
            :param int size: This is the size of the pad.
            :return: Returns a numpy.ndarray of the pad.
            :rtype: numpy.ndarray
            """
            return seed.integers(0, 255, size, dtype=numpy.uint8)

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
            print('{blue}[v] {grey}Creating file... ({green}{path}{grey}){reset}'.format(blue=blue, grey=grey,
                                                                                         green=green, reset=reset,
                                                                                         path=encrypted_file_path))
        file_size = os.path.getsize(file_path)
        max_size = 1024 * 1024 * 1024
        # This is the maximum size (in bytes) per chunk. This can be higher based on your RAM.
        # THE FILE MUST BE DECRYPTED WITH THE SAME CHUNK SIZE YOU ENCRYPTED IT WITH.
        with open(encrypted_file_path, 'wb') as encrypted_file:
            try:
                encrypted_file.write((decryption_key + '\n').encode())
                # The newline is used to separate the decryption key from the rest of the file.
                rng = numpy.random.default_rng(seed=int.from_bytes(bytes((password + decryption_key).encode()), 'big'))
                # This randomizes the outcome of the encryption in a reversible way.
                if verbose:
                    print('{blue}[v] {grey}Encrypting file... ({cyan}{size} bytes{grey}){reset}'.format(blue=blue,
                                                                                                        grey=grey,
                                                                                                        cyan=cyan,
                                                                                                        reset=reset,
                                                                                                        size=file_size))
                    start = time.perf_counter()  # This starts a timer to time the encryption.
                for _ in range(int(file_size / max_size)):
                    encrypted_file.write(apply_pad(decrypted_file.read(max_size), generate_pad(rng, max_size)))
                excess_size = file_size % max_size
                encrypted_file.write(apply_pad(decrypted_file.read(excess_size), generate_pad(rng, excess_size)))
                end = time.perf_counter()
                if verbose:
                    seconds = end - start
                    speed = round(file_size / seconds)
                    message = '{blue}[v] {grey}Encrypted in {seconds} seconds. ({cyan}{speed:,} bytes per second{grey})'
                    print((message + reset).format(blue=blue, grey=grey, cyan=cyan, seconds=round(seconds, 2),
                                                   speed=speed))
            except Exception as exception:
                encrypted_file.close()
                os.remove(encrypted_file_path)  # This removes the partially encrypted file.
                decrypted_file.close()
                raise exception
        if verbose:
            print('{blue}[v] {grey}Closing files...{reset}'.format(blue=blue, grey=grey, reset=reset))
        encrypted_file.close()
    decrypted_file.close()
    if verbose:
        print('{blue}[v] {grey}Cleaning up...{reset}'.format(blue=blue, grey=grey, reset=reset))
    os.remove(file_path)  # This removes the decrypted file.
    print('Encrypted as: {green}{name}{reset}'.format(green=green, reset=reset, name=encrypted_file_name))
    if verbose:
        print('{blue}[v] {green}Done!{reset}'.format(blue=blue, green=green, reset=reset))
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
            print('{blue}[v] {yellow}No file provided.{reset}'.format(blue=blue, yellow=yellow, reset=reset))
        file_path = input('{bold}Enter the path of the file to decrypt: {reset}'.format(bold=bold, reset=reset))
    elif verbose:
        print('{blue}[v] {green}File provided.{reset}'.format(blue=blue, green=green, reset=reset))
    while True:
        if verbose:
            print('{blue}[v] {grey}Checking file...{reset}'.format(blue=blue, grey=grey, reset=reset))
        if os.path.isfile(file_path) and os.path.exists(file_path) and file_path.endswith('.MOTP'):
            if verbose:
                print('{blue}[v] {green}File is valid.{reset}'.format(blue=blue, green=green, reset=reset))
            break
        else:
            print('{red}File is invalid.{reset}'.format(red=red, reset=reset))
            file_path = input('{bold}Enter the path of the file to decrypt: {reset}'.format(bold=bold, reset=reset))
    decrypted_file_name = os.path.splitext(os.path.basename(file_path))[0]
    decrypted_file_path = file_path.rstrip(os.path.basename(file_path)) + decrypted_file_name
    # This generates the file path used to store the decrypted file.
    if os.path.exists(decrypted_file_path):
        print('{red}[!] File {green}{path} {red}already exists.{reset}\n'.format(red=red, green=green, reset=reset,
                                                                                 path=decrypted_file_path))
        return
    if verbose:
        print('{blue}[v] {grey}Opening file...{reset}'.format(blue=blue, grey=grey, reset=reset))
    with open(file_path, 'rb') as encrypted_file:
        if verbose:
            print('{blue}[v] {grey}Building decryption key...{reset}'.format(blue=blue, grey=grey, reset=reset))
        decryption_key = encrypted_file.readlines(1)[0].decode().rstrip()
        try:
            float(decryption_key)
        except ValueError:
            print('{red}[!] Decryption key is invalid or destroyed.{reset}'.format(red=red, reset=reset))
            return
        if not password:
            if verbose:
                print('{blue}[v] {yellow}No password provided.{reset}'.format(blue=blue, yellow=yellow, reset=reset))
            try:
                password = dialog.askstring("Password", 'Enter the password to decrypt the file:', show='*')
            except ModuleNotFoundError:  # Please contact me if this happens
                password = input('{bold}Enter the password to decrypt the file: {reset}'.format(bold=bold, reset=reset))
        elif verbose:
            print('{blue}[v] {green}Password provided.{reset}'.format(blue=blue, green=green, reset=reset))

        def generate_pad(seed, size: int) -> numpy.ndarray:
            """
            This generates a pseudorandom pad for the decryption.
            :param seed: This is the default_rng seed to set the random outcome
            :type seed: <class 'numpy.random._generator.Generator'>
            :param int size: This is the size of the pad.
            :return: Returns a numpy.ndarray of the pad.
            :rtype: numpy.ndarray
            """
            return seed.integers(0, 255, size, dtype=numpy.uint8)

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
            print('{blue}[v] {grey}Creating file... ({green}{path}{grey}){reset}'.format(blue=blue, grey=grey,
                                                                                         green=green, reset=reset,
                                                                                         path=decrypted_file_path))
        file_size = os.path.getsize(file_path) - len(decryption_key) - 1
        max_size = 1024 * 1024 * 1024
        # This is the maximum size (in bytes) per chunk. This can be higher based on your RAM.
        # THE FILE MUST BE DECRYPTED WITH THE SAME CHUNK SIZE YOU ENCRYPTED IT WITH.
        with open(decrypted_file_path, 'wb') as decrypted_file:
            try:
                rng = numpy.random.default_rng(seed=int.from_bytes(bytes((password + decryption_key).encode()), 'big'))
                # This sets the random outcome to reverse the encryption.
                if verbose:
                    print('{blue}[v] {grey}Decrypting file... ({cyan}{size} bytes{grey}){reset}'.format(blue=blue,
                                                                                                        grey=grey,
                                                                                                        cyan=cyan,
                                                                                                        reset=reset,
                                                                                                        size=file_size))
                    start = time.perf_counter()  # This starts a timer to time the decryption.
                for _ in range(int(file_size / max_size)):
                    decrypted_file.write(apply_pad(encrypted_file.read(max_size), generate_pad(rng, max_size)))
                excess_size = file_size % max_size
                decrypted_file.write(apply_pad(encrypted_file.read(excess_size), generate_pad(rng, excess_size)))
                end = time.perf_counter()
                if verbose:
                    seconds = end - start
                    speed = round(file_size / seconds)
                    message = '{blue}[v] {grey}Decrypted in {seconds} seconds. ({cyan}{speed:,} bytes per second{grey})'
                    print((message + reset).format(blue=blue, grey=grey, cyan=cyan, seconds=round(seconds, 2),
                                                   speed=speed))
            except Exception as exception:
                decrypted_file.close()
                os.remove(decrypted_file_path)  # This removes the partially decrypted file.
                encrypted_file.close()
                raise exception
        if verbose:
            print('{blue}[v] {grey}Closing files...{reset}'.format(blue=blue, grey=grey, reset=reset))
        decrypted_file.close()
    encrypted_file.close()
    if verbose:
        print('{blue}[v] {grey}Cleaning up...{reset}'.format(blue=blue, grey=grey, reset=reset))
    os.remove(file_path)  # This removes the encrypted file.
    print('Decrypted as: {green}{name}{reset}'.format(green=green, reset=reset, name=decrypted_file_name))
    if verbose:
        print('{blue}[v] {green}Done!{reset}'.format(blue=blue, green=green, reset=reset))
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
            print('{blue}[v] {yellow}No file provided.{reset}'.format(blue=blue, yellow=yellow, reset=reset))
        file_path = input(
            '{bold}Enter the path of the file to destroy the key for: {reset}'.format(bold=bold, reset=reset))
    elif verbose:
        print('{blue}[v] {green}File provided.{reset}'.format(blue=blue, green=green, reset=reset))
    while True:
        if verbose:
            print('{blue}[v] {grey}Checking file...{reset}'.format(blue=blue, grey=grey, reset=reset))
        if os.path.isfile(file_path) and os.path.exists(file_path) and file_path.endswith('.MOTP'):
            if verbose:
                print('{blue}[v] {green}File is valid.{reset}'.format(blue=blue, green=green, reset=reset))
            break
        else:
            print('{red}File is invalid.{reset}'.format(red=red, reset=reset))
            file_path = input(
                '{bold}Enter the path of the file to destroy the key for: {reset}'.format(bold=bold, reset=reset))
    if verbose:
        print('{blue}[v] {grey}Opening file...{reset}'.format(blue=blue, grey=grey, reset=reset))
    with open(file_path, 'rb') as encrypted_file:
        if verbose:
            print('{blue}[v] {grey}Finding decryption key...{reset}'.format(blue=blue, grey=grey, reset=reset))
        decryption_key = encrypted_file.readlines(1)[0].decode().rstrip()
        try:
            float(decryption_key)
        except ValueError:
            print('{red}[!] Decryption key is invalid or already destroyed.{reset}'.format(red=red, reset=reset))
            return
        decryption_key_length = len(decryption_key)
        data = b'\n' + encrypted_file.read()
    encrypted_file.close()
    file_size = os.path.getsize(file_path) - decryption_key_length - 1
    with open(file_path, 'wb') as encrypted_file:
        try:
            if verbose:
                print(
                    '{blue}[v] {grey}Writing to file... ({cyan}{size} bytes{grey}){reset}'.format(blue=blue, grey=grey,
                                                                                                  cyan=cyan,
                                                                                                  reset=reset,
                                                                                                  size=file_size))
                start = time.perf_counter()  # This starts a timer to time the writing.
            encrypted_file.write(data)
            end = time.perf_counter()
            if verbose:
                seconds = end - start
                speed = round(file_size / seconds)
                message = '{blue}[v] {grey}Wrote in {seconds} seconds. ({cyan}{speed:,} bytes per second{grey}){reset}'
                print(message.format(blue=blue, grey=grey, cyan=cyan, reset=reset, seconds=round(seconds, 2),
                                     speed=speed))
        except Exception as exception:
            encrypted_file.close()
            raise exception
    encrypted_file.close()
    if verbose:
        print('{blue}[v] {green}Done!{reset}'.format(blue=blue, green=green, reset=reset))
    print()
