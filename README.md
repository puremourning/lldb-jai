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

# Using with Vimspector

Here's an example `.vimspector.json` that you can copy/paste (modify the
`initCommands` to specify the correct path):

```json
{
  "$schema": "https://puremourning.github.io/vimspector/schema/vimspector.schema.json",
  "configurations": {
    "Launch": {
      "adapter": "CodeLLDB",
      "variables": {
        "buildme": {
          "shell": "jai main.jai"
        }
      },
      "configuration": {
        "request": "launch",
        "program": "${workspaceRoot}/simple_jai_test",
        "expressions": "native",
        "initCommands": [
          "command script import $HOME/Development/jai/lldb-jai/jaitype.py"
        ]
      }
    }
  }
}
```

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

## Printing arrays (`$T[]` and `$T[..]`)

A summary is shown `Array(count=N)`, along with the members, also appropriately
summarised:

```
(lldb) var command
([] string) command = Array(count=3) {
  0 = A
  1 = B
  2 = /home/vagrant/Development/jai/tests/array_of
}
```

Works for `[] string` and `[..]string`

```
(lldb) var resizable
([..] string) resizable = Array(count=3,allocated=8) {
  0 = A
  1 = B
  2 = /home/vagrant/Development/jai/tests/array_of
}
```

You can print individual elements too, with usual validation:

```
(lldb) var command[3]
error: array index 3 is not valid for "([] string) command"
(lldb) var command[2]
(string) command[2] = /home/vagrant/Development/jai/tests/array_of
```
