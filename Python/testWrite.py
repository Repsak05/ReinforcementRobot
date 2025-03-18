import subprocess

ps_command = '''
[System.IO.Ports.SerialPort]::new("COM3", 9600, "None", 8, "One") | ForEach-Object {
    $_.Open()
    $_.WriteLine("123")   # Replace "123" with the number you want to send
    $_.Close()
}
'''

subprocess.run(["powershell", "-Command", ps_command])
