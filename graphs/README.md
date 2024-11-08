To visualize matplotlib plots in the terminal I have installed https://github.com/daleroberts/itermplot/tree/master

I had to pip3 install itermplot==0.5 otherwise I would get an error.

You have to export this variable in your shell for it to work
```shell
export MPLBACKEND="module://itermplot"
```

To test
```shell
$ echo $MPLBACKEND
module://itermplot
$ python3
Python 3.5.2 (default, Oct 24 2016, 09:14:06)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import matplotlib.pyplot as plt
>>> plt.plot([1,2,3])
[<matplotlib.lines.Line2D object at 0x1041f2e48>]
>>> plt.show()
```
