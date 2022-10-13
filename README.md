# LLDB Formatters for Jai

This repo contains some LLDB formatters and synthetic child providers for Jai.

What that means is that you can print Jai types with useful output.

# How to use

Put `jaitype.py` somewhere on the filesystem (e.g. `/path/to/jai/jaitype.py`), then add
this to a file named `~/.lldbinit`:

```
command script import /path/to/jai/jaitype.py
```

Note for Xcode, you might need `.lldbinit-Xcode` or one of many
[other confusing options](https://lldb.llvm.org/man/lldb.html#configuration-files).

# Supported types

## Summary for `string` values

The value of the string is printed:

```
(lldb) n
(lldb) frame variable s
(string) s = Hello, sailor!
```

You can see the underlying structure still, of course:

```
(lldb) frame variable s -R
(string) s = {
  count = 14
  data = 0x00000000002177a7
}
```

## Printing array elements (`$T[]` and `$T[..]`)

The default summary is used, which prints small arrays in one:

```
(lldb) var counters
([] s64) counters = (0 = 1, 1 = 2, 2 = 3)
```

Works for `[] string` and `[..]string`

```
(lldb) var command
([] string) command = (0 = A, 1 = B, 2 = /home/vagrant/Development/jai/tests/array_of)
(lldb) var resizable
([..] string) resizable = (0 = A, 1 = B, 2 = /home/vagrant/Development/jai/tests/array_of)
```

You can print individual elements too, with usual validation:

```
(lldb) var command[3]
error: array index 3 is not valid for "([] string) command"
(lldb) var command[2]
(string) command[2] = /home/vagrant/Development/jai/tests/array_of
```
