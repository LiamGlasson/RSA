# RSA File Encryption and Decryption
Simple CLI encryption/decryption for files using RSA.
___
## Dependencies
* pycryptodomex 3.16.0

  > *PyCryptodome* is a self-contained Python package of low-level cryptographic primitives.

  You can install it with: `pip install pycryptodomex`
___
Usage
---
To generate a new RSA key use:
- ```shell
  python3 RSA.py -g
  ```
To encrypt a file use:
- ```shell
  python3 RSA.py -f [FILENAME] -k [KEY] -e
  ```
To decrypt a file use:
- ```shell
  python3 RSA.py -f [FILENAME] -k [KEY] -d
  ```
For help:
- ```shell
  python3 RSA.py -h
  ```
