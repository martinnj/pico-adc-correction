# Raspberri Pi Pico ADC Correction

Convenience MicroPython class to produce calibrated ADC outputs on the Raspberry Pi Pico.

More or less a straight MicroPython conversion of Phoenix1747's
[Arduino package](https://github.com/Phoenix1747/Arduino-Pico-Analog-Correction).

I am fairly inept at electronics, so a lot of my terms are probably garbage, feel free to report or
submit corrections.

## Usage

Should be fairly straightforward from the docstrings, but check `example.py` if you need it. :)

A quick note on calibration: The best way would be to first connect the the ADC to a ground
referance, sample that, then to a vref and sample that. Then use those numbers for constructing the
`CalibratedADC` class.

Baring that, if you just need to use one ADC on the Pico, I've gotten fairly good results by using
two of the extra ADCs to gather the calibration data using `CalibratedADC.calibrate_adc`.
The ADCs are then connected to the ground plane and to `3v3` on pin 36 respectively.
`ADC_VREF` might be a better choice.

The reasoning is that since it's the same multi-channel ADC that does the measurements, it's likely
seeing the same noise and bias on all the ADCs.

## ADC Precision

The [datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) says the ADCs are 12bit,
but the values returned in MicroPython are 16-bit. This probably makes noise worse, so by default,
the `CalibratedADC` class will scale the output to 12-bit.

## On PSU Noise

The [datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) has some details in
section 4.3.

But basically, the ADC_VREF on the Pico is not very stable. Some people report improvements when
forcing the powersupply into strict PWM mode, but some report it making it worse. Experiment and draw your
own conclusions.

To force the PSU into PWM mode simply pull the PS mode pin high:
```python
ps_mode = Pin(23, Pin.OUT)
ps_mode.value(1)
```
