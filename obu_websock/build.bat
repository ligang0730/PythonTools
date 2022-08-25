@echo off
for %%i in (protobuf/*.proto) do (
    protoc --python_out=pbpy protobuf/%%i
    echo exchange %%i To python file successfully!  
)
pause