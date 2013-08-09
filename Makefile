#ASSUMPTIONS: If running `make`, assumes you have everything installed:
#	pyopencl, numpy, pypy, node, etc.
#
#See individual targets for detailed info

# Test param config
# ---------------------------------------
# first param is num_records (how many iterations to do / rows)
# second param is how may calculations to do for each record
TEST1 = 40000000 100 1
TEST2 = 40000000 30 1
TEST3 = 4000000 100 1
TEST4 = 4000000 30 1


# Start er up
# ---------------------------------------
all: clear-data test-pyopencl-gpu test-pypy test-node
cpu: clear-data test-pyopencl-cpu test-pypy test-node

# PyOpenCL
# ---------------------------------------
#*assumes a OpenCL enabled GPU is installed as specified as context*
#If this isn't the case, run `make test-pyopencl-gpu-no-ctx`
test-pyopencl-gpu:
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
#CPU Tests - assumes cpu is context 0
#If this isn't the case, run `make test-pyopencl-cpu-no-ctx`
test-pyopencl-cpu:
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py $(TEST1) cpu
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py $(TEST2) cpu
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py $(TEST3) cpu
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py $(TEST4) cpu

test-pyopencl-cpu-no-ctx:
	@python PyOpenCL/test.py $(TEST1) cpu
	@python PyOpenCL/test.py $(TEST2) cpu
	@python PyOpenCL/test.py $(TEST3) cpu
	@python PyOpenCL/test.py $(TEST4) cpu

# PyPy
# ---------------------------------------
test-pypy:
	@pypy PyPy/test.py $(TEST1)
	@pypy PyPy/test.py $(TEST2)
	@pypy PyPy/test.py $(TEST3)
	@pypy PyPy/test.py $(TEST4)

# Node
# ---------------------------------------
test-node:
	@node Node/test.js $(TEST1)
	@node Node/test.js $(TEST2)
	@node Node/test.js $(TEST3)
	@node Node/test.js $(TEST4)

# Util
# ---------------------------------------
clear-data:
	@echo "name,time,records,calculations" > data.csv
