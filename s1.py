from dokusan import generators
import numpy as np 
import pygame
import random
from pprint import pprint

WIDTH= 700
buffer = 45
mistake = 0

background_color = (250,240,245)
original_element_grid_color = (52,31,151)

example_board = np.array(list(str(generators.random_sudoku(avg_rank = 150))))
arr = example_board.reshape(9,9)
grid = arr.astype('int32')

grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
question =  [[grid_original[x][y] for y in range(len(grid_original[0]))] for x in range(len(grid_original))]

def find_next_empty(puzzle):
	for r in range(9):
	  for c in range(9):
	  	if puzzle[r][c] == 0:
	  		return r, c
	return None, None
	
def is_valid(puzzle, guess, row, col):
        row_vals  = puzzle[row]
        if guess in row_vals:
                return False
        col_vals = [puzzle[i][col]for i in range(9)]
        if guess in col_vals:
                return False
        row_start = (row // 3) * 3
        col_start = (col// 3) * 3
        for r in range(row_start, row_start + 3):
                for c in range(col_start, col_start + 3):
                        if puzzle[r][c] == guess:
                                return False
        return True 
	 
	 
def solve_sudoku(puzzle):
	 row, col = find_next_empty(puzzle) 
	 if row is None:
	 	return True
	 for guess in range(1,10):
	      if is_valid(puzzle,guess,row,col):
	      	puzzle[row][col] = guess
	      	if solve_sudoku(puzzle):
	      		return True
	      puzzle[row][col] = 0
	 return False

def cont_mistake(win):
        myfont = pygame.font.SysFont('Comic Sans Ms',30)
        text = myfont.render("Mistakes:" + str(mistake),True,(0,0,0),(background_color))
        win.blit(text,(90,550))
        pygame.display.update()

def congrats_win():
        pygame.init()
        win4 = pygame.display.set_mode((500,200))
        pygame.display.set_caption('')
        win4.fill(background_color)
        picture = pygame.image.load(r'C:\Users\vinay\Downloads\congrats.JPG')
        win4.blit(picture,(0,0))
        smallfont = pygame.font.SysFont('Comic Sans Ms',35)
        text = smallfont.render('Yahhoo!' , True , (0,0,0))
        win4.blit(text,(300,50))
        pygame.display.update()
        
def display_sol():
    pygame.init()
    pygame.display.set_caption('Solution')
    win1 = pygame.display.set_mode((WIDTH,WIDTH))
    win1.fill(background_color)
    pygame.display.flip()
    myfont = pygame.font.SysFont('Comic Sans Ms',30)
    
    
    for i in range(0,10):
    	if i % 3 == 0:
    		pygame.draw.line(win1,(0,0,0),(50+50*i,50),(50+50*i,500),4)
    		pygame.draw.line(win1,(0,0,0),(50,50+50*i),(500,50+50*i),4)
    	pygame.draw.line(win1,(0,0,0),(50+50*i,50),(50+50*i,500),2)
    	pygame.draw.line(win1,(0,0,0),(50,50+50*i),(500,50+50*i),2)
    pygame.display.update()
    	
    for i in range(0,len(question[0])):
    	for j in range(0,len(question[0])):
    		if 0 < question[i][j] < 10:
    			value = myfont.render(str(question[i][j]),True,original_element_grid_color)
    			win1.blit(value,((j+1)*50+15,(i+1)*50+5))

    
    for i in range(0,len(grid_original[0])):
    	for j in range(0,len(grid_original[0])):
    		if question[i][j] == 0:
    			value = myfont.render(str(grid_original[i][j]),True,(0,0,0))
    			win1.blit(value,((j+1)*50+15,(i+1)*50+5))
    			
    pygame.display.update()
    
def insert(win,position):
        global mistake
        i,j = position[1],position[0]
        myfont = pygame.font.SysFont('Comic Sans Ms',30)
        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                return
                        if event.type == pygame.KEYDOWN:
                                if event.type == pygame.QUIT:
                                        pygame.quit()
                                        return
                                if question[i-1][j-1] != 0:
                                        return
                                if event.key == 48:
                                        if grid[i - 1][j - 1] != grid_original[i - 1][j - 1]and mistake > 0:
                                                mistake -= 1
                                                cont_mistake(win)
                                        grid[i-1][j-1] = event.key - 48
                                        text = myfont.render("   ",True,(0,0,0),(background_color))
                                        pygame.draw.rect(win,background_color,(position[0]*50+2* buffer,position[1]*50+2* buffer,50-buffer,50-buffer))
                                        win.blit(text,(position[0]*50 + 15,position[1]*50+ 5))
                                        pygame.display.update()
                                        return
                                if 0 < event.key - 48 < 10 :
                                        if grid_original[i -1][j - 1] != event.key - 48:
                                                mistake += 1
                                                cont_mistake(win)
                                                value = myfont.render(str(event.key -48),True,(255,0,0))
                                        else:
                                                value = myfont.render(str(event.key -48),True,(0,0,0))
                                        pygame.draw.rect(win,background_color,(position[0]*50 + 2*buffer,position[1]*50+2*buffer,50-buffer,50 -buffer))
                                        win.blit(value,(position[0]*50 + 15,position[1]*50+ 5))
                                        grid[i-1][j-1] = event.key - 48
                                        pygame.display.update()
                                        return
                                return
                        if (grid_original == grid).all() and mistake == 0:
                                congrats_win()
																						
def main():
    pygame.init()
    pygame.display.set_caption('Puzzle')
    win = pygame.display.set_mode((WIDTH,WIDTH))
    win.fill(background_color)
    pygame.display.flip()
    myfont = pygame.font.SysFont('Comic Sans Ms',30)
    smallfont = pygame.font.SysFont('Corbel',25)
    text = smallfont.render('Solution' , True , (240,240,240))
    
    for i in range(0,10):
    	if i % 3 == 0:
    		pygame.draw.line(win,(0,0,0),(50+50*i,50),(50+50*i,500),4)
    		pygame.draw.line(win,(0,0,0),(50,50+50*i),(500,50+50*i),4)
    	pygame.draw.line(win,(0,0,0),(50+50*i,50),(50+50*i,500),2)
    	pygame.draw.line(win,(0,0,0),(50,50+50*i),(500,50+50*i),2)
    pygame.display.update()
    	
    for i in range(0,len(grid[0])):
    	for j in range(0,len(grid[0])):
    		if 0 < grid[i][j] < 10:
    			value = myfont.render(str(grid[i][j]),True,original_element_grid_color)
    			win.blit(value,((j+1)*50+15,(i+1)*50+5))
    pygame.display.update()
    
    while True:
            width = 30
            heigth = 30
            for event in pygame.event.get():
                    position = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            insert(win,(pos[0]//50,pos[1]//50))
                    if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                            position = pygame.mouse.get_pos()
                            if width <= position[0] <= width * 16 + 140 and heigth * 18 <= position[1] <= heigth * 18 + 40:
                                    display_sol()
                                    
            if width * 16 <= position[0] <= width * 16 + 140 and heigth * 18 <= position[1] <= heigth * 18 + 40:
                    pygame.draw.rect(win,(160,160,160),[width * 16,heigth * 18,140,40])
            else:
                    pygame.draw.rect(win,(120,120,120),[width * 16,heigth * 18,140,40])
            win.blit(text,(width * 16 + 28,heigth * 18 + 10))
            pygame.display.update()
            
            if (grid_original == grid).all() and mistake == 0:
                    congrats_win()
            
     	
def game_display():
        pygame.init()
        win3 = pygame.display.set_mode((WIDTH,WIDTH))
        pygame.display.set_caption('Sudoku')
        win3.fill(background_color)
        picture = pygame.image.load(r'C:\Users\vinay\Downloads\image.jpeg')
        win3.blit(picture,(80,80))
        smallfont = pygame.font.SysFont('Corbel',20)
        text = smallfont.render('Let start' , True , (240,240,240)) 
        pygame.display.update()
        width = 30
        heigth = 30
        global grid_original
        solve_sudoku(grid_original)
        while True:
                position = pygame.mouse.get_pos()
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                               pygame.quit()
                               return
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            position = pygame.mouse.get_pos()
                            if width <= position[0] <= width * 10 + 140 and heigth * 14 <= position[1] <= heigth * 14 + 40:
                                    pygame.mouse.set_pos([0,0])
                                    main()
                if width * 10 <= position[0] <= width * 10 + 140 and heigth * 14 <= position[1] <= heigth * 14 + 40:
                        pygame.draw.rect(win3,(0,146,69),[width * 10,heigth * 14,140,40])
                else:
                        pygame.draw.rect(win3,(34,181,115),[width * 10,heigth * 14,140,40])
                win3.blit(text,(width * 10 + 28,heigth * 14 + 10))
                pygame.display.update()
game_display()
                
        
