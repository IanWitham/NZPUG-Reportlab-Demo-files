"""Run all Python scripts...

This script will run all of the other python scripts located in the same
folder as itself. Use this to generated all of the example PDF files in order.
"""
import os
import subprocess

for filename in sorted([f for f in os.listdir(".")
                        if f.endswith(".py")
                        and f != "run_all.py"]): 
    subprocess.Popen("python " + filename, shell=True)
