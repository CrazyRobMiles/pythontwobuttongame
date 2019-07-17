# Two Button Game

This started as a Raspberry Pi jam challenge to make a game that you control with two buttons.

It ended up as an attempt to use a Raspberry Pi Zero as an embedded device, and furthermore how to run Python on an ESP device.

The two source files for the different platforms are in the two folders.

They are similar, but different. 

The game itself is very simple:

1. When the game starts the lights will flash white. When the white flashing finishes, you need to start pressing buttons.
2. The game box has coloured lights all round it. If you see more red lights that blue ones, press the red button. If you see more blue lights than red ones, press the blue button. If you get it right you get a flash of green lights and then you get to go again.
3. If you get it wrong you get a red flash (boo) and then the game shows you your score by flashing all the leds. The number of yellow flashes gives you the tens, the number of magenta flashes gives you the units. Then the game starts again. 
4. If you don't press a button in time the game ends. If you leave the game alone all the lights turn off, but they flash cyan every now and then to remind you that you've left it switched on.

And that's it. Take a look at the code if you want to know how it works. If you have any better ideas for a game involving a box with lights and two buttons on it, let me know. 