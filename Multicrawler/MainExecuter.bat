@echo off
title Movie crawler version IR2019
echo Press a Key to run the crawler script!
set /p npages="Enter how many pages per crawler should be scraped: "
set /p ncrawlers="Enter how many crawlers per domain have to be initialised: "

pause
echo Every crawler now crawls up to %npages% pages
echo Every domain contains %ncrawlers% Crawlers

echo %~dp0

echo Initate crawlers
TIMEOUT /T 3

start C:\Users\chris\AppData\Local\Programs\Python\Python37-32\python.exe %~dp0\allmovie.py %npages% %ncrawlers% 
start C:\Users\chris\AppData\Local\Programs\Python\Python37-32\python.exe %~dp0\RottenTomatoes.py %npages% %ncrawlers%
start C:\Users\chris\AppData\Local\Programs\Python\Python37-32\python.exe %~dp0\imdb.py %npages% %ncrawlers%
start C:\Users\chris\AppData\Local\Programs\Python\Python37-32\python.exe %~dp0\Flixable.py %npages% %ncrawlers%

echo Crawlers are now crawling
pause
