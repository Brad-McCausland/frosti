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

5/14/2016
  Added the new Freezer object for use in the Reader Module. A new test script for getting the average temperature for freezer #2 of 3 would be something like:
    
    import temp.py
    
    read.gpi_init()
    temp.freezers_init()
    temp.thermistors_init()
    temp = temp.calc_temp(1)
    print("Average temp for freezer 1: %.2f C\n" % temp)
    
    
