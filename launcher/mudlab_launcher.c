/*
 * MudLab launcher — thin wrapper around python.exe -m mudlab
 * Compile (MinGW64 from repo root):
 *   bash launcher/build.sh
 *
 * mudlab-cmd.exe: console build (-mconsole), spawns python.exe,
 *                 inherits the terminal — output goes to the same console.
 * mudlab.exe:     GUI build (-mwindows -DGUI_MODE), spawns pythonw.exe
 *                 with CREATE_NO_WINDOW — no console window at all.
 */

#include <windows.h>
#include <wchar.h>

int main(void)
{
    /* Directory containing this exe (i.e. data\bin\) */
    wchar_t exe_dir[MAX_PATH];
    GetModuleFileNameW(NULL, exe_dir, MAX_PATH);
    wchar_t *slash = wcsrchr(exe_dir, L'\\');
    if (slash) *slash = L'\0';

    wchar_t python[MAX_PATH];
    _snwprintf(python, MAX_PATH, L"%s\\python.exe", exe_dir);
#ifdef GUI_MODE
    /* GUI launcher: suppress the console window */
    DWORD create_flags = CREATE_NO_WINDOW;
    BOOL inherit_handles = FALSE;
#else
    /* Console launcher: inherit terminal handles */
    DWORD create_flags = 0;
    BOOL inherit_handles = TRUE;
#endif

    /* Collect any extra args the user passed (everything after argv[0]) */
    const wchar_t *cmdline = GetCommandLineW();
    /* Skip past our own argv[0] (may be quoted) */
    const wchar_t *extra = cmdline;
    if (*extra == L'"') {
        extra++;
        while (*extra && *extra != L'"') extra++;
        if (*extra == L'"') extra++;
    } else {
        while (*extra && *extra != L' ') extra++;
    }
    /* extra now points to " <user args>" or "" */

    /* Build: "python[w].exe" -m mudlab [extra args] */
    wchar_t cmd[32768];
    _snwprintf(cmd, 32768, L"\"%s\" -m mudlab%s", python, extra);

    STARTUPINFOW si;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    PROCESS_INFORMATION pi;
    ZeroMemory(&pi, sizeof(pi));

    if (!CreateProcessW(python, cmd,
                        NULL, NULL,
                        inherit_handles,
                        create_flags,
                        NULL, NULL,
                        &si, &pi)) {
        MessageBoxW(NULL, L"Failed to launch python.exe.\nCheck that data\\bin\\python.exe exists.",
                    L"MudLab", MB_ICONERROR | MB_OK);
        return 1;
    }

    WaitForSingleObject(pi.hProcess, INFINITE);
    DWORD exit_code = 0;
    GetExitCodeProcess(pi.hProcess, &exit_code);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return (int)exit_code;
}
