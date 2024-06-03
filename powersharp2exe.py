#!/usr/bin/python3
#Coded by v1k (Radostin Dimov)
import subprocess
import string
import sys
import re
import os
import base64
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox, QComboBox, QFileDialog, QMenuBar
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtGui import QIcon, QAction


csharp_template = '''using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;

//replacemeatitle
//replacemeadescr
[assembly: AssemblyConfiguration("")]
//replacompname
//replacemepname
//replacemecright
[assembly: AssemblyTrademark("")]
[assembly: AssemblyCulture("")]
//replacemeaversion
//replacemefversion

class Program
{
    static void Main(string[] args)
    {
        string base64Script = "#replacemepscommand";
        string tempFilePath = Path.GetTempFileName();

        File.WriteAllText(tempFilePath, base64Script);

        string powerShellCommand = $@"
$command = Get-Content '{tempFilePath}' -Raw;
$decodedCommand = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($command));
Invoke-Expression $decodedCommand;";

        Process process = new Process();
        ProcessStartInfo info = new ProcessStartInfo
        {
            WindowStyle = ProcessWindowStyle.Hidden,
            FileName = "powershell.exe",
            Arguments = $"-NoProfile -WindowStyle hidden -Command \\\"{powerShellCommand}\\\"",
            UseShellExecute = false,
            CreateNoWindow = true
        };
        process.StartInfo = info;
        process.Start();
        process.WaitForExit();

        File.Delete(tempFilePath);
    }
}
'''


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PowerSharp2exe")
        self.setWindowIcon(QIcon("img/powersharp2exe.png"))
        layout = QVBoxLayout()
        
        menu_bar = QMenuBar()
        pwrsharp2exe_menu = menu_bar.addMenu("powersharp2exe")
        help_menu = menu_bar.addMenu("About")
        homepage_action = QAction("Homepage", self)
        pwrsharp2exe_menu.addAction(homepage_action)
        homepage_action.triggered.connect(self.homepage)
        about_action = QAction("Overview", self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.about)
        layout.setMenuBar(menu_bar)

        powershell_layout = QHBoxLayout()
        powershell_file_label = QLabel("PowerShell Script:")
        self.powershell_file_input = QLineEdit()
        self.powershell_browse_button = QPushButton("Browse")
        self.powershell_browse_button.setFixedWidth(100)
        powershell_layout.addWidget(powershell_file_label)
        powershell_layout.addWidget(self.powershell_file_input)
        powershell_layout.addWidget(self.powershell_browse_button)
        self.powershell_browse_button.clicked.connect(self.handle_param_change)
        layout.addLayout(powershell_layout)

        iconfile_layout = QHBoxLayout()
        iconfile_label = QLabel("Icon file (Optional):")
        self.iconfile_input = QLineEdit()
        self.iconfile_browse_button = QPushButton("Browse")
        self.iconfile_browse_button.setFixedWidth(100)
        iconfile_layout.addWidget(iconfile_label)
        iconfile_layout.addWidget(self.iconfile_input)
        iconfile_layout.addWidget(self.iconfile_browse_button)
        self.iconfile_browse_button.clicked.connect(self.handle_param_change)
        layout.addLayout(iconfile_layout)

        platform_layout = QHBoxLayout()
        platform_label = QLabel("Platform:")
        platform_layout.addWidget(platform_label)
        self.platform_input = QComboBox()
        self.platform_input.addItem("AnyCPU")
        self.platform_input.addItem("x64")
        self.platform_input.addItem("x86")
        platform_layout.addWidget(self.platform_input)
        layout.addLayout(platform_layout)

        optionalfields_layout = QHBoxLayout()
        optionalfields_label = QLabel("Optional Fields:")
        optionalfields_layout.addWidget(optionalfields_label)
        layout.addLayout(optionalfields_layout)

        ver_descr_layout = QHBoxLayout()
        version_label = QLabel("Version:")
        self.version_input = QLineEdit()
        description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        ver_descr_layout.addWidget(version_label)
        ver_descr_layout.addWidget(self.version_input)
        ver_descr_layout.addWidget(description_label)
        ver_descr_layout.addWidget(self.description_input)
        layout.addLayout(ver_descr_layout)

        pname_copyr_layout = QHBoxLayout()
        pname_label = QLabel("Product Name:")
        self.pname_input = QLineEdit()
        copright_label = QLabel("Copyright:")
        self.copright_input = QLineEdit()
        pname_copyr_layout.addWidget(pname_label)
        pname_copyr_layout.addWidget(self.pname_input)
        pname_copyr_layout.addWidget(copright_label)
        pname_copyr_layout.addWidget(self.copright_input)
        layout.addLayout(pname_copyr_layout)

        console_label = QLabel("Building Console")
        layout.addWidget(console_label)
        self.console = QTextEdit()
        self.console.setMinimumSize(500, 150)
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        self.compile_button = QPushButton("Compile")
        self.compile_button.setFixedWidth(150)
        self.compile_button.clicked.connect(self.compile)
        layout.addWidget(self.compile_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(layout)

    def homepage(self):
        QMessageBox.about(self, "Homepage", "PowerSharp2exe Github repo:\n\nhttps://github.com/d1mov/powersharp2exe")

    def about(self):
        QMessageBox.about(self, "About", "PowerSharp2exe 1.0\n\nPython GUI based tool that converts powershell scripts to exe files utilizing csharp.\n\nUse responsibly!\n\nCoded by: v1k (Radostin Dimov)")

    def handle_param_change(self, index):
        bbutton1 = QObject.sender(self.powershell_browse_button)
        if bbutton1 is self.powershell_browse_button:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select PowerShell File")
            if file_path:
                self.powershell_file_input.setText(file_path)

        bbutton2 = QObject.sender(self.iconfile_browse_button)
        if bbutton2 is self.iconfile_browse_button:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon File")
            if file_path:
                self.iconfile_input.setText(file_path)

    def compile(self):
        global csharp_template
        powershell_file = self.powershell_file_input.text()
        iconfile = self.iconfile_input.text()
        platform = self.platform_input.currentText()
        version = self.version_input.text()
        description = self.description_input.text()
        pname = self.pname_input.text()
        copyright = self.copright_input.text()
        
        if not powershell_file:
            self.console.append("[*] No PowerShell File Specified!")
            return
        if not os.path.isfile(powershell_file):
            self.console.append("[*] Specified PowerShell File does not exist!")
            return
        if not powershell_file.lower().endswith('.ps1'):
            self.console.append("[*] The specified file is not a PowerShell script!")
            return
        if iconfile:
            if not os.path.isfile(iconfile):
                self.console.append("[*] Specified Icon File does not exist!")
                return
            if not iconfile.lower().endswith('.ico'):
                self.console.append("[*] The specified file is not an icon file!")
                return


        try:
            if version:
                csharp_template = csharp_template.replace('//replacemeaversion', f'[assembly: AssemblyVersion("{version}")]')
                csharp_template = csharp_template.replace('//replacemefversion', f'[assembly: AssemblyFileVersion("{version}")]')
            if description:
                csharp_template = csharp_template.replace('//replacemeatitle', f'[assembly: AssemblyTitle("{description}")]')
                csharp_template = csharp_template.replace('//replacemeadescr', f'[assembly: AssemblyDescription("{description}")]')
            if pname:
                csharp_template = csharp_template.replace('//replacemepname', f'[assembly: AssemblyProduct("{pname}")]')
            if copyright:
                csharp_template = csharp_template.replace('//replacompname', f'[assembly: AssemblyCompany("{copyright}")]')
                csharp_template = csharp_template.replace('//replacemecright', f'[assembly: AssemblyCopyright("{copyright}")]')
            QApplication.processEvents()
            self.console.append("[*] Reading PowerShell file...")
            with open(powershell_file, 'r', encoding='utf-8') as file:
                content = file.read()
            powershell_utf16le_content = content.encode('utf-16le')
            powershellbase64_encoded = base64.b64encode(powershell_utf16le_content)
            stringpsencoded = powershellbase64_encoded.decode('utf-8')
            csharp_template = csharp_template.replace('#replacemepscommand', stringpsencoded)
            self.console.append("[*] Generating stub")
            with open('.program.cs', 'w') as file:
                file.write(csharp_template)
            self.console.append("[*] Compiling stub...Please wait....")
            output_file, _ = QFileDialog.getSaveFileName(self, "Save Output File", "program.exe", "Executable Files (*.exe)")
            if not output_file:
                self.console.append("[-] File saving canceled.")
                subprocess.run(['rm', '.program.cs'], check=True)
                return
            if iconfile:
                subprocess.run(['csc', '/target:winexe', f'/platform:{platform}', '/nologo', f'/out:{output_file}', f'/win32icon:{iconfile}', '.program.cs'], check=True)
            else:
                subprocess.run(['csc', '/target:winexe', f'/platform:{platform}', '/nologo', f'/out:{output_file}', '.program.cs'], check=True)
            self.console.append("[*] Cleaning Up...")
            subprocess.run(['rm', '.program.cs'], check=True)
            self.console.append(f"[*] Done! File saved successfully to {output_file}.")
            QMessageBox.about(self, "Success!", "Success! File compiled and saved!")
                
        
        except ValueError as e:
            self.console.append(f"Error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
