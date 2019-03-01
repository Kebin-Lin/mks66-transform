from display import *
from matrix import *
from draw import *
from copy import deepcopy

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         translate: create a translation matrix,
                    then multiply the transform matrix by the translation matrix -
                    takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing

See the file script for an example of the file format
"""

def parse_file( fname, points, transform, screen, color ):
    infile = file(fname,'r').read().split("\n")
    currCommand = None
    for i in infile:
        if currCommand != None:
            args = i.split()
            if currCommand == "line":
                for i in range(len(args)):
                    args[i] = int(args[i])
                add_edge(points,args[0],args[1],args[2],args[3],args[4],args[5])
            elif currCommand == "scale":
                for i in range(len(args)):
                    args[i] = int(args[i])
                temp = make_scale(args[0],args[1],args[2])
                matrix_mult(temp,transform)
            elif currCommand == "translate" or currCommand == "move":
                for i in range(len(args)):
                    args[i] = int(args[i])
                temp = make_translate(args[0],args[1],args[2])
                matrix_mult(temp,transform)
            elif currCommand == "rotate":
                temp = None
                args[1] = 180 * int(args[1]) / math.pi
                if args[0] == "x":
                    temp = make_rotX(args[1])
                elif args[0] == "y":
                    temp = make_rotY(args[1])
                else:
                    temp = make_rotZ(args[1])
                matrix_mult(temp,transform)
            elif currCommand == "save":
                clear_screen(screen)
                draw_lines(points, screen, color)
                save_extension(screen,args[0])
            currCommand = None
        else:
            if i == "ident":
                ident(transform)
            elif i == "apply":
                matrix_mult(transform,points)
            elif i == "display":
                clear_screen(screen)
                temp = deepcopy(points)
                fixMatrix(temp)
                draw_lines(temp, screen, color)
                display(screen)
            elif i == "quit":
                return
            else:
                currCommand = i

def fixMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(4):
            matrix[i][j] = int(round(matrix[i][j],0))
