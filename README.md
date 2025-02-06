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
