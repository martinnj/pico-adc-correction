from machine import ADC

class CalibratedADC():
    """
    Convinience class for helping decrease the noise of the built-in ADCs on the Raspberry Pi Pico.
    Can be used for other ADCs as well.

    Applies simple linear correction to measurements based on either given values or measured
    values.

    I am fairly inept at electronics, so a lot of my terms are probably garbage, feel free to submit
    corrections.

    The class is a conversion of Phoenix1747's Arduino Package:
    https://github.com/Phoenix1747/Arduino-Pico-Analog-Correction
    """
    _max_value = 0
    _gnd_offset = 0
    _vcc_offset = 0
    _a = 1.0
    _d = 1.0

    def __init__(self, adc_res: int=12, gnd_ref: int=0, vcc_ref: int=0):
        """
        Create a new onstance of the class.

        ### Arguments
        - adc_res : int (Optional, default: 12)
        The number of bits in the ADC output. While the Pico reports 16-bit outputs, it only has
        12-bit precision internally, so we scale down the output to the 12-bit range.
        - gnd_ref : int (Optional)
        Bootstrap the ground value, if you have another instance of the class that is already
        calibrated you can reuse it's calibration numbers here.
        - vcc_ref : int (Optional)
        Bootstrap the vcc value, if you have another instance of the class that is already
        calibrated you can reuse it's calibration numbers here.
        """
        self._max_value = (2**adc_res) - 1
        self._gnd_offset = gnd_ref
        self._vcc_offset = vcc_ref
        self._set_correction_values()


    def _set_correction_values(self) -> None:
        """
        Will recalculate and set the necesarry internal parameters based on the current GND and VCC
        offsets.
        """
        if self._vcc_offset == 0:
            self._a = 1.0
        else:
            self._a = self._max_value / (self._vcc_offset - self._gnd_offset)
        self._d = -self._a * self._gnd_offset


    def calibrate_adc(self, gnd_adc: ADC, vcc_adc: ADC, sample_size: int=100) -> None:
        """
        Measure and calculate correction values based on GND and VCC readings.
        Should only be done if gnd_ref and vcc_ref was not supplied to the constructor.

        ### Arguments
        - gnd_adc : machine.ADC
          An ADC connected to ground. Used to measure the calibrated ADCs offset from the "real"
          ground. Essenitally AGND on the Pico.
        - vcc_adc : machine.ADC
          An ADC connected to VCC. Used to measure the calibrated ADCs offset from the "real"
          operating voltage. Essentially ADC_VREF on the Pico.
        - sample_size : int (Optional, Default: 100)
          How many times should each ADC be sampled to produce the calibration values.
        """
        gnd_value = 0.0

        for _ in range(sample_size):
            gnd_value += float(gnd_adc.read_u16())
        self._gnd_offset = int(gnd_value/sample_size)

        vcc_value = 0.0
        for _ in range(sample_size):
            vcc_value += float(vcc_adc.read_u16())
        self._vcc_offset = int(vcc_value/sample_size)

        self._set_correction_values()


    def calibration_values(self) -> Tuple[int, int, float, float]:
        """
        Gets the calibration values as a tuple.
        The calibration values are:
        - gnd_offset: int - How far the measured GND was from 0.
        - vcc_offset: int - How far the measured VCC was from 0.
        - a: float - The correction factor applied to ADC measurements.
        - d: float - The absolute correction applied to ADC measurements.

        ### Returns
        tuple: A tuple with the following values:
           (gnd_offset, vcc_offset, a, d)
        """
        return (self._gnd_offset, self._vcc_offset, self._a, self._d)


    def read_adc(self, adc: ADC, sample_size: int=1000) -> int:
        """
        Given an ADC, use the calibration and multiple samples to get a, hopefully, more accurate
        reading.

        ### Arguments
        - adc : machine.ADC
          An ADC to read data from.
        - sample_size : int (Optional)
          How many samples to use for the measurement.

        ### Returns
        int : The calibrated reading from the ADC.
        """
        value = 0.0
        for i in range(sample_size):
            value += float(self._a * adc.read_u16() + self._d)

        return round(value/sample_size)
