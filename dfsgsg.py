import asyncio,random,curses,time

screen = curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()
screen.nodelay(True)
screen.keypad(True)
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

aa,bb=screen.getmaxyx()
globalMaximumY=aa//2
globalMaximumX=bb/2
loop = asyncio.get_event_loop()

async def read_controls(canvas,shipSpeed=1):
  global coordinateCorrectionY,coordinateCorrectionX,space_pressed,globalMaximumY,globalMaximumX
  canvas.nodelay(1)
  windowMaxY, windowMaxX= screen.getmaxyx()
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
    if coordinateCorrectionY!=0 or coordinateCorrectionX!=0:
      globalMaximumX+=coordinateCorrectionX*shipSpeed
      globalMaximumY+=coordinateCorrectionY*shipSpeed
      if globalMaximumY<0:
        globalMaximumY=0
      if globalMaximumX<0:
        globalMaximumX =0
      if globalMaximumY>windowMaxY-frameSizeY:
        globalMaximumY=windowMaxY-frameSizeY
      if globalMaximumX>windowMaxX-frameSizeX:
        globalMaximumX=windowMaxX-frameSizeX
      # screen.addstr(10, 10, str(10)+"  "+str(globalMaximumY) +"  "+ str(globalMaximumX))
      curses.flushinp() # для стирания очереди нажатых кнопок

    await asyncio.sleep(0.2)

async def draw_frame(canvas, innerMaximumX, globalMaximumX, frame, deletingMode=False):
    frameStringList = frame.splitlines()
    global frameSizeY,frameSizeX
    frameSizeY=len(frameStringList)
    frameSizeX=max(len(string) for string in frameStringList)
    if deletingMode == False:
      for frameString in range(len(frameStringList)):
        # canvas.addstr(20, 20, str(20) + "  " + str(ax+frameString) + "  " + str(globalMaximumX)+ "  " +str(frameString))
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


async def gatherRoutines():
  routinesList=[]
  for i in range(25):
    routinesList.append(asyncio.create_task(twinkleTheStars()))
    await asyncio.sleep(0.05)
  routinesList.append(asyncio.create_task(drawAnimation(screen)))
  routinesList.append(asyncio.create_task(read_controls(screen,shipSpeed=4)))
  await asyncio.wait(routinesList)

async def drawAnimation(screen):
  global globalMaximumY,globalMaximumX
  while True:
    innerMaximumX,innerMaximumY=globalMaximumY,globalMaximumX
    # screen.addstr(15, 15, str(15) + "  " + str(ax) + "  " + str(bx))
    await draw_frame(screen,innerMaximumX,innerMaximumY,frame1)
    await asyncio.sleep(0.1)
    await draw_frame(screen, innerMaximumX,innerMaximumY, frame1,deletingMode=True)
    await draw_frame(screen,innerMaximumX,innerMaximumY,frame2)
    await asyncio.sleep(0.1)
    await draw_frame(screen, innerMaximumX,innerMaximumY, frame2, deletingMode=True)


loop.run_until_complete(gatherRoutines())

# gatherRoutines главная функция управляющая корутинами
# drawAnimation функция управляющая сменой анимаций корабля
# twinkleTheStars функция отрисовывающая звёзды и заставляющая их асинхронно мигать
# read_controls считывает клавиши управления
# p список корутин, не используется
# frameStringList список строк кадра анимации
# frameSizeY frameSizeX высота и ширина кадра анимации корабля
# screen это объект window библиотеки curses
# globalMaximumY globalMaximumX координаты корабля по y и x
# ax bx координаты корабля внутри функции drawAnimation чтобы изменение globalMaximumY и globalMaximumX от нажатия клавиш управления не сбивало анимацию в середине цикла
# b c starSymbol это случайные координаты звёзд и случайный символ для звезды
# coordinateCorrectionY coordinateCorrectionX это поправка к координатам корабля, вызванная нажатием клавиши управления
# aa windowMaxY высота окна screen ,bb, windowMaxX ширина окна screen



