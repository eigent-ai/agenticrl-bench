# Java 2D Game - Build System
CC = C:\Program Files\Java\jdk\bin\javac
SRCDIR = src
OUTDIR = classes
CLASSPATH = $(OUTDIR);$(SRCDIR)
SOURCES = $(wildcard src\game\*.java)

all: setup.bat compile

compile:
	@mkdir -p $(OUTDIR)
	"$(CC)" -cp "$(CLASSPATH)" -d $(OUTDIR) $(SOURCES)
