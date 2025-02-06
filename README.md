#### Инфа для редактирования README.md - https://github.com/GnuriaN/format-README
## Конфигурационные команды в одной строке (remake by me)
```bash
sed -i 's|arg name="aruco_map" default="false"|arg name="aruco_map" default="true"|g' /home/clover/catkin_ws/src/clover/clover/launch/aruco.launch;sed -i 's|arg name="aruco_vpe" default="false"|arg name="aruco_vpe" default="true"|g' /home/clover/catkin_ws/src/clover/clover/launch/aruco.launch;sed -i 's|arg name="length" default="0.22"|arg name="length" default="0.33"|g' /home/clover/catkin_ws/src/clover/clover/launch/aruco.launch;sed -i 's|arg name="map" default="map.txt"|arg name="map" default="guap.txt"|g' /home/clover/catkin_ws/src/clover/clover/launch/aruco.launch;sed -i 's|arg name="aruco" default="false"|arg name="aruco" default="true"|g' /home/clover/catkin_ws/src/clover/clover/launch/clover.launch;rosrun aruco_pose genmap.py 0.33 4 5 1 1 0 -o guap.txt;find ./ -name 'guap.txt';rosrun clover_simulation aruco_gen --single-model --source-world=/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover.world /home/clover/catkin_ws/src/clover/aruco_pose/map/guap.txt > /home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/guap.world;sed -i 's|clover_aruco.world|guap.world|g' /home/clover/catkin_ws/src/clover/clover_simulation/launch/simulator.launch
```
## Конфигурационные команды (оригинал)

```bash
# вместо ручного редактирования файлов выполнить команды:
sed -i 's|arg name="aruco_map" default="false"|arg name="aruco_map" default="true"|g' /home/clover/catkin_ws/src/clover/clover/launch/aruco.launch
sed -i 's|arg name="aruco_vpe" default="false"|arg name="aruco_vpe" default="true"|g' /home/clover/catkin_ws/src/clover/clover/launch/aruco.launch
sed -i 's|arg name="length" default="0.22"|arg name="length" default="0.33"|g' /home/clover/catkin_ws/src/clover/clover/launch/aruco.launch
sed -i 's|arg name="map" default="map.txt"|arg name="map" default="guap.txt"|g' /home/clover/catkin_ws/src/clover/clover/launch/aruco.launch
sed -i 's|arg name="aruco" default="false"|arg name="aruco" default="true"|g' /home/clover/catkin_ws/src/clover/clover/launch/clover.launch
# для генерации карты использовать:
# для изменения размера карты поменять два числа после 0.33
rosrun aruco_pose genmap.py 0.33 4 5 1 1 0 -o guap.txt
# в результате появится файл:
find ./ -name 'guap.txt'
#./catkin_ws/src/clover/aruco_pose/map/guap.txt
# посмотреть содержимое файла:
cat ./catkin_ws/src/clover/aruco_pose/map/guap.txt
# создаём мир с помощью команды из сгенерированной карты:
rosrun clover_simulation aruco_gen --single-model --source-world=/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover.world /home/clover/catkin_ws/src/clover/aruco_pose/map/guap.txt > /home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/guap.world
# подключаем мир
sed -i 's|clover_aruco.world|guap.world|g' /home/clover/catkin_ws/src/clover/clover_simulation/launch/simulator.launch
```
Настройка LPE
-----------
При использовании LPE (параметр ```SYS_MC_EST_GROUP``` = ```local_position_estimator```, ```attitude_estimator_q```):

- В параметре ```LPE_FUSION``` включены флажки ```vision position```, ```land detector```. Флажок ```baro``` рекомендуется отключить.<br>
- Вес угла по рысканью по зрению: ```ATT_W_EXT_HDG``` = 0.5<br>
- Включена ориентация по Yaw по зрению: ```ATT_EXT_HDG_M``` = 1 Vision.<br>
- Шумы позиции по зрению: ```LPE_VIS_XY``` = 0.1 m, ```LPE_VIS_Z``` = 0.1 m.<br>
- ```LPE_VIS_DELAY``` = 0 sec.
