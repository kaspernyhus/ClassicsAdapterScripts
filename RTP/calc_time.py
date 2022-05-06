
samplerate = 48000
bytes_per_sample = 2
channels = 2




time1 = 29.454428172
timestamp1 = 3217191326

time2 = 29.461627293
timestamp2 = 3217191673


deltaTime = (time2-time1) * 1000
deltaTimestamps = timestamp2-timestamp1

expected_bytes = (samplerate/1000)*channels*bytes_per_sample*deltaTime

timeInSamples = deltaTime * (samplerate/1000)
print("timeInSamples:", timeInSamples)

print("expected_bytes:", expected_bytes)
print("deltaTime [ms]:", deltaTime)
print("deltaTimestamps:", deltaTimestamps)



