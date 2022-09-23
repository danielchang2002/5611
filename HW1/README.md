# 5611 HW1: Foundations of Animation & Planning

Daniel Chang
(Worked w/ Hank Berger)

Click [here](https://github.com/danielchang2002/5611/tree/main/HW1) for the code!

## Mouse Follow

![Video](https://raw.githubusercontent.com/danielchang2002/5611/main/HW1/assets/mousefollow.gif)

### Challenge
I downloaded an image of spongybobby (shown in gif). 
I used the image library function to render spongybobby.
I oriented spongybobby towards the mouse by computing the angle of the velocity vector using the atan function, translating the origin to the position of the mouse, and rotating the image by the computed angle.

## Particle System
![Video](https://raw.githubusercontent.com/danielchang2002/5611/main/HW1/assets/particle.gif)

### Challenge
I made the blue balls color a function of time by creating a time vector, incremented after each time step, and setting the red and blue values of the fill to be a linear function of the number of time steps. This can be seen in the beginning of the video.

Additionally, the particles were colored as a function of the bounce. I had a vector of bounce values (the previous velocity imparted onto the blue balls via the red) and used these values to set the green fill (shown near end of video).

```bash
    int green = (int) (bounce[i] == null ? 0 : bounce[i].length());

    fill(255 - time[i], green, time[i]); 
    circle(pos[i].x, pos[i].y, r*2); //(x, y, diameter)
```

## TTC Forces

![Video](https://raw.githubusercontent.com/danielchang2002/5611/main/HW1/assets/ttc.gif)

## Tree Search Exercise

![Image](https://raw.githubusercontent.com/danielchang2002/5611/main/HW1/assets/ttc.gif)

## PRM Exericse

![Video](https://raw.githubusercontent.com/danielchang2002/5611/main/HW1/assets/PRM.gif)