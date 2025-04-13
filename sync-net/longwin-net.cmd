@echo off
call %USERPROFILE%\anaconda3\Scripts\activate.bat  %USERPROFILE%\anaconda3
call conda activate playground

python longwin-net.py

call conda deactivate