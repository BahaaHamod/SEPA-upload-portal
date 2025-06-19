@echo off
echo Starte SEPA-Upload-Portal mit Waitress...
cd /d %~dp0
"C:\Users\bahaa\AppData\Roaming\Python\Python313\Scripts\waitress-serve.exe" --port=5000 app:app
pause
