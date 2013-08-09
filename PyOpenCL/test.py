import pyopencl as cl
import numpy
import sys
import os
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

from util import timing

# User input
# ---------------------------------------
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

# Setup OpenCL test
# ---------------------------------------
class CL:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)

    def load_program(self):
        ''' Load or create a .cl program to use
        '''
        ##Could read program from file:
        #   (also, accept filename as a parameter)
        #f = open(filename, 'r')
        #fstr = "".join(f.readlines())

        #Generate a .cl program
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

    def setup_buffers(self):
        #Here we set up the data arrays and buffers. This is NOT counted
        #   in the performance metrics, as on the server this would only need
        #   to happen once

        #initialize client side (CPU) arrays
        timing.timings.start('buffer')
        print 'Setting up data arrays'
        self.data1 = numpy.array(xrange(num_records), dtype=numpy.float32)
        self.data2 = numpy.array(xrange(num_records), dtype=numpy.float32)
        timing.timings.stop('buffer')
        print 'Done setting up two numpy arrays in %s ms | (%s seconds)' % (
            timing.timings.timings['buffer']['timings'][-1],
            timing.timings.timings['buffer']['timings'][-1] / 1000
        )

        #create OpenCL buffers
        timing.timings.start('buffer')

        mf = cl.mem_flags
        self.data1_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.data1)
        self.data2_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.data2)
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.data2.nbytes)
        timing.timings.stop('buffer')
        print 'Done setting up buffers in %s ms' % (
            timing.timings.timings['buffer']['timings'][-1]
        )

    def execute(self):
        ''' This handles the actual execution for the processing, which would
        get executed on each request - this is where we care about the
        performance
        '''
        timing.timings.start('execute')

        # Start the program
        self.program.worker(self.queue, self.data1.shape, None, self.data1_buf, self.data2_buf, self.dest_buf)

        # Get an empty numpy array in the shape of the original data
        result = numpy.empty_like(self.data1)

        #Wait for result
        cl.enqueue_read_buffer(self.queue, self.dest_buf, result).wait()

        #show timing info
        timing.timings.stop('execute')
        finish = timing.timings.timings['execute']['timings'][-1]
        print '<<< DONE in %s' % (finish)

        #Open data file to append to
        data_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../data.csv'), 'a')
        data_file.write('PyOpenCl %s,%s,%s,%s\n' % (
            process_type, finish, num_records, num_calculations,
        ))
        data_file.close()

# Execute it
# ---------------------------------------
if __name__ == "__main__":
    example = CL()
    example.load_program()
    example.setup_buffers()

    for i in xrange(num_iterations):
        print '>>> Exceuting... (%s of %s)' % (i+1, num_iterations)
        example.execute()

    timer = timing.timings.timings['execute']
    avg = (timer['total'] ) / timer['count']

    print 'DONE with PyOpenCL tests. %s records | %s calculations each' % (
        locale.format("%d", num_records, grouping=True),
        num_calculations,
    )
    print 'Average time for execute: %s milliseconds | (%s seconds)' % (avg, avg / 1000)
