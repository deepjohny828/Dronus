https://translated.turbopages.org/proxy_u/en-ru.ru.be9ac1b7-67c0aec2-c1c209e6-74722d776562/https/github.com/CopterExpress/clover/blob/master/docs/en/auto_setup.md
https://github.com/CopterExpress/clover/blob/master/docs/ru/setup.md
1) Качаем 23 архив и прошивку(2 ссылка на гит)
2) ![изображение](https://github.com/user-attachments/assets/1947d098-065a-4df5-af5c-b6a7936527f0)
   С этого момента все по гайду (Кроме камеры)
3) rosrun aruco_pose genmap.py 0.33 4 6 1 1 0 > ~/catkin_ws/src/clover/aruco_pose/map/map.txt --top-left
В кловер лаунч или аруко есть настройка аруко - дефолт 0.22 **надо 0.33**
4) Полетник по второй ссылке сверху делаем (Карту сначала форматируем в фат32)
   
