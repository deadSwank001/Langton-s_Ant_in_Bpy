import bpy
import bmesh
import random

# Constants for the simulation
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
CELL_SIZE = 0.1

class LangtonsAnt:
    def __init__(self, width, height):
        # Initialize board
        self.width = width
        self.height = height
        self.board = [[True] * width for _ in range(height)]
        self.ant_pos = (width // 2, height // 2)
        self.ant_direction = 3  # 0 = North, 1 = East, 2 = South, 3 = West
       
        # Create the board in Blender
        self.create_board()

        # Create the ant object
        self.create_ant()
   
    def create_board(self):
        ###Create a grid of squares in Blender to represent the board."""
        for x in range(self.width):
            for y in range(self.height):
                bpy.ops.mesh.primitive_plane_add(size=CELL_SIZE, location=(x * CELL_SIZE, y * CELL_SIZE, 0))
                obj = bpy.context.object
                mat = bpy.data.materials.new(name="White")
                mat.diffuse_color = (1, 1, 1, 1)  # White
                obj.data.materials.append(mat)
               
                # Set the initial material to white
                self.board[x][y] = True  # True means white
               
    def create_ant(self):
        ###"""#Create a representation of the ant."""
        bpy.ops.outliner.item_activate(ANT)
        self.ANT = bpy.ops.object.ANT
       

    def move_ant(self):
        #Move the ant according to Langton's Ant rules."""
        x, y = self.ant_pos
        if self.board[x][y]:  # White square
            self.ant_direction = (self.ant_direction + 1) % 4  # Turn clockwise
            self.board[x][y] = False  # Flip square to black
            self.ANT.data.materials[0].diffuse_color = (0, 0, 0, 1)  # Change material to black
        else:  # Black square
            self.ant_direction = (self.ant_direction - 1) % 4  # Turn counter-clockwise
            self.board[x][y] = True  # Flip square to white
            self.ANT.data.materials[0].diffuse_color = (1, 1, 1, 1)  # Change material to white

        # Move the ant in the current direction
        if self.ant_direction == 0:  # North
            self.ant_pos = (x, (y + 1) % self.height)
        elif self.ant_direction == 1:  # East
            self.ant_pos = ((x + 1) % self.width, y)
        elif self.ant_direction == 2:  # South
            self.ant_pos = (x, (y - 1) % self.height)
        elif self.ant_direction == 3:  # West
            self.ant_pos = ((x - 1) % self.width, y)

        # Update ant's position in Blender
        self.ANT.location = (self.ant_pos[0] * CELL_SIZE, self.ant_pos[1] * CELL_SIZE, 0.1)

    def run_simulation(self, steps):
        for _ in range(steps):
            self.move_ant()


    def move_ant(self):
        #Move the ant according to Langton's Ant rules."""
        x, y = self.ant_pos
        if self.board[x][y]:  # White square
            self.ant_direction = (self.ant_direction + 1) % 4  # Turn clockwise
            self.board[x][y] = False  # Flip square to black
            self.ant.data.materials[0].diffuse_color = (0, 0, 0, 1)  # Change material to black
        else:  # Black square
            self.ant_direction = (self.ant_direction - 1) % 4  # Turn counter-clockwise
            self.board[x][y] = True  # Flip square to white
            self.ANT.data.materials[0].diffuse_color = (1, 1, 1, 1)  # Change material to white

        # Move the ant in the current direction
        if self.ant_direction == 0:  # North
            self.ant_pos = (x, (y + 1) % self.height)
        elif self.ant_direction == 1:  # East
            self.ant_pos = ((x + 1) % self.width, y)
        elif self.ant_direction == 2:  # South
            self.ant_pos = (x, (y - 1) % self.height)
        elif self.ant_direction == 3:  # West
            self.ant_pos = ((x - 1) % self.width, y)

        # Update ant's position in Blender
        self.ANT.location = (self.ant_pos[0] * CELL_SIZE, self.ant_pos[1] * CELL_SIZE, 0.1)

    def run_simulation(self, steps):
        for _ in range(steps):
            self.move_ant()

# Clear existing objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
#bpy.ops.object.delete()

# Run the simulation
ant_simulation = LangtonsAnt(BOARD_WIDTH, BOARD_HEIGHT)
ant_simulation.run_simulation(10)  # Run for 10,000 steps (adjust as needed)
