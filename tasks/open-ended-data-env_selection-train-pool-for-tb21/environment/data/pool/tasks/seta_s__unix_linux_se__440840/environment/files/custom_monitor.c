#include <linux/module.h>
#include <linux/kernel.h>
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Custom system monitoring module");
MODULE_AUTHOR("sysadmin");
static int __init custom_monitor_init(void) { return 0; }
static void __exit custom_monitor_exit(void) {}
module_init(custom_monitor_init);
module_exit(custom_monitor_exit);
