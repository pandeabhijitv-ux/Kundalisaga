# AstroKnowledge - Operations Guide
## Starting, Stopping, and Maintenance

---

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Starting the Application](#starting-the-application)
3. [Stopping the Application](#stopping-the-application)
4. [Monitoring](#monitoring)
5. [Maintenance Tasks](#maintenance-tasks)
6. [Troubleshooting](#troubleshooting)
7. [Backup & Recovery](#backup--recovery)

---

## 🖥️ System Requirements

### Minimum Requirements
- **Python**: 3.10 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 2 GB free space
- **OS**: Windows 10/11, Linux, macOS

### Required Services
- **Ollama** (for AI/LLM capabilities) - Optional if using remote LLM
- **Internet Connection** (for initial setup and external API calls)

---

## 🚀 Starting the Application

### Method 1: Using Virtual Environment (Recommended)

#### On Windows (PowerShell):
```powershell
# Navigate to project directory
cd C:\AstroKnowledge

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start the application
streamlit run app.py
```

#### On Windows (Command Prompt):
```cmd
cd C:\AstroKnowledge
.venv\Scripts\activate
streamlit run app.py
```

#### On Linux/macOS:
```bash
cd /path/to/AstroKnowledge
source .venv/bin/activate
streamlit run app.py
```

### Method 2: Direct Start (If environment is configured)
```powershell
# From project root
C:/AstroKnowledge/.venv/Scripts/streamlit.exe run app.py
```

### Access the Application
Once started, the application will be available at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://[YOUR_IP]:8501

The terminal will display these URLs. Click on the Local URL or copy it to your browser.

---

## 🛑 Stopping the Application

### Normal Shutdown
1. Go to the terminal where Streamlit is running
2. Press `Ctrl + C` (on Windows/Linux/macOS)
3. Wait for the graceful shutdown message

### Force Stop (If application hangs)
```powershell
# Find the process
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"}

# Kill the process (replace PID with actual process ID)
Stop-Process -Id [PID] -Force
```

On Linux/macOS:
```bash
# Find the process
ps aux | grep streamlit

# Kill the process
kill -9 [PID]
```

---

## 📊 Monitoring

### Application Health Checks

#### Check if Application is Running
```powershell
# Check if port 8501 is listening
Test-NetConnection -ComputerName localhost -Port 8501
```

On Linux:
```bash
netstat -tuln | grep 8501
```

#### View Real-time Logs
Logs are stored in: `./logs/app.log`

```powershell
# View logs (Windows PowerShell)
Get-Content -Path .\logs\app.log -Wait -Tail 50

# View logs (Linux/macOS)
tail -f ./logs/app.log
```

### Key Metrics to Monitor
- **Response Time**: Application should load within 2-3 seconds
- **Memory Usage**: Should not exceed 1-2 GB under normal load
- **Disk Space**: Monitor `./data/` directory size
- **Error Logs**: Check logs for ERROR or CRITICAL messages

---

## 🔧 Maintenance Tasks

### Daily Maintenance

#### 1. Check Logs
```powershell
# Check for errors in last 24 hours
Get-Content .\logs\app.log | Select-String "ERROR|CRITICAL" | Select-Object -Last 20
```

#### 2. Monitor Disk Space
```powershell
# Check data directory size
Get-ChildItem -Path .\data -Recurse | Measure-Object -Property Length -Sum
```

### Weekly Maintenance

#### 1. Clean Old Session Data
```powershell
# Clear old OTP codes and expired sessions
# Navigate to data directory
cd data\users

# Backup before cleaning
Copy-Item sessions.json sessions_backup_$(Get-Date -Format 'yyyyMMdd').json
Copy-Item otp_codes.json otp_codes_backup_$(Get-Date -Format 'yyyyMMdd').json
```

#### 2. Update Dependencies
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Check for outdated packages
pip list --outdated

# Update specific package (if needed)
pip install --upgrade [package-name]
```

#### 3. Database Cleanup
```powershell
# Clean vector database cache (if needed)
# Backup first
Copy-Item -Path .\data\vector_db -Destination .\data\vector_db_backup_$(Get-Date -Format 'yyyyMMdd') -Recurse
```

### Monthly Maintenance

#### 1. Full System Backup
```powershell
# Backup entire data directory
$backupPath = ".\backups\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupPath -Force
Copy-Item -Path .\data\* -Destination $backupPath -Recurse
Copy-Item -Path .\config\config.yaml -Destination $backupPath
Copy-Item -Path .\logs\app.log -Destination $backupPath
```

#### 2. Review Configuration
- Review `config/config.yaml` for any needed updates
- Check payment settings if enabled
- Verify email configuration if enabled

#### 3. Performance Optimization
```powershell
# Clear old log files (keep last 30 days)
Get-ChildItem -Path .\logs\*.log | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
```

---

## 🔍 Troubleshooting

### Application Won't Start

#### Issue: "streamlit: command not found"
**Solution**:
```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Reinstall Streamlit
pip install --force-reinstall streamlit
```

#### Issue: "Port 8501 already in use"
**Solution**:
```powershell
# Find process using port 8501
Get-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess

# Kill the process
Stop-Process -Id [PID] -Force

# Or start on different port
streamlit run app.py --server.port 8502
```

#### Issue: "Module not found"
**Solution**:
```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Reinstall requirements
pip install -r requirements.txt
```

### Application Running Slow

#### Check Memory Usage
```powershell
# Windows
Get-Process streamlit | Select-Object ProcessName, @{Name="Memory(MB)";Expression={[math]::round($_.WS/1MB,2)}}
```

#### Clear Cache
```powershell
# Stop application
# Delete Streamlit cache
Remove-Item -Path "$env:USERPROFILE\.streamlit\cache" -Recurse -Force -ErrorAction SilentlyContinue
```

### Database Connection Issues

#### Reset Vector Database
```powershell
# Backup first
Copy-Item -Path .\data\vector_db -Destination .\data\vector_db_backup -Recurse

# Remove and rebuild
Remove-Item -Path .\data\vector_db -Recurse -Force

# Restart application - it will rebuild the database
```

### Email Service Not Working

1. Check `config/config.yaml`:
   - Verify `email.enabled: true`
   - Check SMTP credentials
   - Verify sender email and password

2. Test SMTP connection:
```python
# Run in Python to test
python -c "
from src.auth.email_sender import EmailSender
sender = EmailSender()
print('Email configured:', sender.is_configured())
"
```

---

## 💾 Backup & Recovery

### What to Backup

#### Critical Data
- `data/users/` - User accounts and sessions
- `data/user_data/` - User profiles and charts
- `data/payments/` - Transaction history
- `config/config.yaml` - Configuration settings

#### Optional Data
- `data/knowledge_base/` - Document embeddings (can be regenerated)
- `data/vector_db/` - Vector database (can be rebuilt)
- `logs/` - Log files

### Backup Script (Windows)
```powershell
# Create backup directory
$backupDir = ".\backups\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force

# Backup critical data
Copy-Item -Path .\data\users -Destination $backupDir\users -Recurse
Copy-Item -Path .\data\user_data -Destination $backupDir\user_data -Recurse
Copy-Item -Path .\data\payments -Destination $backupDir\payments -Recurse
Copy-Item -Path .\config\config.yaml -Destination $backupDir\

# Compress backup
Compress-Archive -Path $backupDir -DestinationPath "$backupDir.zip"
Remove-Item -Path $backupDir -Recurse

Write-Host "Backup completed: $backupDir.zip"
```

### Restore from Backup
```powershell
# Stop the application first
# Ctrl+C in the terminal

# Expand backup
Expand-Archive -Path ".\backups\backup_YYYYMMDD_HHMMSS.zip" -DestinationPath ".\restore_temp"

# Restore data
Copy-Item -Path ".\restore_temp\users" -Destination ".\data\" -Recurse -Force
Copy-Item -Path ".\restore_temp\user_data" -Destination ".\data\" -Recurse -Force
Copy-Item -Path ".\restore_temp\payments" -Destination ".\data\" -Recurse -Force
Copy-Item -Path ".\restore_temp\config.yaml" -Destination ".\config\" -Force

# Cleanup
Remove-Item -Path ".\restore_temp" -Recurse

# Restart application
```

---

## 🔄 Application Updates

### Update Application Code
```powershell
# Stop application
# Ctrl+C

# Backup current version
$date = Get-Date -Format 'yyyyMMdd'
Copy-Item -Path . -Destination "..\AstroKnowledge_backup_$date" -Recurse

# Pull latest changes (if using git)
git pull origin main

# Update dependencies
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt --upgrade

# Restart application
streamlit run app.py
```

---

## 📞 Support

### Log Files Location
- **Application Logs**: `./logs/app.log`
- **Streamlit Logs**: `%USERPROFILE%\.streamlit\logs\` (Windows)

### Before Reporting Issues
1. Check the logs for error messages
2. Verify configuration settings
3. Ensure all dependencies are installed
4. Try restarting the application

### Collect Diagnostic Information
```powershell
# System information
python --version
pip list > installed_packages.txt

# Recent errors
Get-Content .\logs\app.log | Select-String "ERROR|CRITICAL" | Select-Object -Last 50 > recent_errors.txt
```

---

## ⚙️ Environment Variables

### Optional Environment Variables
Create a `.env` file in the project root for sensitive data:

```env
# Email Configuration
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Payment Configuration
UPI_ID=your-upi@bank
UPI_NAME=YourName

# API Keys (if using external services)
OPENAI_API_KEY=your-api-key
ANTHROPIC_API_KEY=your-api-key
```

**Note**: Never commit `.env` file to version control!

---

## 🔐 Security Best Practices

1. **Keep dependencies updated**: Regularly update packages for security patches
2. **Secure credentials**: Use environment variables for sensitive data
3. **Backup regularly**: Automated daily backups recommended
4. **Monitor logs**: Check for suspicious activities
5. **Restrict access**: Use firewall rules if exposing to network
6. **HTTPS**: Use reverse proxy (nginx/Apache) for production with SSL

---

## 📈 Performance Tuning

### Streamlit Configuration
Create `.streamlit/config.toml`:

```toml
[server]
maxUploadSize = 200  # Max upload size in MB
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### System Resources
- Recommended RAM: 8GB
- Recommended CPU: 4 cores
- SSD recommended for better performance

---

**Last Updated**: December 21, 2025  
**Version**: 1.0.0
