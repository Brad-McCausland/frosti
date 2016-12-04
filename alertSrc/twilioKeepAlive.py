# This is a simple script to be run twice a month
# with the purpose of keeping twilio from revoking
# frosti's number (twilio will cancel a number if
# it goes more than a month without being used).
#
# This sends a simple message to users ostensibly
# as a test.

import alert

alert.send("This is a test of the FROSTI Freezer Monitoring Alert System. There is no emergency at this time.", "all")
