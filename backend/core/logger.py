# backend/core/logger.py
"""
This file allows for coloured logs in terminal.
"""
from colorama import Fore, Style, init
init(autoreset=True)

def log_info(msg):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")

def log_warn(msg):
    print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {msg}")

def log_error(msg):
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")

def log_security(msg):
    print(f"{Fore.MAGENTA}[SECURITY]{Style.RESET_ALL} {msg}")

def log_module(msg):
    print(f"{Fore.GREEN}[MODULE]{Style.RESET_ALL} {msg}")
