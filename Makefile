SUBDIRS = Pylib_fftw Griding
.PHONY: all  
all:  
	@list='$(SUBDIRS)';\
		for subdir in $$list; \
		do echo "cd in $$subdir"; \
		$(MAKE) -C $$subdir ; \
		done  
.PHONY: clean  
clean:  
	@list='$(SUBDIRS)';\
		for subdir in $$list; \
		do echo "Clean in $$subdir"; \
		$(MAKE) -C $$subdir clean; \
		done  
