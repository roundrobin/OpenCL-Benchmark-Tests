# PyOpenCL Benchmark Tests #
Some dummy performance tests for PyOpenCL, Python, PyPy, etc. Used to get an idea of the magnitude of performance for different implmentation options for Outline.com's budget simulator


The problem we are solving is running a series of calcluations on millions of records as fast as possible.  Record data is static, but input variables come from the client.

## Usage ##
Run `make` to run the tests.  It will run each test and output results to a data.csv file.  To run individual tests alone, see below

### pyopencl tests ###
To run, run `test.py` in the PyOpenCL. It takes two arguments: number of records and number of calculations. e.g.,
    `python test.py 4000000 100` to run 100 calculations on 4 million records

Note: We don't care about how long it takes to create the numpy arrays - in our usecase, we'll be setting it up once and leaving it in memory, calling execute whenever a request comes in.

** Shoutout to @enjalot for his [OpenCL tutorials](http://enja.org/opencl/) **
