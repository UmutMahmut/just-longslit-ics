@echo off
setlocal

chcp 65001 > nul
pushd "%~dp0"

set "OUT=repo_tree_brief.txt"
if exist "%OUT%" del "%OUT%"

echo # Repo Tree (Brief) > "%OUT%"
echo Generated: %DATE% %TIME%>> "%OUT%"
echo Root: %CD%>> "%OUT%"
echo.>> "%OUT%"

echo [ROOT FILES]>> "%OUT%"
dir /b /a:-d >> "%OUT%"
echo.>> "%OUT%"

echo [ROOT DIRS]>> "%OUT%"
dir /b /ad >> "%OUT%"
echo.>> "%OUT%"

echo [DIR TREE: DIRS ONLY]>> "%OUT%"
tree /A > temp_tree.txt

findstr /v /i ^
  /c:".git\" ^
  /c:".venv\" ^
  /c:"__pycache__" ^
  /c:".mypy_cache" ^
  /c:".pytest_cache" ^
  /c:".ruff_cache" ^
  /c:"node_modules" ^
  /c:"dist" ^
  /c:"build" ^
  temp_tree.txt >> "%OUT%"

del temp_tree.txt
echo.>> "%OUT%"

echo [KEY PATHS: 1-LEVEL FILE LIST]>> "%OUT%"
call :ListDir "workflows"
call :ListDir ".github\workflows"
call :ListDir "docs"
call :ListDir "just-ls-ics-starter"
call :ListDir "just-ls-ics-starter\src"
call :ListDir "just-ls-ics-starter\src\justls"
call :ListDir "just-ls-ics-starter\tests"
call :ListDir "just-ls-ics-starter\docs"
call :ListDir "just-ls-ics-starter\docs\api"
echo Wrote %OUT%
goto :eof

:ListDir
set "P=%~1"
if exist "%P%" (
  echo -- %P%>> "%OUT%"
  dir /b "%P%" >> "%OUT%"
  echo.>> "%OUT%"
)
exit /b
