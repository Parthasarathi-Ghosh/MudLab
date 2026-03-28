/*
 * MudLab launcher — Python 3.12+ (PyConfig API)
 * Compile (MinGW64 from repo root):
 *   bash launcher/build.sh
 */

#include <Python.h>
#include <windows.h>
#include <stdlib.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                   LPSTR lpCmdLine, int nCmdShow)
{
    (void)hInstance; (void)hPrevInstance; (void)lpCmdLine; (void)nCmdShow;

    PyStatus status;

    /* Enable UTF-8 mode (PEP 540) before streams are created.
       utf8_mode lives in PyPreConfig, not PyConfig. */
    PyPreConfig preconfig;
    PyPreConfig_InitPythonConfig(&preconfig);
    preconfig.utf8_mode = 1;
    status = Py_PreInitialize(&preconfig);
    if (PyStatus_Exception(status)) {
        Py_ExitStatusException(status);
    }

    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    config.write_bytecode      = 0;
    config.use_environment     = 0;
    config.user_site_directory = 0;

    /* Pass command-line args */
    int argc;
    LPWSTR *argv_w = CommandLineToArgvW(GetCommandLineW(), &argc);
    status = PyConfig_SetArgv(&config, argc, argv_w);
    LocalFree(argv_w);
    if (PyStatus_Exception(status)) {
        Py_ExitStatusException(status);
    }

    status = Py_InitializeFromConfig(&config);
    PyConfig_Clear(&config);
    if (PyStatus_Exception(status)) {
        Py_ExitStatusException(status);
    }

    int ret = PyRun_SimpleString(
        "import sys; from mudlab.core import run_main; sys.exit(run_main())"
    );

    Py_Finalize();
    return ret;
}

int main(int argc, char *argv[])
{
    (void)argc; (void)argv;
    return WinMain(GetModuleHandle(NULL), NULL, GetCommandLineA(), SW_SHOW);
}
