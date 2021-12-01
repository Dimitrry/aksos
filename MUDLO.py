import asyncio,random,curses,time,math,collections

screen = curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()
screen.nodelay(True)
screen.keypad(True)
PIZDA=""" 
.----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |   ______     | || |     _____    | || |   ________   | || |  ________    | || |      __      | |
| |  |_   __ \   | || |    |_   _|   | || |  |  __   _|  | || | |_   ___ `.  | || |     /  \     | |
| |    | |__) |  | || |      | |     | || |  |_/  / /    | || |   | |   `. \ | || |    / /\ \    | |
| |    |  ___/   | || |      | |     | || |     .'.' _   | || |   | |    | | | || |   / ____ \   | |
| |   _| |_      | || |     _| |_    | || |   _/ /__/ |  | || |  _| |___.' / | || | _/ /    \ \_ | |
| |  |_____|     | || |    |_____|   | || |  |________|  | || | |________.'  | || ||____|  |____|| |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------' """
frame1="""  .
 .'.
 |o|
.'o'.
|.-.|
'   '
 ( )
  )
 ( )"""

frame2="""  .
 .'.
 |o|
.'o'.
|.-.|
'   '
  )
 ( )
  ("""

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258

MENT,PIDAR=collections.defaultdict(list), collections.defaultdict(int)
speedlimit=3
fading=0.8
speedx,speedy=0,0
urodbetween=6
urodspeed=1
year=1957

aa,bb=screen.getmaxyx()
globalMaximumY=aa//2
globalMaximumX=bb/2
loop = asyncio.get_event_loop()

EXPLOSION_FRAMES = [
    r"""\
           (_)
       (  (   (  (
      () (  (  )
        ( )  ()
    """,
    r"""\
           (_)
       (  (   (
         (  (  )
          )  (
    """,
    r"""\
            (
          (   (
         (     (
          )  (
    """,
    r"""\
            (
              (
            (
    """,
]


gad1=r"""          ___
     ____/   \___
  __/           /
 /             |
|             __\
\       _____/
 \_____/
"""
gad2=r"""   _
,_(')<
\___)
"""
gad3=r"""    \  \  \  \
      \  \  \  \
   _____\__\__\__\__
  / \     HUBBLE    \
 | O |_______________)
  \_/_______\  \  \  \
             \  \  \  \
              \__\__\__\
"""
gad4=r""" _
(~)
 #
"""
gad5=r"""     ____
  __/    \
 /        \
/         _\
\     ___/
 \___/
"""
gad6=r"""     ___
   _/ o \
  /     /
  \____/
"""
async def ass():
    global year,urodspeed,urodbetween
    while True:
        screen.addstr(2,2,str(year))
        await asyncio.sleep(1.5)
        year+=1
        urodspeed=urodspeed*0.97
        urodbetween=urodbetween**0.97

def measuck(a):
    asuka = a.splitlines()
    sizz = max(len(gnida) for gnida in asuka)
    return [int(sizz),len(asuka)]

def deprive(a):
        return "\n".join(a.splitlines()[:-1])

async def explode(canvas, center_row, center_column):
    corner_row = center_row
    corner_column = center_column
    curses.beep()
    for frame in EXPLOSION_FRAMES:
        await draw_frame(canvas, corner_row, corner_column, frame)
        await asyncio.sleep(0.1)
        await draw_frame(canvas, corner_row, corner_column, frame, deletingMode=True)
        await asyncio.sleep(0.1)

def AIDS(X,Y):
  global speedx,speedy
  delta=math.cos(speedx/speedlimit)*0.75

  if X==-1:
      speedx+=X/2-delta
      if abs(speedx)>speedlimit:
          speedx=0-speedlimit
  if X==1:
      speedx+=X/2+delta
      if abs(speedx)>speedlimit:
          speedx=speedlimit
  if Y==-1:
      speedy+=Y/2-delta
      if abs(speedy)>speedlimit:
          speedy=0-speedlimit
  if Y==1:
      speedy+=Y/2+delta
      if abs(speedy)>speedlimit:
          speedy=speedlimit

  speedx,speedy=speedx*fading,speedy*fading
  if abs(speedx)<0.2:
      speedx=0
  if abs(speedy)<0.2:
      speedy=0
  return speedx,speedy

async def read_controls(canvas):
  global coordinateCorrectionY,coordinateCorrectionX,space_pressed,globalMaximumY,globalMaximumX
  canvas.nodelay(1)
  windowMaxY, windowMaxX= screen.getmaxyx()
  frameSizeX,frameSizeY=measuck(frame1)
  while True:
    pressed_key_code = canvas.getch()
    coordinateCorrectionY, coordinateCorrectionX = 0, 0
    space_pressed = False
    if pressed_key_code == 27:
      loop.close()
    if pressed_key_code == UP_KEY_CODE:
      coordinateCorrectionY = -1
    if pressed_key_code == DOWN_KEY_CODE:
      coordinateCorrectionY = 1
    if pressed_key_code == RIGHT_KEY_CODE:
      coordinateCorrectionX = 1
    if pressed_key_code == LEFT_KEY_CODE :
      coordinateCorrectionX = -1
    if pressed_key_code == SPACE_KEY_CODE:
      space_pressed = True

    a=AIDS(coordinateCorrectionX,coordinateCorrectionY)
    if space_pressed and year>2019:
        asyncio.create_task(fire(screen,globalMaximumY-1,globalMaximumX+measuck(frame1)[0]//2))
    globalMaximumX+=a[0]
    globalMaximumY+=a[1]
    if globalMaximumY<0:
      globalMaximumY=0
    if globalMaximumX<0:
      globalMaximumX =0
    if globalMaximumY>windowMaxY-frameSizeY:
      globalMaximumY=windowMaxY-frameSizeY
    if globalMaximumX>windowMaxX-frameSizeX:
      globalMaximumX=windowMaxX-frameSizeX
    curses.flushinp() # для стирания очереди нажатых кнопок
    await asyncio.sleep(0.2)

async def draw_frame(canvas, innerMaximumX, globalMaximumX, frame, deletingMode=False):
    frameStringList = frame.splitlines()

    if deletingMode == False:
      for frameString in range(len(frameStringList)):
        canvas.addstr(int(innerMaximumX + frameString), int(globalMaximumX), frameStringList[frameString])
        canvas.refresh()
    else:
      for frameString in range(len(frameStringList)):
        canvas.addstr(int(innerMaximumX + frameString), int(globalMaximumX), " " * (len(frameStringList[frameString])))
        canvas.refresh()
    await asyncio.sleep(0)


async def twinkleTheStars(screen=screen):
  x,y=screen.getmaxyx()[0],screen.getmaxyx()[1]
  starPositionY,starPositionX=random.randint(2,x),random.randint(2,y)
  starSymbol=random.choice(["*",".",":","+"])
  while True:
    screen.addstr(starPositionY,starPositionX,starSymbol,curses.A_DIM)
    screen.refresh()
    await asyncio.sleep(2)
    screen.addstr(starPositionY,starPositionX,starSymbol)
    await asyncio.sleep(0.3)
    screen.addstr(starPositionY,starPositionX,starSymbol,curses.A_BOLD)
    screen.refresh()
    await asyncio.sleep(0.5)
    screen.addstr(starPositionY,starPositionX,starSymbol)
    await asyncio.sleep(0.3)

async def urod(screen,i):
    global MENT,PIDAR
    aaa, bbb = screen.getmaxyx()
    gad = random.choice([gad1, gad2, gad3, gad4, gad5, gad6])
    susuck = measuck(gad)
    ay, bx = 1, random.randint(1, bbb - susuck[0])
    loframe=str()

    for i in range(susuck[1]+2):
        if i == 0 or i == (susuck[1]+1):
            loframe += "_" * (susuck[0]+2) + "\n"
        else:
            loframe += "|" + " " * (susuck[0]) + "|" + "\n"

    while True:
      await draw_frame(screen, ay-1, bx-1, loframe)
      await draw_frame(screen, ay, bx, gad)
      ttt = [ay, ay + susuck[1] + 1, bx, bx + susuck[0] + 2]
      MENT[i]=ttt

      await asyncio.sleep(urodspeed)
      await draw_frame(screen, ay-1, bx-1, loframe, deletingMode=True)
      if PIDAR[i] and PIDAR[i] == 1:
          PIDAR=collections.defaultdict(int)
          await explode(screen,ay,bx)
          return
      ay += 1
      if ay + susuck[1] > aaa - 1:
        gad = deprive(gad)
        loframe = deprive(loframe)
        if not deprive(gad):
          del MENT[i]
          return

async def gatherRoutines():
  routinesList=[]
  p = set()
  for i in range(25):
    routinesList.append(asyncio.create_task(twinkleTheStars()))
    await asyncio.sleep(0.05)
  routinesList.append(asyncio.create_task(drawAnimation(screen)))
  routinesList.append(asyncio.create_task(read_controls(screen)))
  routinesList.append(asyncio.create_task(ass()))
  ii=0
  while True:
    ii+=1
    p.add(asyncio.create_task(urod(screen,ii)))
    await asyncio.sleep(urodbetween)
    for i in p.copy():
      if i.done():
        p.remove(i)

async def fire(canvas, start_row, start_column, rows_speed=-1, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""
    global PIDAR
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')
    row += rows_speed
    column += columns_speed
    symbol = '-' if columns_speed else '|'
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0.05)
        canvas.addstr(round(row), round(column), ' ')
        for suka,ssuka in MENT.items():
            if ssuka[0]<round(row)<ssuka[1] and ssuka[2]-1< round(column)<ssuka[3]+1:
                canvas.addstr(10,10,"     "+str(suka))
                curses.beep()
                PIDAR[suka]=1
                return
        row += rows_speed
        column += columns_speed
    else:
        return

async def drawAnimation(screen):
  global globalMaximumY,globalMaximumX,MENT
  while True:
    innerMaximumX,innerMaximumY=globalMaximumY,globalMaximumX
    await draw_frame(screen,innerMaximumX,innerMaximumY,frame1)
    await asyncio.sleep(0.1)
    await draw_frame(screen, innerMaximumX,innerMaximumY, frame1,deletingMode=True)
    for suka, ssuka in MENT.items():
        if ssuka[0]-measuck(frame1)[1] < innerMaximumX < ssuka[1] and ssuka[2] - measuck(frame1)[0] < innerMaximumY < ssuka[3]:
            curses.beep()
            await draw_frame(screen,5,5,PIZDA)
            return
    await draw_frame(screen,innerMaximumX,innerMaximumY,frame2)
    await asyncio.sleep(0.1)
    await draw_frame(screen, innerMaximumX,innerMaximumY, frame2, deletingMode=True)

loop.run_until_complete(gatherRoutines())




