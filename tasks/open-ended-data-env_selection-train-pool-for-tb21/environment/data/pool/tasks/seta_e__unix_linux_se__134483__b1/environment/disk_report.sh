#!/bin/bash
source /opt/diskmon/disks.conf
REPORT_DIR=/var/log/diskmon
mkdir -p $REPORT_DIR

echo "Disk Status Report" > $REPORT_DIR/report.txt
echo "Generated: $(date)" >> $REPORT_DIR/report.txt
echo "========================" >> $REPORT_DIR/report.txt

for disk in sda1 sdb1; do
    echo "" >> $REPORT_DIR/report.txt
    echo "Device: /dev/$disk" >> $REPORT_DIR/report.txt
    df -h /dev/$disk >> $REPORT_DIR/report.txt 2>&1
    if [ $? -ne 0 ]; then
        echo "WARNING: Device /dev/$disk not available" >> $REPORT_DIR/report.txt
    fi
done

echo "" >> $REPORT_DIR/report.txt
echo "Configured roles:" >> $REPORT_DIR/report.txt
echo "  DATA: /dev/$DATA_DISK ($DATA_MOUNT)" >> $REPORT_DIR/report.txt
echo "  BACKUP: /dev/$BACKUP_DISK ($BACKUP_MOUNT)" >> $REPORT_DIR/report.txt
echo "Report generation complete"
