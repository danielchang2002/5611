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
```java
  PImage img = loadImage("spongebob.png");
  imageMode(CENTER);

  // rotate image so its oriented towards the mouse
  // looked at this: https://forum.processing.org/one/topic/rotate-image.html
  translate(pos.x, pos.y);

  float angle = atan(vel.y / vel.x);

  if (Float.isNaN(angle)) {
    angle = last_angle;
  }
  rotate(angle);

  // draw image
  image(img, 0, 0);
```


## Particle System
![Video](https://raw.githubusercontent.com/danielchang2002/5611/main/HW1/assets/particle.gif)

### Challenge
I made the blue balls color a function of time by creating a time vector, incremented after each time step, and setting the red and blue values of the fill to be a linear function of the number of time steps. This can be seen in the beginning of the video.

Additionally, the particles were colored as a function of the bounce. I had a vector of bounce values (the previous velocity imparted onto the blue balls via the red) and used these values to set the green fill (shown near end of video).

```java
    int green = (int) (bounce[i] == null ? 0 : bounce[i].length());

    fill(255 - time[i], green, time[i]); 
    circle(pos[i].x, pos[i].y, r*2); //(x, y, diameter)
```

## TTC Forces

![Video](https://raw.githubusercontent.com/danielchang2002/5611/main/HW1/assets/ttc.gif)

## Tree Search Exercise

Terminal output:
```bash
List of Neighbors:
[1, 3] [2, 4] [7, 1] [4, 6] [5] [7] [5] []

Beginning Search
Adding node 0 (start) to the fringe.
 Current Fring:  [0]
Added node 1 to the fringe.
 Current Fringe:  [1]
Added node 3 to the fringe.
 Current Fringe:  [1, 3]
Added node 4 to the fringe.
 Current Fringe:  [1, 4]
Added node 6 to the fringe.
 Current Fringe:  [1, 4, 6]
Added node 5 to the fringe.
 Current Fringe:  [1, 4, 5]
Added node 7 to the fringe.
 Current Fringe:  [1, 4, 7]
Goal found!

Reverse path: 7  5  6  3  0  
```

Answers to questions:
  1. Try to understand how this Breadth-first Search (BFS) implementation works.
      As a start, compare to the pseudocode at: https://en.wikipedia.org/wiki/Breadth-first_search
      How do I represent nodes? How do I represent edges?
      
      Nodes are just integers, Edges are just ArrayLists of integers (which are nodes)
      
      What is the purpose of the visited list? What about the parent list?
      
      Visited: to be robust w/ cycles (don't get stuck in inf loop)
      Parent: to reconstruct path
      
      What is getting added to the fringe? In what order?

      The (unvisted) neighbors of the earliest added node on the fringe.
      
      How do I find the path once I've found the goal?

      Traverse the parent list (recursively find the parent).
      
  2. Convert this Breadth-first Search to a Depth-First Search.
      Which version BFS or DFS has a smaller maximum fring size?

      DFS has a smaller max fringe size (3).
      
  3. Currently, the code sets up a graph which follows this tree-like structure: https://snipboard.io/6BhxRd.jpg
      Change it to plan a path from node 0 to node 7 over this graph instead: https://snipboard.io/VIx6Er.jpg
      How do we know the graph is no longer a tree?

      There's a node w/ two parents (in degree > 1)
      
      Does Breadth-first Search still find the optimal path?

      Yes
      
CHALLENGE:
  1. Make a new graph where there is a cycle. DFS should fail. Does it? Why?

  It doesn't fail, we have a visited list, handles cycles.
  
  2. Add a maximum depth limit to DFS. Now can it handle cycles?

  It can still handle cycles, it was never failing before.
  
  3. Call the new depth-limited DFS in a loop, growing the depth limit with each
      iteration. Is this new iterative deepening DFS optimal? Can it handle loops
      in the graph? How does the memory usage/fringe size compare to BFS?

      Yes, this method visits the nodes in the same order as BFS, so it is guaranteed to be optimal. It can handle loops. It trades time w/ space: Since DFS's fringe is at most the depth of the tree, its memory usage is a lot smaller.

## PRM Exericse

![Video](https://raw.githubusercontent.com/danielchang2002/5611/main/HW1/assets/PRM.gif)