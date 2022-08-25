@echo off
for %%i in (./*.proto) do (
    protoc --python_out=../pbpy ./%%i
    echo exchange %%i To python file successfully!  
)
pause