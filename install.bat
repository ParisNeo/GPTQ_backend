@echo off

setlocal

REM Get the absolute path to the GPT4All-ui root directory
for /f "delims=" %%i in ('cd') do set "gpt4all_ui_root=%%~fi"
set "gptq_backend_path=%~dp0"
echo "runnin on %gpt4all_ui_root%"
REM Activate the GPT4All-ui virtual environment
echo activating environment "%gpt4all_ui_root%\env\Scripts\activate"
call "%gpt4all_ui_root%\env\Scripts\activate"

REM Install the required packages
pip install -r "%gptq_backend_path%\requirements.txt"

REM Copy the gptq subfolder to the backends directory
xcopy /E /Y "%gptq_backend_path%\gptq" "%gpt4all_ui_root%\backends\gptq\"

echo.
echo GPTQ_backend has been installed successfully!
echo.

REM Deactivate the virtual environment
deactivate

endlocal
