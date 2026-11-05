# Meeting Notes — Storage Working Group

## 2024-11-01

- Reviewed current USB backup schedule
- Discussed udev trigger reliability on hot-plug events
- Action items:
  - Confirm `rsync` flags are correct for incremental mode
  - Check modprobe configuration on workstation nodes
  - Update runbook with new mount point locations

## 2024-11-08

- Confirmed backup path is `/mnt/usb` across all nodes
- Script permissions verified (chmod 755)
- Log rotation set to 30-day retention
