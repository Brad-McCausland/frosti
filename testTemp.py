import temp.py

read.gpio_init()
temp.freezers_init()
temp.thermistors_init()
temp = temp.calc_temp(1)
print("Average temp for freezer 1: %.2f C\n" % temp)
