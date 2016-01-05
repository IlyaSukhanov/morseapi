# morse
`morse` is a python library for controlling Wonder Workshop's
[Dash and Dot](https://www.makewonder.com/?gclid=CPOO8bC8k8oCFdaRHwodPeMIZg) bots.

The bots utilize a closed-source bluetooth API based on the GATT protocol. This library provides python functions
for controlling (some of) the functionality available over bluetooth, such as eye color, neck and ear colors,
sounds and limited head movement.

The library uses `pexpect` (via `pygatt`) to send commands to a `gatttool` session which then uses the ATT protocol
to send the bluetooth packets. The `gatttool` session is kept alive for as long as a reference to the bot object is available.

## Installation
This is only tested on Debian, though it should work on other Linux flavors. OSX and Windows are NOT supported.

Steps:

 * `apt-get install bluez  # version 5+ is required by pygatt`
 * `git clone https://github.com/peplin/pygatt`
 * `pip install -r requirements.pip`

## Examples
Edit the source file to point to the right bluetooth address of your bot, then:

`python -m morse/examples/clock.py`
