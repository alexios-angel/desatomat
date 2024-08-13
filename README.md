# Desatomat
Open-source implementation of Extended Desátomatu Syntax. The creator of the original Desatomat refuses to open-source it, so this is my effort to reverse-engineer the tool.

## Grammer

Below is the grammar for Extended Desátomatu Syntax:

| Syntax Element  | Definition |
|---:|:---|
| grammar                                | `((rule_statement \| set_definition \| comment) newline)*`                                   |
| comment                                | `'#' anything_not_newline*`                                                                  |
| rule_statement                         | `name "->" rule ('\|' rule)*`                                                                 |
| rule                                   | `(name ':')* rule_content`                                                                   |
| rule_content                           | `parts (',' parts)*`                                                                         |
| parts                                  | `terminal`                                                                                   |
|                                        | `string`                                                                                     |
|                                        | `non-terminal`                                                                               |
|                                        | `semantic_action`                                                                            |
| terminal                               | `name`                                                                                       |
|                                        | `'*' name`                                                                                   |
|                                        | `name epsilon atom`                                                                          |
| string                                 | `'"' text '"'`                                                                               |
| text                                   | `("\\"" \| ~["])*`                                                                           |
| non-terminal                           | `'<‘ name '>'`                                                                               |
| semantic_action                        | `'[' name ']'`                                                                               |
| name                                   | `[a-zA-Z_] [a-zA-Z_0-9]*`                                                                    |
| epsilon                                | `'@'`                                                                                        |
| set_definition                         | `name '=' minus_sigma? '{' set_content '}'`                                                  |
| minus_sigma                            | `"sigma" '-'`                                                                                |
| set_contents                           | `atom (',' atom)*`                                                                           |
| atom                                   | `'\\' ? anything_not_newline`                                                                |
| newline                                | `[\\n\\r]`                                                                                   |
| anything_not_newline                   | `~[\\n\\r]`                                                                                  |

