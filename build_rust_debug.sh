#!/bin/sh
cargo build
rm -f ./pyspeed/pyspeed_rust.so
ln -s ../target/debug/libpyspeed_rust.so ./pyspeed/pyspeed_rust.so
