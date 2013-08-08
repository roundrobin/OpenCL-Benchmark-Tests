import pyopencl as cl
import numpy
import datetime
import sys

#Number of num_records to use
num_records = 4000000
try:
    num_records = int(sys.argv[1])
except IndexError:
    pass
print 'Testing with %s num_records' % num_records

#Number of calculations to use
num_calculations = 100
try:
    num_calculations = int(sys.argv[2])
except IndexError:
    pass
print 'Testing with %s calculations' %  num_calculations

#Number of iterations
num_iterations = 1
try:
    num_iterations = int(sys.argv[3])
except IndexError:
    pass

#Type (CPU or GPU)
process_type = 'GPU'
try:
    process_type = sys.argv[4]
except IndexError:
    pass
print 'Testing on %s' %  process_type

class CL:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)

    def loadProgram(self):
        ##Could read program from file:
        #   (also, accept filename as a parameter)
        #f = open(filename, 'r')
        #fstr = "".join(f.readlines())

        #Generate it
        program = """__kernel void worker(__global float* data1, __global float* data2, __global float* result)
        {
            unsigned int i = get_global_id(0);
            float d1 = data1[i];
            float d2 = data2[i];
        """

        # Generate n calculations
        for i in xrange(num_calculations):
            # This is just a series of nonsenscial operations to get an idea of
            #   what performance might look like. Our calculations will involve
            #   less operations
            program += """result[i] = d1 * d2 + (0.05 * d1) * (1.08 / d2) * (0.02 * (0.0485 * d2)) + ((d1 / d2) + (0.02 * 0.02 * 0.02 * d1)) - (d2 / 2);
            """

        program += "}" 

        #create the program
        self.program = cl.Program(self.ctx, program).build()

    def setupBuffers(self):
        #Here we set up the data arrays and buffers. This is NOT counted
        #   in the performance metrics, as on the server this would only need
        #   to happen once

        #initialize client side (CPU) arrays
        start = datetime.datetime.now()
        print 'Setting up data arrays'
        self.data1 = numpy.array(xrange(num_records), dtype=numpy.float32)
        self.data2 = numpy.array(xrange(num_records), dtype=numpy.float32)
        print 'Done setting up two numpy arrays in %s' % (datetime.datetime.now() - start)

        start = datetime.datetime.now()
        mf = cl.mem_flags
        #create OpenCL buffers
        self.data1_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.data1)
        self.data2_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.data2)
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.data2.nbytes)
        print 'Done setting up buffers in %s' % (datetime.datetime.now() - start)

    def execute(self):
        ''' This handles the actual execution for the processing, which would
        get executed on each request - this is where we care about the
        performance
        '''
        start = datetime.datetime.now()
        self.program.worker(self.queue, self.data1.shape, None, self.data1_buf, self.data2_buf, self.dest_buf)
        # Get an empty numpy array in the shape of the original data
        result = numpy.empty_like(self.data1)
        cl.enqueue_read_buffer(self.queue, self.dest_buf, result).wait()
        finish = datetime.datetime.now() - start
        print 'DONE in ::::::::: %s ::::::::' % (finish)
        print 'Result: ', result
        print '%s items' % len(result)

        #Open data file to append to
        import os
        data_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../data.csv'), 'a')
        data_file.write('PyOpenCl %s,%s,%s,%s\n' % (
            process_type, finish, num_records, num_calculations
        ))
        data_file.close()

if __name__ == "__main__":
    example = CL()
    example.loadProgram()
    example.setupBuffers()

    for i in xrange(num_iterations):
        print '>>> Exceuting... (%s of %s)' % (i+1, num_iterations)
        example.execute()
