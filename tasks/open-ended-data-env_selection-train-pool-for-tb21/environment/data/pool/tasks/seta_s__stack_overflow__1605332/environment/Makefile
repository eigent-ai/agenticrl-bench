.PHONY: all compile run clean

all: run

compile:
	mkdir -p bin
	javac -d bin src/FileChecker.java

run: compile
	java -cp bin FileChecker

clean:
	rm -f bin/*.class output/copy_transfer.bin output/copy_buffer.bin output/report.json
