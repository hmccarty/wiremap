# WireMap

Small script to periodically collect WAN IP and visualize in Hilbert curve

## Start collection

```
crontab -e
```

Add the following line:
```
*/5 * * * * <location of script>/collect.py
```

## Visualize

```
./plot.py
```

> Even ipv4 takes a while, so TODO: Optimize / allow subset display