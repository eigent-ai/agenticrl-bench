.PHONY: compile run clean

compile:
	javac LogAnalyzer.java

run: compile
	java LogAnalyzer data/messages.txt 8 15 data/output.csv

clean:
	rm -f *.class data/output.csv
