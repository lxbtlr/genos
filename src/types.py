from numpy import dtype, array, recarray
#FIXME: import flags from argparse for colormode

# RGBA Color


def color(r,g,b,a):
    Color = dtype({'names': ['r', 'g', 'b','a'],
                   'formats': ['B', 'B','B', 'B',]}) 
    arr = array([r,g,b,a],dtype=dtype)
    return arr.view(recarray)



