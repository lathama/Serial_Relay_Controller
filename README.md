# Serial Relay Controller

## Introduction

Several makes of multi channel relay boards that are controlled over an RS232
serial port. I am testing with a model that uses a ULN2803A chip also noted as
a `darlington array` and an RS232 level shifter chip that is hard to read the
label on.

## Other labels silkscreened on the board:

`R221A08`
`8 Channel RS232 Relay`
`eletechsup`

## Control Commands

```
0 - Read
1 - Open
2 - Close
3 - Toggle
4 - Momentary ~200ms
5 - Interlock
```

### FAQs

Q: How can I run this as a user?
A: Add user to dialout group for access to ttyS or ttyUSB devices

## Next Steps

1. Add Argparse for CLI operation
1. Add schedule demo example
