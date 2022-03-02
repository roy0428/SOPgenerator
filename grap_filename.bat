@echo off

set /P file_name=please enter filename.
set bag=.bag
set avi=.avi

python ./extract_bag.py ./%file_name%%bag%
timeout 5

cd ./%file_name%
dir /b color > filenames.csv
cd ..

python ./c_excel.py ./%file_name%/filenames.csv ./%file_name%/sample.csv
python ./images_to_video.py ./%file_name%/color/ ./%file_name%/%file_name%%avi%
python ./check_elements.py ./%file_name%/filenames.csv ./%file_name%/sample.csv ./%file_name%/elements.csv