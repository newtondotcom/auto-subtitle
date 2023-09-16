@echo off
setlocal enabledelayedexpansion

:: Check if FFmpeg is installed and in the system PATH
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo FFmpeg is not installed or not in the system PATH.
    pause
    exit /b 1
)

:: Set the input video file and output file name pattern
set input_file=%1
set output_pattern=%2

:: Set the segment duration in seconds
set segment_time=%3

:: Create the output directory if it doesn't exist
mkdir output >nul 2>&1

:: Split the video into segments
ffmpeg -i "%input_file%" -c:v copy -c:a copy -f segment -segment_time %segment_time% "output\%output_pattern%_%%03d.mp4"

echo Video splitting completed.
pause
