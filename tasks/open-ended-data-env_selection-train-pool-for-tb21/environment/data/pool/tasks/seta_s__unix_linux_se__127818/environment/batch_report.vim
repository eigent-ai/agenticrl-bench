edit /var/log/webapp/access.log
g/(?!.*\.php).*index/d
%s/\v^(.*)\" 404 (.*)$/[MISSING] \1" 404 \2/
%s/\v^(.*)\" 5\d{2} (.*)$/[ERROR] \1" 5xx \2/
w! /opt/logtools/output/report.txt
quit!
