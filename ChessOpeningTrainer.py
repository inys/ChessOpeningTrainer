import pygame as pg
#import chessdotcom
import chess

def cr2xy(cr, flipped):
  if flipped:
    return (7-cr[0])*FIELD, (7-cr[1])*FIELD
  else:
    return cr[0]*FIELD, cr[1]*FIELD

def xy2cr(xy, flipped):
  if flipped:
    return 7 - (xy[0] // FIELD), 7 - (xy[1] // FIELD)
  else:
    return xy[0] // FIELD, xy[1] // FIELD

def cr2square(cr):
  return chess.square(file_index=cr[0], rank_index=7-cr[1])

def square2cr(square):
  return chess.square_file(square), 7-chess.square_rank(square)

def cr2uci(cr):
  return chess.FILE_NAMES[cr[0]]+chess.RANK_NAMES[7-cr[1]]

def uci2cr(uci):
  return chess.FILE_NAMES.index(uci[0]), 7-chess.RANK_NAMES.index(uci[1])

def drawBoard(BOARD_COLORS):
  for cr, field in BOARD_COLORS.items():
    color = '#DFBF93' if field else '#C5844E'
    pg.draw.rect(screen, color, (*cr2xy(cr, flipped), FIELD, FIELD))

def fen2position(board_fen):
  position, c, r = {}, 0, 0
  for char in board_fen:
    if char.isalpha():
      position[(c,r)] = char
      c += 1
    elif char.isnumeric():
      c += int(char)
    elif char == '/':
      c, r = 0, r+1
    else:
      raise ValueError(board_fen)
  
  return position

def loadPieces():
  images = {}
  piece2file = dict(r = 'br', n='bn', b='bb', q='bq', k='bk', p='bp',
                    R = 'wr', N='wn', B='wb', Q='wq', K='wk', P='wp',)
  for piece, file in piece2file.items():
    image = pg.image.load(f'pieces/{file}.png')
    images[piece] = pg.transform.smoothscale(image, (FIELD, FIELD))
  
  return images

def drawPieces(p, flipped=False):
  for cr, piece in p.items():
    screen.blit(PIECES[piece], cr2xy(cr, flipped))

pg.init()
WIDTH, HEIGHT = 800, 800
FIELD = WIDTH // 8
FPS = 40
screen = pg.display.set_mode((WIDTH, HEIGHT))
BOARD_COLORS = {(r,c): r % 2 == c % 2 for r in range(8) for c in range(8)}
PIECES = loadPieces()
board = chess.Board()
position = fen2position(board.board_fen())
drag = None
flipped = True

go_on = True
clock = pg.time.Clock()

while go_on:
  clock.tick(FPS)
  for event in pg.event.get():
    if event.type == pg.QUIT:
      go_on = False
    
    elif event.type == pg.MOUSEBUTTONDOWN and not drag:
      
      from_pos = xy2cr(pg.mouse.get_pos(), flipped)
      
      if from_pos in position:
        piece = position[from_pos]
        drag = PIECES[piece]
        del position[from_pos]
    
    elif event.type == pg.MOUSEBUTTONUP and drag:
      to_pos = xy2cr(pg.mouse.get_pos(), flipped)    
      drag = None

      if from_pos != to_pos:
        uci = cr2uci(from_pos) + cr2uci(to_pos)
        move = chess.Move.from_uci(uci)

        if board.is_legal(move):
          board.push(move)

      position = fen2position(board.board_fen())
        
  screen.fill((0,0,0))
  
  drawBoard(BOARD_COLORS)
  drawPieces(position, flipped)

  if drag:
    rect = drag.get_rect(center=pg.mouse.get_pos())
    screen.blit(drag, rect)
  
  pg.display.flip()
  
pg.quit()