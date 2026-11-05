:set nomore
:set magic

:%s/\d{6}/[ORD-&]/g

:%s/\n\n+/\r\r/g

:w! /home/analyst/output/processed_report.txt
:q!
