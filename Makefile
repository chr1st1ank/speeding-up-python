CPP_CYTHON_DIR=pyspeed/cpp_cython
CPP_CYTHON_LIB=mergesortcpp.cpython-39-x86_64-linux-gnu.so
CPP_PYB11_DIR=pyspeed/cpp_pyb11
CPP_PYB11_LIB=pyspeed_pyb11.cpython-39-x86_64-linux-gnu.so

build: ${CPP_CYTHON_DIR}/${CPP_CYTHON_LIB} ${CPP_PYB11_DIR}/${CPP_PYB11_LIB} build_rust

${CPP_CYTHON_DIR}/${CPP_CYTHON_LIB}: ${CPP_CYTHON_DIR}/mergesort.cpp ${CPP_CYTHON_DIR}/mergesort.hpp ${CPP_CYTHON_DIR}/mergesortcpp.pxd ${CPP_CYTHON_DIR}/mergesortcpp.pyx
	cd ${CPP_CYTHON_DIR}; poetry run python setup.py build_ext --inplace

${CPP_PYB11_DIR}/${CPP_PYB11_LIB}: ${CPP_PYB11_DIR}/mergesort.cpp ${CPP_PYB11_DIR}/mergesort.hpp ${CPP_PYB11_DIR}/pyspeed.cpp
	cd ${CPP_PYB11_DIR}; poetry run python setup.py build_ext --inplace

build_rust:
	cargo build --release
	rm -f ./pyspeed/pyspeed_rust.so
	ln -s ../target/release/libpyspeed_rust.so ./pyspeed/pyspeed_rust.so

build_rust_debug:
	cargo build
	rm -f ./pyspeed/pyspeed_rust.so
	ln -s ../target/debug/libpyspeed_rust.so ./pyspeed/pyspeed_rust.so

clean:
	rm ${CPP_CYTHON_DIR}/${CPP_CYTHON_LIB}
	rm -rf ${CPP_CYTHON_DIR}/build
	rm ${CPP_CYTHON_DIR}/pyspeed/**/*.so

	rm ${CPP_PYB11_DIR}/${CPP_PYB11_LIB}
	rm -rf ${CPP_PYB11_DIR}/build
	rm -rf ${CPP_PYB11_DIR}/.objs
	rm -rf ${CPP_PYB11_DIR}/obj
