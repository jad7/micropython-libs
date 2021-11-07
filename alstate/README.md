Usage:

You can define your variables, which will have defaule value (defined in as second param in state_val() function), or restored value from Flash (file).

This is useful when you don't know exact value for now, but it could we found in imperative way, and you want to use stored value after restart.

For example you have trigger for activation pin (device) based on ADC value from thermistor. You know approximate value, but exact value will be found and set from REPL.

     
```
from state import state_val

varbl1 = state_val("varbl1", 22)
varbl2 = state_val("varbl2", 25)

if varbl1.get() > varbl2.get(): # ... some logic
```