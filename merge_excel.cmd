@echo off
call %USERPROFILE%\anaconda3\Scripts\activate.bat  %USERPROFILE%\anaconda3
call conda activate playground

python merge_excel.py data/choice/AU0 K线导出_AU0_5分钟线数据.xlsx

python merge_excel.py data/choice/MGC00Y K线导出_MGC00Y_5分钟线数据.xlsx

python merge_excel.py data/choice/AG0 K线导出_AG0_5分钟线数据.xlsx

python merge_excel.py data/choice/SI00Y K线导出_SI00Y_5分钟线数据.xlsx

python merge_excel.py data/choice/USDCNH K线导出_USDCNH_5分钟线数据.xlsx

python merge_excel.py data/choice/基准/518850 K线导出_518850_60分钟线数据.xlsx

call conda deactivate

pause