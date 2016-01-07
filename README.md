# morse
`morse` is a python library for controlling Wonder Workshop's
[Dash and Dot](https://www.makewonder.com/?gclid=CPOO8bC8k8oCFdaRHwodPeMIZg) bots.

The bots utilize a closed-source bluetooth API based on the GATT protocol. Our library provides python functions
for controlling (some of) the functionality available over bluetooth, such as eye, neck and ear colors,
sounds, and movement.

The library uses `pexpect` (via `pygatt`) to send commands to a `gatttool` session which then uses the ATT protocol
to send the bluetooth packets. The `gatttool` session is kept alive for as long as a reference to the bot object is available.

## Motivation
There exist smartphone apps which allow remote-controlling Dash and Dot, and even "writing programs" for them.
However, the programming functionality is limited to drag-and-drop style and does not allow interaction with
any industry programming languages.

That doesn't need to be the case - young kids can get started with the simple
drag-and-drop interface to get some exposure and instill interest, then graduate to a programming API interface in order
to create more complicated and complete implementations of their creative ideas.

`morse` provides that programming interface, in a language that is easy to pick up even for non-engineers: Python.

## Installation
This is only tested on Debian, though it should work on other Linux flavors. OSX and Windows are NOT supported.

Steps:

 * first clone this repo and `cd` into it
 * `apt-get install bluez`  # version 5+ is required by pygatt
 * `git clone https://github.com/peplin/pygatt`
 * `pip install -r requirements.pip`

## Example
Run:

```
python -m morse/examples/clock.py C0:F0:84:3C:51:FA
```

where `C0:F0:84:3C:51:FA` should be the bluetooth address of your bot
