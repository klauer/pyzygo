pyzygo
======

Python to zygo interferometer interface (mrc3 / MetroPro)

* Uses ctypes to interface with the mrc3 DLL
* Fixes GIL-related issues with callbacks via the `callback_fix` extension.

Installation
============

1. Copy `mrc3_client.*` (.h, .lib, .dll) to this directory. (I don't think I have the rights to distribute this)

2. Set distutils to use Visual Studio to compile C++ code.

3. python setup.py build install

4. Simple example in zygo.py
