# A 4X4 PUZZLE GAME USING PYGSME IN PYTHON

#### Description:

This is a 4X4 Puzzle game built in Python using the pygame library. The board is a 4x4 grid with fifteen tiles (numbered 1 through 15 going left to right) and a single blank space. The tiles start out in random positions, and the player must slide tiles around until
the tiles are back in their original order. Players can reset the game i theywant to start over or better still they can just start a new game

This project was inspired by one of my favorite mobile games "Johnny Bravo Big Babe adventure"
The pygame library does most of the work due to its massive array of functional functions (no pun intended).
I created the necessary columns, rows and boxes using the rect object and designed it using my favorite colours (cyan and pink).
Then I created the game mechanics making sure the boxes moved as expected (eliminating bugs along the way), I updated the variables of the game state and displayed the new state on the screen. If "move" has been set (either by the keyboard event handling code) then we can call the animate() to perform the sliding animation. The parameters are the board data structure, the direction of the slide, a message to display while sliding the box, and the speed of the sliding.
After it returns, we need to update the actual board data structure (which is done by the makeMove() function) and then add the box to the allMoves list of all the slides made so
far. This is done so that if the player clicks on the "Reset" button, we know how to undo all the player’s slides.
I set a basic reset format so that the machine can return the boxes to their original scrambled format. This is useful if the user wants to start anew but without having to start a new game. If the user successfully arranges the boxes, they receive a congratulatory message commending them for a job well done.
Then I created the necessary key movement buttons (using the event.key) and the necessary destruction functions needed to end the game (pygame.quit() and sys.quit()). Pygame internally has its own list data structure that it creates and appends Event objects to as they are made. This data structure is called the event queue. When the pygame.event.get() function is called with no parameters, the entire list is returned. However, you can pass a constant like QUIT to pygame.event.get() so that it will only return the QUIT events (if any) that are in the internal event queue. The rest of the events will stay in the event queue for the next time pygame.event.get() is called.
All in all, puzzles are a fun way to build one's thinking capacity and I am proud to use this game as my final project in CS50x.
