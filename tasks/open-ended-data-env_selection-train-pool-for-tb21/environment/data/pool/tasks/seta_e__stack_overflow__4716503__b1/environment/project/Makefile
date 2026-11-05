.PHONY: compile run clean

compile:
	gcc -o log_analyzer log_analyzer.c

run: compile
	./log_analyzer data/messages.txt 8 15 data/output.csv

clean:
	rm -f log_analyzer data/output.csv
