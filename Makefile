all: test-pyopencl

test-pyopencl:
	#Run some pyopencl tests
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py 40000000 100
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py 40000000 30
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py 4000000 100
	@export PYOPENCL_CTX=0 && python PyOpenCL/test.py 4000000 30

clear:
	@echo "" > data.csv
