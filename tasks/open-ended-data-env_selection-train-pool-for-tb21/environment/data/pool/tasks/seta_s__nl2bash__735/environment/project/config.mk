# Shared build configuration
TOOLCHAIN_PREFIX = /opt/old-toolchain
CC = $(TOOLCHAIN_PREFIX)/bin/gcc
CXX = $(TOOLCHAIN_PREFIX)/bin/g++
AR = $(TOOLCHAIN_PREFIX)/bin/ar
COMMON_CFLAGS = -Wall -Wextra -fPIC
COMMON_LDFLAGS =
