# snzr

Sneeze Tracking App

## Quick Startup

run `go run .`

## API

Base URL: `http://localhost:8080`

**Windows PowerShell:** In PowerShell, `curl` is an alias for `Invoke-WebRequest` and uses different syntax. Use **`curl.exe`** for the bash examples below, or use the PowerShell examples in each section.

### List all sneezes

**Bash / Git Bash / WSL:**
```bash
curl http://localhost:8080/sneeze
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:8080/sneeze -Method Get
```

### Get sneeze by ID

**Bash:**
```bash
curl http://localhost:8080/sneeze/1
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:8080/sneeze/1 -Method Get
```

### Create sneeze

**Bash:**
```bash
curl -X POST http://localhost:8080/sneeze \
  -H "Content-Type: application/json" \
  -d "{\"notes\":\"After dusting\",\"location\":\"Bedroom\",\"volume\":2}"
```

**PowerShell:**
```powershell
$body = '{"notes":"After dusting","location":"Bedroom","volume":2}'
Invoke-RestMethod -Uri http://localhost:8080/sneeze -Method Post -Body $body -ContentType "application/json"
```

With optional `occurred_at` (ISO8601), PowerShell:
```powershell
$body = '{"notes":"Pollen","occurred_at":"2025-02-28T14:30:00Z","location":"Garden","volume":3}'
Invoke-RestMethod -Uri http://localhost:8080/sneeze -Method Post -Body $body -ContentType "application/json"
```

### Update sneeze

**Bash:**
```bash
curl -X PUT http://localhost:8080/sneeze/1 \
  -H "Content-Type: application/json" \
  -d "{\"notes\":\"Updated notes\",\"occurred_at\":\"2025-03-01T10:00:00Z\",\"location\":\"Office\",\"volume\":4}"
```

**PowerShell:**
```powershell
$body = '{"notes":"Updated notes","occurred_at":"2025-03-01T10:00:00Z","location":"Office","volume":4}'
Invoke-RestMethod -Uri http://localhost:8080/sneeze/1 -Method Put -Body $body -ContentType "application/json"
```

### Delete sneeze

**Bash:**
```bash
curl -X DELETE http://localhost:8080/sneeze/1
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:8080/sneeze/1 -Method Delete
```
