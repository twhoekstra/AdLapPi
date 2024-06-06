# AdLapPi
Controller for the AdLap XYZ stage

### Convenient tools

Connecting to the Raspberry Pi via SSH
```shell
ssh adlap@raspberrypi.local
```

For getting serial USB devices (i.e. the Arduinos):
```shell
python -m serial.tools.list_ports
```

### Bluetooth connection to the controller


1. On the raspberry pi
```shell
bluetoothctl 
```

```shell
discoverable on
pairable on
agent on
default-agent
```

2. Turn on your Xbox Wireless Controller by pressing the Xbox button
3. Press and hold the Pair button on your controller for three seconds (the Xbox button will start flashing rapidly).
 
4. On the Raspberry Pi:
```shell
scan on
```
5. The controller should appear in the list, e.g.:
```shell
[NEW] 40:8E:2C:4E:4F:01 Xbox Wireless Controller
```

6. Pair using:

```shell
pair 40:8E:2C:4E:4F:01
```

7. If successful, the terminal should  look like:

```shell
[Xbox Wireless Controller]#
```

8. Exit the Bluetooth tool using:
```shell
quit
```
