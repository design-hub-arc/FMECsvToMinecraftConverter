@echo off
REM this line is a comment, or REMark

REM %1 means the first parameter
IF [%1] == [] GOTO help
IF [%2] == [] GOTO help
GOTO convert

:help
echo Usage: convert.bat inputCsvFile resultWorldName
GOTO end

:convert
REM %~f1 means full path name
echo Converting %~f1



"C:\Program Files\FME\fme.exe" ".\Converter.fmw" --DestDataset_MINECRAFT "%HOMEDRIVE%%HOMEPATH%\AppData\Roaming\.minecraft\saves" --worldName "%~2" --pointReduction "100" --SourceDataset_CSV2 "%~f1" --FEATURE_TYPES "" --shouldColor "no"

:end
