@echo off
call %USERPROFILE%\anaconda3\Scripts\activate.bat  %USERPROFILE%\anaconda3
call conda activate playground

python merge_excel.py data/choice/disaggregated K线导出_AU0_5分钟线数据.xlsx

python merge_excel.py data/choice/disaggregated K线导出_AG0_5分钟线数据.xlsx

python merge_excel.py data/choice/disaggregated K线导出_518850_60分钟线数据.xlsx

python merge_excel.py data/choice/disaggregated K线导出_AG0_120分钟线数据.xlsx

python merge_excel.py data/choice/disaggregated K线导出_AU0_120分钟线数据.xlsx

call conda deactivate

pause