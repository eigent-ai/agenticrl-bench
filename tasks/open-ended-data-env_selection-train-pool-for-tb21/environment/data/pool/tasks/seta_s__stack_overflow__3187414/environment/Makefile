include config.mk

BENCHMARKS = array_bench math_bench poly_bench
OPT_LEVELS = O2 O3
COMPILERS = gcc clang

BUILDDIR = build

ALL_TARGETS =

define make_target
$(BUILDDIR)/$(1)_$(2)_$(3): src/$(1).cpp | $(BUILDDIR)
	$$($(call compiler_var,$(2))) -$(3) $$(CXXFLAGS) $$(LDFLAGS) -o $$@ $$<

ALL_TARGETS += $(BUILDDIR)/$(1)_$(2)_$(3)
endef

compiler_var = $(if $(filter gcc,$(1)),GCC_CXX,CLANG_CXX)

$(foreach b,$(BENCHMARKS),$(foreach c,$(COMPILERS),$(foreach o,$(OPT_LEVELS),$(eval $(call make_target,$(b),$(c),$(o))))))

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

.PHONY: all clean
all: $(ALL_TARGETS)

clean:
	rm -rf $(BUILDDIR) output
