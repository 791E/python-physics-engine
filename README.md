# A simple physics/simulation engine written in python with pygame
This is a simple physics engine to simulate interactions between bodies, mainly based on newtonian physics. It's core is the python module `pysics`, which is a combination of the words 'python' and 'physics'.
# Features
- [Spacial hash map](pysics/hash_map.py): Divide space into cells for efficient collision detection
- [Dynamic coordinate system](pysics/coordinate_system.py): A dynamic coordinate system which allows for proper resizing of the `pygame` window, with the simulation adapting to the display size.
- [Fully elastic ball-to-ball collision](pysics/temp_ball_collision.py): Accurately calculate fully elastic collisions between multiple balls.
# Usage
View [demo.py](demo.py) for instructions on how to create your `pysics` simulation, or check out [billiard.py](billiard.py) for an example.
# Future plans
The ultimate goal of this physics/simulation engine is, to accurately calculate interactions (mainly collisions) between not only balls, but also any kind of convex polygon. This is not implemented just yet, as the collision response is rather complicated (especially when accounting for rotation), but you will find some artifacts showing the start of the work for this goal. There is the `Polygon` class in the [body.py](pysics/body.py) file, as well as the general collision methods in [collision.py](pysics/collision.py). Especially the latter is not working well, as, until now, I didn't have the time to properly look into the algorithms that are involved in this.

However, I did find some sources that look to be very helpful:
- [dyn4j SAT (Separating Axis Theorem)](https://dyn4j.org/2010/01/sat/)
- [myPhysicsLab.com Rigid Body Collision](https://www.myphysicslab.com/engine2D/collision-en.html)
# Credits
Coordinate system class by [@DanceMonkey276](https://github.com/DanceMonkey276/) on Github
