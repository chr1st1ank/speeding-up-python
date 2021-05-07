#!/bin/sh
cargo build --release
rm -f ./pyspeed/pyspeed_rust.so
ln -s ../target/release/libpyspeed_rust.so ./pyspeed/pyspeed_rust.so
