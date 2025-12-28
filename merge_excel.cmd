@echo off
call %USERPROFILE%\anaconda3\Scripts\activate.bat  %USERPROFILE%\anaconda3
call conda activate playground

python merge_excel.py ./AU0 K线导出_AU0_5分钟线数据.xslx

python merge_excel.py ./MGC00Y K线导出_MGC00Y_5分钟线数据.xslx

python merge_excel.py ./AG0 K线导出_AG0_5分钟线数据.xslx

python merge_excel.py ./SI00Y K线导出_SI00Y_5分钟线数据.xslx

python merge_excel.py ./USDCNH K线导出_USDCNH_5分钟线数据.xslx

python merge_excel.py ./基准/USDCNY USDCNY-1H.csv

python merge_excel.py ./基准/MGC MGC-1H.csv

python merge_excel.py ./基准/518850 K线导出_518850_60分钟线数据.xslx

call conda deactivate

pause