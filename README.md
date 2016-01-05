# morse
`morse` is a python library for controlling Wonder Workshop's
[Dash and Dot](https://www.makewonder.com/?gclid=CPOO8bC8k8oCFdaRHwodPeMIZg) bots.

The bots utilize a closed-source bluetooth API based on the GATT protocol. This library provides python functions
for controlling (some of) the functionality available over bluetooth, such as eye color and limited head and wheel movement.

## Installation
This is only tested on Debian, though it should work on other Linux flavors. OSX and Windows are NOT supported.

Steps:

 * `apt-get install bluez  # version 5+ is required by pygatt`
 * `git clone https://github.com/peplin/pygatt`
 * `pip install -r requirements.pip`

## Examples
Edit the source file to point to the right bluetooth address of your bot, then:

`python -m morse/examples/clock.py`
