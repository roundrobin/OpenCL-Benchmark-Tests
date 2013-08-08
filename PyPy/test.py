import numpypy
import datetime
import random
import datetime
import sys

#Number of records to use
records = 4000000
try:
    records = int(sys.argv[1])
except IndexError:
    pass
print 'Testing with %s records' % records

#Number of calculations to use
num_calculations = 100
try:
    num_calculations = int(sys.argv[2])
except IndexError:
    pass
print 'Testing with %s calculations' %  num_calculations


#-- Setup dummy data
speeds = []
start = datetime.datetime.now()
data1 = []
data2 = []
for i in xrange(records):
    data1.append(random.random() * 200000)
    data2.append(random.random() * 200000)

speeds.append(datetime.datetime.now() - start)
print 'Setup dummy data in %s' % (speeds[-1])

# -- Numpy Array
start = datetime.datetime.now()
print 'Setting up numpy arrays'
incomeArray = numpypy.array(data1, dtype=numpypy.float32)
print 'turned to array (1/2)'
capArray = numpypy.array(data2, dtype=numpypy.float32)
print 'turned to array (2/2)'

speeds.append(datetime.datetime.now() - start)
print 'Setup two numpy arrays in %s' % (speeds[-1])

print '---------> Actual speed tests <-----------'
start = datetime.datetime.now()

for i in xrange(records):
    for j in xrange(num_calculations):
        #Do a dummy calculation n times
        dummy = data1[i] * data2[i] + (0.05 * data1[i]) * (1.08 / data2[i]) * (0.02 * (0.0485 * data1[i])) + ((data1[i] / data2[i]) + (0.02 * 0.02 * 0.02 * data1[i])) - (data2[i] / 2)

speeds.append(datetime.datetime.now() - start)
print '>>> Done: %s' % (speeds[-1])

# Write to file
import os
data_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../data.csv'), 'a')
data_file.write('PyPy Numpy,%s,%s,%s\n' % (
    speeds[-1], records, num_calculations
))
data_file.close()

#print '>>>>>>>>>> Done: %d' % ([a.total_seconds() for a in speeds])
