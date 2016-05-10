# frosti
Freezer-Ready Optimal Sustained Temperature Indicator

5/9/2016
  Added the Read Module source files. Currently, a test script would be like;
  
    import temp.py
    
    read.gpio_init()
    temp.thermistor_init()
    temp.calc_temp()
  
  The temperature calculation currently just prints out the values of each thermistor. Can easily be modded to return the list of thermistor objects to use as the Driver pleases. 

5/10/2016
  Added the Logger Module source files.
