<domain type='kvm'>
  <name>{{NAME}}</name>
  <memory unit='MiB'>{{RAM}}</memory>
  <vcpu placement='static'>{{VCPUS}}</vcpu>
  <os>
    <type arch='x86_64' machine='pc-q35-6.2'>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
  </features>
  <on_poweroff>restart</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='{{DISK_PATH}}'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
    </interface>
    <graphics type='spice' port='{{PORT}}' tlsPort='-1' autoport='no' listen='{{LISTEN}}'>
      <listen type='address' address='{{LISTEN}}'/>
    </graphics>
    <channel type='spicevmc'>
      <target type='virtio' name='com.redhat.spice.0'/>
    </channel>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
  </devices>
</domain>
