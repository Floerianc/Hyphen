# Hyphen 5

**INFO:**

Hyphen is a dashboard for a 64x32 RGB-LED-Panel running on e.g. a Raspberry Pi. It displays weather, Hamburg public transport, Bundestag election and pollen statistics and the following holidays as well as school vacations.

## Features

### All pages

`1. Weather`
* Rainbar (*visualizes precipitation*)
* Weather icon
* Precipitation graph (*1 bar = 1 hour*)
* Temperature graph (*1 bar = 1 hour*)

`2. HVV bus routes`
* Shows the next 3 busses for your selected routes and bus lines
    * Displays the bus line, destination and time of arrival in real-time

`3. Bundestag barometer`
* Displays election results in a bar chart
* Only shows parties with more than 5% of the votes (veto for the "Other")

`4. Pollen`
* Shows the most severe pollen in your region
    * Severity is color-coded (more info in core/pollen.py)
* Alignment is really weird but essentially centered around the center of the panel

`5. Holidays`
* Let's you see the next holidays and school vacations
    * Shows in how many days the holiday starts and the duration in days
* Overwrites the status bar when there's an active holiday/vacation
    * Also displays the remaining length of the holiday

## Installation

```bash
git clone https://github.com/Floerianc/Hyphen.git
cd Hyphen
uv sync
```

**Emulate the LED Panel**
```bash
uv run app.py
```

**Run the program on the computer connected to the LED Panel**
```bash
nano core/canvas.py
```
Replace the "from **RGBMatrixEmulator** import ..." with "from **rgbmatrix** import ..." at the top of the program.
The **rgbmatrix** package is not on PyPi and therefore you must use the `setup.py` to install it from [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix).

If you're unfamiliar with the installation process, the GitHub repository above has a bunch of tutorials and solved issue threads if you encounter any problems.

Then, you can run the program with the arguments you'd use in the sample scripts.
In my case, it looks like this:
```bash
sudo nohup ./.venv/python app.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-brightness=15 --led-slowdown-gpio=3
```
