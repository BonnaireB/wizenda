import datetime
import uuid
from uuid import uuid4
unique_token = uuid.uuid4()
# On decide quand est-ce que cette cle sera expire
expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
exp = '23:0'

daa = datetime.datetime.utcnow()
now = str(daa.hour) + ":" + str(daa.minute)
print(unique_token)
print(exp)
print(now)

hour_exp = exp.split(':')
hour_now = now.split(':')

if hour_exp[0] == '23' and hour_now[0] == '0'
	print("expire h")

if hour_exp[0] < hour_now[0] :
	print("expire h")
else:
	if hour_exp[1] < hour_now[1]:
	    print("expire")