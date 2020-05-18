# Maze Generator Vizualiser 

This is a tool for vizualising how different maze generation algorithms work build in Pygame. It was inspired by [this blog post](https://bost.ocks.org/mike/algorithms/) by Mike Bostock and Jamis Buck's [curation of maze algorithms](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap).

### Recursive Backtracker

This algorithm works as follows:

1. Pick a start cell
2. Randomly choose a direction (N, S, E, W)
3. Iterate over these directions, checking if the adjacent cell in this direction has been visited before.
4. If a direction hasn't been visited before, carve a path into the adjacent cell; if it has been visited, try the next direction.
5. Once all directions have been tried, return.

To visualise it, I have implemented it iteratively. 
* Blue = start cell.
* Green = current cell on which the recursive call is being made.
* Grey = cells with unfinished calls on the stack. 
* White = cells corresponding to calls that have returned.

### Eller's Algorithm

Eller's Algorithm is interesting because it produces a maze row by row. This makes it very memory efficient because it only needs to store information about a single row. 
It uses sets to group together cells which have a connection between them.

1. First, create the initial row and assign each cell a unique set.
2. Randomly merge together adjacent cells. Every cell that has been merged now belongs to the set of its neighbour because there is a connection between them, and the cell's original set becomes exinct.
3. Create the next row: each set in the previous row must have at least one cell in the new row. This is essentially a vertical connection in the maze that prevents isolates from forming. After these vertical connections have been assigned, fill in the rest of the row with new random unique sets.
4. Repeat the merging and creation process until the last row has been created.
5. Finish by merging all remaining sets together.

My implementation uses colours to represent the sets.

### Kruskal's Algorithm 

A randomised adaptation of Kruskal's algorithm (originially used to produce minimal spanning trees from a weighted graph) can be used to generate mazes.

1. Assign each cell in the grid a unique set. This is how we will keep track of whether the cells are connected or not.
2. Add each internal boundary in the grid to a list - i.e. every line separating one cell from its neighbour. Shuffle the list.
3. For each line in the list, decide whether the cells that it divides are in the same set. If they are, simply discard the line - these cells are already connected. Else, remove this boundary from the grid and merge the sets of the cells.
4. Repeat until there are no more edges.

My implementation again uses colours to represent the sets.


