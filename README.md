# Hyphen 4

## Features

I will add this soon. ;)

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

**Run the program normally**
```bash
nano core/canvas.py
```
Replace the "from **RGBMatrixEmulator** import ..." with "from **rgbmatrix** import ..." at the top of the program.
The **rgbmatrix** package is not on PyPi and therefore you must use the `setup.py` to install it from [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix).

If you're unfamiliar with the installation process, the GitHub repository above has a bunch of tutorials and solved issue threads if you encounter any problems.

Then, you can run the program with the arguments you'd use in the sample scripts.
In my case, it looks like this:
```bash
sudo venv/python app.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-brightness=15 --led-slowdown-gpio=3
```
