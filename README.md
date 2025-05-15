# EC2 Port Compliance Checker

This Python script audits Amazon EC2 instances to verify whether **ports 80 (HTTP)** and **443 (HTTPS)** are open in associated security groups. It generates a CSV report summarizing the open/closed status of these ports per instance.

---

## 🔍 Purpose

Ensuring that essential ports (like 80 and 443) are open is critical for instances that host web applications. This script helps verify compliance across your EC2 fleet and identify misconfigured security groups.

---

## 🧰 Features

- Retrieves all **running and stopped EC2 instances**
- Checks associated **Security Groups** for rules allowing access to ports 80 and 443
- Outputs a CSV report with:
  - Instance ID, Name, Public/Private IPs
  - Open/Closed status for each port
  - Associated Security Group IDs
  - Overall port compliance status

---

## 🚀 Usage

### 1. **Prerequisites**
- Python 3.x
- `boto3` installed:
  ```bash
  pip install boto3
  ```
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)

### 2. **Run the Script**
```bash
python PortCheck.py
```

This will create a file named:
```
ec2_port_check_report.csv
```

---

## 📦 Sample Output (CSV)

| Instance ID | Name       | State  | Public IP | Private IP | Security Groups     | Port 80 | Port 443 | Status           |
|-------------|------------|--------|-----------|------------|---------------------|---------|-----------|------------------|
| i-012abcde  | WebServer1 | running| 52.x.x.x  | 10.0.1.5   | sg-0abc12de         | Open    | Closed    | Missing [443]    |
| i-0def6789  | AppServer2 | stopped| N/A       | 10.0.2.7   | sg-0def34gh, sg-xyz | Closed  | Closed    | Missing [80,443] |

---

## 📌 Notes

- The script checks only **inbound rules**.
- Only TCP ports in defined ranges (e.g., 80–80) are inspected; wildcard or custom protocol rules may not be reflected precisely.
- You can adjust the `REQUIRED_PORTS` list at the top of the script for other port checks (e.g., SSH: 22).

---

## 🔐 Permissions Required

The AWS credentials used must have the following permissions:

- `ec2:DescribeInstances`
- `ec2:DescribeSecurityGroups`

---

## 🔄 Customization

Want to audit more ports?
Open the script and modify:
```python
REQUIRED_PORTS = [80, 443]
```

To:
```python
REQUIRED_PORTS = [22, 80, 443]
```

---

## 📝 License

MIT or your preferred license.

---

## 👤 Author

Script developed by Brenden Turco as part of AWS security and compliance auditing toolkit.
