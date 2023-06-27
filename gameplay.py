"""
https://www.facebook.com/ngtrduc19

"""
import pygame, sys, time
from definitions import *

pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

# KÍCH THƯỚC MÀN HÌNH
size = width, height = 1080, 1920
screen = pygame.display.set_mode(size)

# MÀU
white = (255, 255, 255)
blue = (47, 60, 126)
red = (216, 36, 41)
gray = (50, 50, 50)
light_gray = (100, 100, 100)

# CHỮ
fontTitle = pygame.font.Font("font/title.ttf", 200)
fontGame = pygame.font.Font("font/game.ttf", 180)
mediumfontGame = pygame.font.Font("font/game.ttf", 120)
fontButton = pygame.font.Font("font/game.ttf", 100)

# ÂM THANH
sound_files = [
	"button.mp3",
	"move.mp3",
	"xwin.mp3",
	"owin.mp3",
	"tie.mp3"	]
sounds = [pygame.mixer.Sound(f"sound/{file}") for file in sound_files]
button_sfx, move_sfx, xwin_sfx, owin_sfx, tie_sfx = sounds

# CÁC BIẾN CỐ ĐỊNH
board = create_board()
players = X
play_sound = info = True
onclick = False

while True:
	for  event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	screen.fill(white)
	
	if info:

		# THÔNG TIN TRÊN MÀN CHÍNH
		title = fontTitle.render("Caro", True, gray)
		titleRect = title.get_rect(center=(width / 2, 400))
		screen.blit(title, titleRect)
		
		playerButton = pygame.Rect((width / 6), (height / 2), width / 1.5, 150)
		player = fontButton.render("2 Player", True, white)
		playerRect = player.get_rect(center = playerButton.center)
		pygame.draw.rect(screen, red, playerButton)
		screen.blit(player, playerRect)

		click,_,_ = pygame.mouse.get_pressed()
		mouse = pygame.mouse.get_pos()
		if click == 1:
			onclick = True
		elif click == 0 and onclick:
			if playerButton.collidepoint(mouse):
				onclick = False
				button_sfx.play()
				time.sleep(0.2)
				info = False
	else:
	
		# KẺ Ô BẢNG
		tile_size = 240
		tile_position = (width / 2 - (1.5 * tile_size),
		height / 2 - (1.5 * tile_size))
		tiles = []
		for i in range(3):
			row = []
			for j in range(3):
				rect = pygame.Rect(
						tile_position[0] + j * tile_size,
	                    tile_position[1] + i * tile_size,
	                    tile_size, tile_size)
				pygame.draw.rect(screen, white, rect, 0)
				
				if board[i][j] != None:
					moveColor = red if board[i][j] == X else blue
					move = fontGame.render(board[i][j], True, moveColor)
					moveRect = move.get_rect(center = rect.center)
					screen.blit(move, moveRect)
				row.append(rect)
			tiles.append(row)

		# KẺ LINE BẢNG
		for i in range(1, 3):
			pygame.draw.line(screen, gray,
			(tile_position[0] + i * tile_size, tile_position[1]), 
			(tile_position[0] + i * tile_size, tile_position[1] + 3 * tile_size), 
			12)
			pygame.draw.line(screen, gray,
			(tile_position[0], tile_position[1] + i * tile_size), 
			(tile_position[0] + 3 * tile_size, tile_position[1] + i * tile_size), 
			12)

		# SỰ KIỆN TRONG GAME
		game_over = terminal(board)
		msgColor = red if players == X else blue
		if game_over:
			winner = winners(board)
			if winner is None:
				msg = "TIE GAME"
				msgColor = gray
				if play_sound:
					tie_sfx.play()
				play_sound = False
			else:
				msg = f"PLAYER {winner} WIN"
				if play_sound:
					xwin_sfx.play() if winner == X else owin_sfx.play()
				play_sound = False
				msgColor = red if winner == X else blue
		elif players == X:
			msg = "Player as X"
		else:
			msg = "Player as O"
		message = mediumfontGame.render(msg, True, msgColor)
		messageRect = message.get_rect(center = ((width / 2), 150))
		screen.blit(message, messageRect)
	
		click,_,_= pygame.mouse.get_pressed()
		mouse = pygame.mouse.get_pos()
		if click == 1 and not game_over:
			onclick = True
		elif click == 0 and onclick and not game_over:
			onclick = False
			for i in range(3):
				for j in range(3):
					if board[i][j] is None and tiles[i][j].collidepoint(mouse):
						onclick = False
						board = result(board, (i, j))
						move_sfx.play()
						players = O if players == X else X

		# TẠO NÚT RESTART KHI KẾT THÚC
		if game_over:
			rstButton = pygame.Rect(width / 6, height - 255, width / 1.5, 150)
			rst = fontButton.render("Restart", True, white)
			rstRect = rst.get_rect(center = rstButton.center)
			pygame.draw.rect(screen, gray, rstButton)
			screen.blit(rst, rstRect)
			click,_,_ = pygame.mouse.get_pressed()
			mouse = pygame.mouse.get_pos()
			if click == 1:
				onclick = True
			elif click == 0 and onclick:
				onclick = False
				if rstButton.collidepoint(mouse):
					onclick = False
					button_sfx.play()
					time.sleep(0.2)
					players = X
					board = create_board()
					play_sound = True
			
	pygame.display.flip()