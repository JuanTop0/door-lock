# Door-assistant

### App for mongoose os.

### RFID and web controlled door.

### How to bootsrap:
```
mos build --arch esp8266

mos flash && mos console 
```
### How to open door: 
```
 mos call Door.Open

```
### How to create RPC user: 
```
 mos call RPC.Add_user '{"user": "usario", "pass": "tranca"}'

```

### How to disable door: 
```
mos config-set door.enable="false"
```
### How to run integration tests: 
with ESP8266 connected to USB:
```
./integration_tests.py 
```
