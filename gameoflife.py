# Game Of Life - BBC Software Engineering Test
# Created      - Feb 2019 (Stephen Brown)
# 
# New to Python - so some of this will be a bit rough round the edges!
# Improvements could incorporate Tkinter or other widget based package
#
# Developed using Python3 with Anaconda

import numpy as np
import matplotlib.pyplot as plt
import time

def main():           # This is the main loop
    seeds=seedgrid()  # Call function that allows user to seed the grid
    iterlife(seeds)   # Call function that iterates through the game of life
    return(seeds)

#***********************************************************************************#
#***********************************************************************************#
#***********************************************************************************#

def seedgrid():      # This function allows the user to seed the grid of live cells
    print('Click the cells you want to seed the grid with') # Prompt user to 
    print('Close the window when done seeding!')            # populate the grid
    plt.figure(0)                          # Initialise a figure to plot on
    plt.plot([1,1], alpha=0, linestyle='None') # Begin creating a blank plot
    plt.axis([0,25,25,0])                  # Manually define the axis range to create 25 cells
    plt.grid(which='both')                 # Show the grid lines to divide plot into cells
    plt.xticks(np.arange(0,25,step=1))     
    plt.yticks(np.arange(0,25,step=1))
    plt.show(block=False)                  # Allow code to execute while the plot is showing

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~ Create Class to obtain co-ordinates of mouse input ~~~~~~~~~~~~~~~~~~~#
    class SeedPoints:                       # Based on Event Handling documentation 
          def __init__(self, cell, ax):     # See MatPlotLib.org
             self.cell = cell                       
             self.xs = list(cell.get_xdata())    # Get X position of click
             self.ys = list(cell.get_ydata())    # Get Y position of click
             self.cid = cell.figure.canvas.mpl_connect('button_press_event', self) 
             self.axs = ax                       # Link current axis to this instance

          def __call__(self, event):
             if event.inaxes!=self.cell.axes: return
             self.xs.append(event.xdata)         # Extend array of X points
             self.ys.append(event.ydata)         # Extend array of Y points
             self.cell.set_data(self.xs, self.ys)
             self.axs.scatter(int(self.xs[-1])+0.5, int(self.ys[-1])+0.5, c='lime') # Draw live cells
             plt.draw()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
 
    while plt.fignum_exists(0):        # Enter a loop to allow the user to click which cells are to be
          ax = plt.gca()               # Get reference to current plot axis                   
          cell, = ax.plot([0], [0], linestyle='None')   # empty cell object
          seeding=SeedPoints(cell,ax)                   # Instantiate a new event/click
          plt.show()                                    # Keep plotting until user closes window 

    seeds=[seeding.xs[1:], seeding.ys[1:]] # Return the X and Y co-ordinates of the live cells 
    return(seeds)

#************************************************************************************#
#************************************************************************************#

def iterlife(seeds):      # Iterates the loop that evolves the cell life/death process
    igrid=np.zeros([25,25])             # Defines the grid of cells at t=0
    for x in range(len(seeds[0])):      # Populate the live cells at t=0
        ix=int(seeds[0][x])             
        iy=int(seeds[1][x])
        igrid[iy][ix]=1
    ###################### ENTER MAIN ITERATIVE LOOP #################################
    while igrid.sum() >= 1.0:
       
          # ~~~~~~~~~~~~~~~~~~ Determine if grid needs extended ~~~~~~~~~~~~~~~~~~~~#
          # ~~~~~~~~ This is done if there are live cells close to grid edge ~~~~~~~#
          exta = igrid[0:2,:].sum()               # Check top rows
          extb = igrid[-3:-1,:].sum()             # Check bottom rows
          extc = igrid[:,0:2].sum()               # Check left columns
          extd = igrid[:,-3:-1].sum()             # Check right columns
          extall=np.array([exta,extb,extc,extd])
          if extall.sum() >= 1:
                  print('Extending Array')
                  igrid = xtendgrid(igrid)
          
          #@@@@@@@@@@@@@@@@@@@    Evolve the game of life    @@@@@@@@@@@@@@@@@@@@@@@#

          # The current extension function means that the edge cells are never 
          # populated with live cells - Even if the grid is initially seeded
          # with live cells at the edge, xtendgrid will always expand the grid
          # before iterating through the game of life - Therefore, we do not need
          # to include the edge cells in the upcoming iterative loop

          ndim=np.shape(igrid)          # Obtain current dimensions of the grid
          ndloop=ndim[0]-2              # We don't loop around edge cells
          tempgrid=np.zeros([ndim[0],ndim[0]])
          tempgrid[:]=igrid             # Create unreferenced temporary copy of igrid
          ## Essential to create separate grid - Don't want to update grid while iterating!
           
          for i in range(ndloop):       # Open row loop    
              for j in range(ndloop):   # Open column loop
                  cval=igrid[i+1][j+1]  # Obtain value of current cell
                  nnei=igrid[i][j:j+3].sum() +   \
                       igrid[i+2][j:j+3].sum() + \
                       igrid[i+1][j] + igrid[i+1][j+2] # Obtain number of live neighbours
                  # Deal with the live cells first (Scenarios 1,2 and 3) 
                  if cval == 1:    # Check cell is live
                     if nnei < 2:           # Underpopulation
                        cval=0
                     if nnei > 3:           # Overcrowding
                        cval=0     
                     if nnei==2 or nnei==3: # Survival
                        cval=1
                     
                  elif cval==0: # Deal with the dead cells
                       if nnei==3: # Creation (Scenario 4)
                          cval=1  
                  else:
                       cval=cval

                  tempgrid[i+1,j+1]=cval
                  # Array is based on zeroes - Scenario 5 is default
                  # igrid[i+1][j+1]=cval   # Kill or spare the current cell                  

          igrid=tempgrid
          ###################### Show the game of life ##########################
          plt.figure(0)                              # Initialise figure
          plt.plot([1,1], alpha=0, linestyle='None') # Create blank plot
          plt.axis([0,ndim[0],ndim[0],0])            # Define correct axis
          plt.grid(which='both')                     # Show grid lines
          plt.xticks(np.arange(0,ndim[0],step=1))    
          plt.yticks(np.arange(0,ndim[0],step=1))
                
          for i in range(ndloop):          # Open loop to plot live cells
              for j in range(ndloop):
                    if igrid[i+1][j+1]==1:
                       ax=plt.gca()               
                       ax.scatter(int(j+1)+0.5, int(i+1)+0.5, c='lime')  
          plt.show(block=False)    
          plt.pause(0.75)                  # Briefly pause execution to allow ctrl+c
          plt.close(0)                     # Close plot window
        
    return(0)

#************************************************************************************#
#************************************************************************************#

def xtendgrid(igrid):     # In case of live cells reaching edge of grid, extend the grid
    dim=np.shape(igrid)   # Obtain dimensions of grid as it currently is
    ngrid=np.zeros([dim[0]+4,dim[0]+4])   # Create new extended grid of zeros
    ngrid[2:-2,2:-2]=igrid                # Place live grid in new grid
    igrid=ngrid                           # Set igrid to the new grid
    return(igrid)                         # Return igrid

#***********************************************************************************#
#***********************************************************************************#
#~~~~~~~~~~~~~~ State what to do when called from command line ~~~~~~~~~~~~~~~~~~~~~#
if __name__=="__main__":   # If running from command line, then execute
   main()                  # the main() function
#***********************************************************************************#

