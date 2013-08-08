#ASSUMPTIONS: If running `make`, assumes you have everything installed:
#	pyopencl, numpy, pypy, node, etc.
#
#See individual targets for detailed info

all: clear-data test-pyopencl-gpu test-pypy
cpu: clear-data test-pyopencl-cpu test-pypy

# PyOpenCL
# ---------------------------------------
test-pyopencl-gpu:
	#Run some pyopencl tests
	#	*assumes a OpenCL enabled GPU is installed as specified as context*
	#	If this isn't the case, run `make test-pyopencl-gpu-no-ctx`
	@export PYOPENCL_CTX=1 && python PyOpenCL/test.py 40000000 100
	@export PYOPENCL_CTX=1 && python PyOpenCL/test.py 40000000 30
	@export PYOPENCL_CTX=1 && python PyOpenCL/test.py 4000000 100
	@export PYOPENCL_CTX=1 && python PyOpenCL/test.py 4000000 30

test-pyopencl-gpu-no-ctx:
	@python PyOpenCL/test.py 40000000 100
	@python PyOpenCL/test.py 40000000 30
	@python PyOpenCL/test.py 4000000 100
	@python PyOpenCL/test.py 4000000 30

# CPU Tests with OpenCL
test-pyopencl-cpu:
	# CPU Tests - assumes cpu is context 0
	#	If this isn't the case, run `make test-pyopencl-cpu-no-ctx`
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py 40000000 100 cpu
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py 40000000 30 cpu
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py 4000000 100 cpu
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py 4000000 30 cpu

test-pyopencl-cpu-no-ctx:
	@python PyOpenCL/test.py 40000000 100 cpu
	@python PyOpenCL/test.py 40000000 30 cpu
	@python PyOpenCL/test.py 4000000 100 cpu
	@python PyOpenCL/test.py 4000000 30 cpu

# PyPy
# ---------------------------------------
test-pypy:
	#Run some numpy + pypy tests
	@pypy PyPy/test.py 40000000 100
	@pypy PyPy/test.py 40000000 30
	@pypy PyPy/test.py 4000000 100
	@pypy PyPy/test.py 4000000 30

# Util
# ---------------------------------------
clear-data:
	# Empty data file
	@echo "name,time,records,calculations\n" > data.csv
