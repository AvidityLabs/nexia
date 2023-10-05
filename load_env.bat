@echo off
for /f "usebackq tokens=1,* delims==" %%i in (.env) do (
    setx "%%i" "%%j" /m
)
