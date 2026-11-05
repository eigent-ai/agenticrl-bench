#!/bin/bash
cd /home/user/file-organizer
javac -d bin src/*.java
java -cp bin FileOrganizer data/records.csv output
