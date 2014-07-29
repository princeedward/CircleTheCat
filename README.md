CircleTheCat
============

##Introduction

This is a MiniMax algorithm implementation for the circle the cat game, which is originally deisgned by a Japanese designer. A link to the game can be found [here](http://www.gamedesign.jp/flash/chatnoir/chatnoir.html).

A snapshoot of the original game and my python gui are showed below.

![circle the cat flash game snapshoot](https://github.com/princeedward/CircleTheCat/blob/master/resource/GameSnap.PNG)

**circle the cat flash game snapshoot**

![python solver gui snapshoot](https://github.com/princeedward/CircleTheCat/blob/master/resource/GuiSnap.PNG)

**python solver gui snapshoot**

##How to Use

1. Left click on the yellow dot to mark the blocks, which will turn the dot to black. (At begining, you should mark all the blocks initially on the map first)
2. Right click on the yellow dot to specify the position of the cat, it will turn the dot to red and begin caculating the recommandation step for users.
3. The recommandation step will beshowed in dark green. But to make it a real block, you have to click on it before specifying the next position of the cat.
4. To clear the current map and start over you can click the mouse middle button.

**Notice**: To change the search step, simply set MINI_MAX_depth on line 17 to whatever you want. The bigger the number is, the slower the program will run, but the more better the recommandation will be.

##Future improvement

Code has been tested on a windows machine with 18% cpu cosumption and 8MB memmory cosumption, however it takes very long time to run if setting the depth equal to 6. To improve the speed, the nature of minimax algorithm will enable us to use parallel computing. This could be implemented in the future.
