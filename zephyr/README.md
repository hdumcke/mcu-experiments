# Example Application

## Build

```
./example-app.sh
```

## menuconfig

```
cd my-workspace/example-application/
west build -t menuconfig
```

## Device Tree

```
pip install dtsh
dtsh
find --with-bus * -T --format NYCd
tree --format Nc
q
```

## UART0

```
screen /dev/cu.usbserial-A50285BI 115200
```

# Example Application with GPIO in/out

## Build

```
./button.sh
```
