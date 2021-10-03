import pygame as pg
import chessdotcom as chess

def cr2xy(cr):
  return cr[0]*FIELD, cr[1]*FIELD

def xy2cr(xy):
  return xy[0] // FIELD, xy[1] // FIELD

def drawBoard(BOARD):
  for cr, field in BOARD.items():
    color = '#DFBF93' if field else '#C5844E'
    pg.draw.rect(screen, color, (*cr2xy(cr), FIELD, FIELD))

def fen2position(fen):
  position, c, r = {}, 0, 0
  piece_placement, active_color, castling, enpassant, hmoves50, fmoves = fen.split()
  for char in piece_placement:
    if char.isalpha():
      position[(c,r)] = char
      c += 1
    elif char.isnumeric():
      c += int(char)
    elif char == '/':
      c, r = 0, r+1
    else:
      raise ValueError(piece_placement)
  
  return position, active_color

def loadPieces():
  images = {}
  piece2file = dict(r = 'br', n='bn', b='bb', q='bq', k='bk', p='bp',
                    R = 'wr', N='wn', B='wb', Q='wq', K='wk', P='wp',)
  for piece, file in piece2file.items():
    image = pg.image.load(f'pieces/{file}.png')
    images[piece] = pg.transform.smoothscale(image, (FIELD, FIELD))
  
  return images

def drawPieces(p):
  for cr, piece in p.items():
    screen.blit(PIECES[piece], cr2xy(cr))

pg.init()
WIDTH, HEIGHT = 800, 800
FIELD = WIDTH // 8
FPS = 40
screen = pg.display.set_mode((WIDTH, HEIGHT))
BOARD = {(r,c): r % 2 == c % 2 for r in range(8) for c in range(8)}
PIECES = loadPieces()
# fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
fen = chess.get_random_daily_puzzle().json['puzzle']['fen']
position, active_color = fen2position(fen)
drag = None

go_on = True
clock = pg.time.Clock()

while go_on:
  clock.tick(FPS)
  for event in pg.event.get():
    if event.type == pg.QUIT:
      go_on = False
    elif event.type == pg.MOUSEBUTTONDOWN and not drag:
      from_pos = xy2cr(pg.mouse.get_pos())
      if from_pos in position:
        piece = position[from_pos]
        drag = PIECES[piece]
        del position[from_pos]
    elif event.type == pg.MOUSEBUTTONUP and drag:
      to_pos = xy2cr(pg.mouse.get_pos())
      position[to_pos] = piece
      drag = None
  
  screen.fill((0,0,0))
  
  drawBoard(BOARD)
  drawPieces(position)
  if drag:
    rect = drag.get_rect(center=pg.mouse.get_pos())
    screen.blit(drag, rect)
  
  pg.display.flip()
  
pg.quit()