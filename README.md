# Desatomat
Open-source implementation of Desatomat and it's Extended Desátomatu Syntax. This is my effort to reverse-engineer the closed-source Desatomat tool.

This tool aims to cover the features used by the [Compile Time Regular Expressions](https://github.com/hanickadot/compile-time-regular-expressions) library grammer. It aims to be a drop in replacement.

## Setup
To setup you need python and the lark parser
```bash
sudo apt install python3 python3-pip
pip3 install lark
git clone https://github.com/alexios-angel/desatomat.git
cd desatomat
chmod +x desatomat
```

## Usage

Basic usage:
```bash
./desatomat --input=FILENAME --output=/dev/stdout -q
```


| Option               | Description                                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------------------------- |
| `-q`                 | Only print errors to stdout                                                                                   |
| `--version` `-v`     | Print version and exit                                                                                        |
| `--verbose`          | Set log level to `debug`                                                                                      |
| `--log`              | Logs level; Takes `debug` `info` `warn` `error` and `critical` as options                                     |
| `--ll`               | Output LL1 grammer. This option is ignored as it is the default. The original Desatomat uses this option.     |
| `--q`                | Create Q-grammer. This option is ignored as it is the default. The original Desatomat uses this option.       |
| `--input`            | Input grammer file. Use `--input=-` if you are passing grammer via stdin                                      |
| `--output`           | Output directory or file. If not a filename `--cfg:fname` is used; Default directory is the current directory |
| `--cfg:fname`        | Filename for the output. If not specified grammer.hpp is used.                                                |
| `--cfg:namespace`    | C++ namespace to put the grammer in                                                                           |
| `--cfg:guard`        | C++ header guard to use `#ifndef GUARDNAME #define GUARDNAME`                                                 |
| `--cfg:grammar_name` | C++ grammar struct name                                                                                       |

## Unsupported features
- `sigma-` is not supported as it is not used in CTRE. I also don't know what it does.
    - `sigma-` is correctly parsed, but is ignored in this Desatomat and the set is treated as a regular set.
- `NAME: rule` - NAME is ignored. It seems NAME is only there for debugging.