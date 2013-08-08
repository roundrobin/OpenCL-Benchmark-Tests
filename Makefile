#ASSUMPTIONS: If running `make`, assumes you have everything installed:
#	pyopencl, numpy, pypy, node, etc.
#
#See individual targets for detailed info

# Start er up
# ---------------------------------------
all: clear-data test-pyopencl-gpu test-pypy
cpu: clear-data test-pyopencl-cpu test-pypy

# Test param config
# ---------------------------------------
# first param is num_records (how many iterations to do / rows)
# second param is how may calculations to do for each record
TEST1 = 40000000 100
TEST2 = 40000000 30
TEST3 = 4000000 100
TEST4 = 4000000 30

# PyOpenCL
# ---------------------------------------
test-pyopencl-gpu:
	@echo "Run some pyopencl tests"
	@echo "*assumes a OpenCL enabled GPU is installed as specified as context*"
	@echo "If this isn't the case, run `make test-pyopencl-gpu-no-ctx`"
	@export PYOPENCL_CTX=1 && python PyOpenCL/test.py $(TEST1)
	@export PYOPENCL_CTX=1 && python PyOpenCL/test.py $(TEST2)
	@export PYOPENCL_CTX=1 && python PyOpenCL/test.py $(TEST3)
	@export PYOPENCL_CTX=1 && python PyOpenCL/test.py $(TEST4)

test-pyopencl-gpu-no-ctx:
	@python PyOpenCL/test.py $(TEST1)
	@python PyOpenCL/test.py $(TEST2)
	@python PyOpenCL/test.py $(TEST3)
	@python PyOpenCL/test.py $(TEST4)

# CPU Tests with OpenCL
test-pyopencl-cpu:
	@echo "CPU Tests - assumes cpu is context 0"
	@echo "If this isn't the case, run `make test-pyopencl-cpu-no-ctx`"
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py $(TEST1)
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py $(TEST2)
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py $(TEST3)
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py $(TEST4)

test-pyopencl-cpu-no-ctx:
	@python PyOpenCL/test.py $(TEST1)
	@python PyOpenCL/test.py $(TEST2)
	@python PyOpenCL/test.py $(TEST3)
	@python PyOpenCL/test.py $(TEST4)

# PyPy
# ---------------------------------------
test-pypy:
	@echo "Running some numpy + pypy tests"
	@pypy PyPy/test.py $(TEST1)
	@pypy PyPy/test.py $(TEST2)
	@pypy PyPy/test.py $(TEST3)
	@pypy PyPy/test.py $(TEST4)

# Util
# ---------------------------------------
clear-data:
	# Empty data file
	@echo "name,time,records,calculations\n" > data.csv
