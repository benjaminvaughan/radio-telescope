import pigpio

pi = pigpio.pi()

print(pi.read(13))
print(pi.read(19))
print(pi.read(26))
