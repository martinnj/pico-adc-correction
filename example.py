from calibrated_adc import CalibratedADC
from machine import ADC

adc = machine.ADC(28)
gnd_adc = machine.ADC(27)
vcc_adc = machine.ADC(26)

# Create the calibration class and have it use 5000 samples to perform the calibration.
c_adc = CalibratedADC(12)
c_adc.calibrate_adc(gnd_adc, vcc_adc, 5000)

# Read the ADC using the calibration class, use 2000 samples pr reading.
while True:
    adc_value = c_adc.read_adc(adc, 2000)
    print("Calibrated value:", adc_value)
