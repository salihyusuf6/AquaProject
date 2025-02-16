import os
# Aynı dizindeki dosyanın adı ve yolu
vbs_name = input("your_vbs_script_name->")
mainFilePath = os.path.dirname(os.path.abspath(__file__))
script_name = input("Dosyanın adı->")

vbs_content = f"""set objshell = CreateObject("WScript.Shell")
objshell.Run "cmd.exe /c cd /d {mainFilePath} & node {script_name}",0,True"""
startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
# VBS dosyasını startup klasörüne kaydediyoruz
with open(f"{startup_folder}\\{vbs_name}.vbs", "w", encoding="utf-8") as dosya:
    dosya.write(vbs_content)
