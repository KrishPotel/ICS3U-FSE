from pygame import *
from coinSorting import CoinSorter

screen = display.set_mode((800,600))

CoinSort = CoinSorter(screen)

running = True

isCoinSorting = False
exitButton = Rect(0,500,100,100)
enterButton = Rect(300,200,200,100)

while running:
    for evt in event.get():

        
        if evt.type == QUIT:
            running = False

    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    # ----------------------------------

    # screen.blit(nickel,(0,0))
    if(isCoinSorting == True): #Checks if the coin sorter should be displayed or not

        CoinSort.run(mx,my,mb,evt) #Shows the coinsorter

        if(exitButton.collidepoint(mx,my) and mb[0]): #checks if mouse is over and clicked exit button
            isCoinSorting=False #Tells the coin sorter to not display anymore

        draw.rect(screen,(0,0,0), exitButton) #Draws the exit button
    
    else:
        screen.fill((255,255,255))

        draw.rect(screen,(0,0,0), enterButton)#Draws the enter coinSorting button

        if(enterButton.collidepoint(mx,my) and mb[0]): #checks if mouse is over and clicked enter button
            isCoinSorting=True #Says to display coin sorter
            
    


    
    # ----------------------------------
    display.flip()

quit()