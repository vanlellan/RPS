# RPS battle system



## Basic Idea
- players play a generalized version of Rock Paper Scissors
- instead of a discrete choice between rock(1,0,0), paper(0,1,0), and scissors(0,0,1), the player chooses any normalized 3-vector: (r,p,s)
- The RPS vectors of the two players are compared, and the winner is determined
- players make their choice of vector by orienting a sphere



## Other Features/Ideas
- [X] The game is live, rather than turn based
	- [ ] each player has a trigger to 'attack', forcing a comparison of RPS vectors
- [X] Continuous scoring
	- [X] points are float-valued, determined by outcome of vector comparison
- [ ] Discrete scoring
	- [ ] points are integer valued, with pre-defined ranges for vector comparison output
	- [ ] e.g. 0 points: 0.0-0.5, 1 point: 0.5-0.9, 2 points, 0.9-1.0
- [ ] AI
	- [ ] It would be quite fun to try to write an optimal AI for this game
	- [ ] use a simple neural net (~few inputs are coordinates of player for past few steps, seven outputs: up,down,left,right,cw,ccw,brake, perhaps just one hidden layer?)
    - [ ] start with a simple random walk
- [ ] Separate attack/defense  **SAFE ZONES MAKE THIS A BAD IDEA**
	- [ ] each player controls two independent spheres: one for attack, one for defense
	- [ ] points can only be scored by attacking
	- [ ] the attacking player's attack vector is compared against the defending player's defense vector
- [ ] **NEW WAY TO DO IT:**
	- [ ] attack and defense are determined by the same sphere, but the central reticule is split (left/right) (or top/bottom)
			into an attack reticule and a defense reticule
	- [ ] the angular separation between the two could be fixed, or variable, determined by the player directly, or determined by character gear/modifiers
	- [ ] you can still sort of park your defense reticule on the safezone, but it is more challenging to do it while moving your attack reticule
- [ ] **SIMPLER NEW WAY:**
    - attack and defense are determined by the same sphere
    - the ship's shield *is* the chromasphere
    - the attack color is whatever is directly in front of the nose of the ship
    - defense color depends on *where* the incoming attack hits the shield
    - the pilot flies the ship and decides when to fire
    - the co-pilot (chroma-engineer?), orients the chromasphere
    - visuals: open-circles represent enemy chroma-position, filled circles represent enemy physical angular position
    - perhaps enemy chroma info is only shown if the enemy is in your reticule, or if you're in theirs
- [X] angular momentum
	- [X] the spheres conserve angular momentum
	- [X] players control sphere orientation through application of torque
	- [X] there should probably be some small friction applied
	- [X] also, perhaps a "brake" key, to significantly increase friction
- [ ] move keybindings to player class?
- [ ] joy con controls:
    - stick for pitch and roll (or yaw)
    - bumpers for yaw (or roll)
    - a to attack
    - b to brake


## Potential Applications-
- [ ] GAME: Co-Pilot-
	- A minimalist space dogfight game (could be limited to 1vAI or 1v1), perhaps set in an asteroid field (something like Frontier)
	- The pilot flies the ship, just as in Frontier
	- The co-pilot controls the ships laser frequency and shield frequency using the RPS sphere system
	- Which player should control the laser aiming/trigger? probably the pilot
	- co-pilot controls only one RPS sphere
	- ship lasers fire only straight forward
	- therefore, pilot must aim lasers
	- On the co-pilot HUD (the RPS sphere):
		- numbered targeting dots for each enemy ship in the forward FOV
		- damage dots for each laser currently impacting the shields
		- pilot and copilot must communicate and coordinate which enemy to target next
	- shield spectrum and laser spectrum are identical
	- therefore, you can sit at the safe points and have impervious shield, but your lasers won't do any damage
	- alternatively: 3 crew:
		- pilot (only pilots the ship)
		- gunner (aims the lasers)
		- tuner (tunes the laser and shield frequencies)

- [ ] SIMPLE VERSION:
	- [ ] remake asteroids (2D), for two players
	- [ ] changes:
		- [ ] add in strafing
		- [ ] change 'bullet' weapon to beam weapon
		- [ ] beam weapon does instant, constant, long-range damage, low DPS (eventually overheats? pulse instead of beam?)
		- [ ] beam color and shield color are determined by RPS sphere
            - a 1-sphere (circle) could be the equator of a RPS 2-sphere, eliminating the safe zones

- [ ] MINIMAL RPS GAME OF LIFE:
	- all live squares have an RGB color
	- each step, all live squares battle all live neighbors. The sum of the outcomes determines if the square lives or dies
	- each step, all dead squares search pairs of live neighbors for those with 'enough overlap' in their RGB values (i.e. dot product)
		- if so, the dead square becomes live next round, somehow taking RGB colors from both parents
	- alternative: Asexual reproduction
		- at each death, the neighbor that dealt the most damage clones itself to replace the dying square
		- cloning is imperfect, mutations can occur
