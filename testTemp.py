import temp.py

read.gpio_init()
temp.freezers_init()
temp.thermistors_init()
temp = temp.calc_temp(0)
print("Average temp for freezer 0: %.2f C\n" % temp)
temp = temp.calc_temp(1)
print("Average temp for freezer 1: %.2f C\n" % temp)
temp = temp.calc_temp(2)
print("Average temp for freezer 2: %.2f C\n" % temp)
