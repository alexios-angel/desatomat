# Desatomat
Open-source implementation of Desatomat and it's Extended Desátomatu Syntax. This is my effort to reverse-engineer the closed-source Desatomat tool.

This tool aims to cover the features used by the [Compile Time Regular Expressions](https://github.com/hanickadot/compile-time-regular-expressions) library grammer. It amins to be a drop in replacement.

## Usage

| Option            | Description                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------- |
| `--ll`            | Output LL1 grammer. This option is ignored as it is the default. The original Desatomat uses this option.     |
| `--q`             | Create Q-grammer. This option is ignored as it is the default. The original Desatomat uses this option.       |
| `--input`         | Input grammer file. Use `--input=-` if you are passing grammer via stdin                                      |
| `--output`        | Output directory or file. If not a filename `--cfg:fname` is used; Default directory is the current directory |
| `--cfg:fname`     | Filename for the output. If not specified grammer.hpp is used.                                                |
| `--cfg:namespace` | C++ namespace to put the grammer in                                                                           |
| `--cfg:guard`     | C++ header guard to use `#ifndef GUARDNAME #define GUARDNAME`                                                 |
| `--cfg:grammar_name` | C++ grammar struct name |

## Unsupported features
- `sigma-` is not supported as it is not used in CTRE. I also don't know what it does.
    - `sigma-` is correctly parsed, but is ignored in this Desatomat and the set is treated as a regular set.
- `NAME: rule` - NAME is ignored. It seems NAME is only there for debugging.