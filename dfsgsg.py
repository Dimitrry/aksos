import asyncio,random,curses,time

screen = curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()
screen.nodelay(True)
screen.keypad(True)
gad1="""  .
 .'.
 |o|
.'o'.
|.-.|
'   '
 ( )
  )
 ( )"""

gad2="""  .
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
aaa=aa//2
bbb=bb/2

async def read_controls(canvas,s=1):
  global rowd,cold,space_pressed,aaa,bbb
  canvas.nodelay(1)
  asuk, bsuk= screen.getmaxyx()
  while True:
    pressed_key_code = canvas.getch()
    rowd, cold = 0, 0
    space_pressed = False
    if pressed_key_code == 27:
      loop.close()
    if pressed_key_code == UP_KEY_CODE:
      rowd = -1
    if pressed_key_code == DOWN_KEY_CODE:
      rowd = 1
    if pressed_key_code == RIGHT_KEY_CODE:
      cold = 1
    if pressed_key_code == LEFT_KEY_CODE :
      cold = -1
    if pressed_key_code == SPACE_KEY_CODE:
      space_pressed = True
    if rowd!=0 or cold!=0:
      bbb+=cold*s
      aaa+=rowd*s
      if aaa<0:
        aaa=0
      if bbb<0:
        bbb =0
      if aaa>asuk-asiz:
        aaa=asuk-asiz
      if bbb>bsuk-bsiz:
        bbb=bsuk-bsiz
      # screen.addstr(10, 10, str(10)+"  "+str(aaa) +"  "+ str(bbb))
      screen.refresh()
      curses.flushinp() # для стирания очереди нажатых кнопок

    await asyncio.sleep(0.2)

async def draw_frame(canvas, ax, bx, text, die=False):
    asuka = text.splitlines()
    global asiz,bsiz
    asiz=len(asuka)
    bsiz=max(len(gnida) for gnida in asuka)
    if die == False:
      for aaaa in range(len(asuka)):
        # canvas.addstr(20, 20, str(20) + "  " + str(ax+aaaa) + "  " + str(bx)+ "  " +str(aaaa))
        canvas.addstr(int(ax + aaaa), int(bx), asuka[aaaa])
        canvas.refresh()
        curses.beep()
    else:
      for aaaa in range(len(asuka)):
        canvas.addstr(int(ax + aaaa), int(bx), " " * (len(asuka[aaaa])))
        canvas.refresh()
    await asyncio.sleep(0)


async def blind(a=screen):
  x,y=screen.getmaxyx()[0],screen.getmaxyx()[1]
  b,c=random.randint(2,x),random.randint(2,y)
  sym=random.choice(["*",".",":","+"])
  while True:
    a.addstr(b,c,sym,curses.A_DIM)
    a.refresh()
    await asyncio.sleep(2)
    a.addstr(b,c,sym)
    a.refresh()
    await asyncio.sleep(0.3)
    a.addstr(b,c,sym,curses.A_BOLD)
    a.refresh()
    await asyncio.sleep(0.5)
    a.addstr(b,c,sym)
    a.refresh()
    await asyncio.sleep(0.3)
loop = asyncio.get_event_loop()

async def suka():
  p=[]
  for i in range(15):
    p.append(asyncio.create_task(blind()))
    await asyncio.sleep(0.05)
  p.append(asyncio.create_task(urod(screen)))
  p.append(asyncio.create_task(read_controls(screen,4)))
  await asyncio.wait(p)

async def urod(screen):
  global aaa,bbb
  while True:
    ax,bx=aaa,bbb
    # screen.addstr(15, 15, str(15) + "  " + str(ax) + "  " + str(bx))
    screen.refresh()
    await draw_frame(screen,ax,bx,gad1)
    await asyncio.sleep(0.1)
    await draw_frame(screen, ax,bx, gad1,die=True)
    await draw_frame(screen,ax,bx,gad2)
    await asyncio.sleep(0.1)
    await draw_frame(screen, ax,bx, gad2, die=True)


loop.run_until_complete(suka())

# suka главная функция управляющая корутинами
# urod функция управляющая сменой анимаций корабля
# blind функция отрисовывающая звёзды и заставляющая их асинхронно мигать
# read_controls считывает клавиши управления
# p список корутин, не используется
# asuka список строк кадра анимации
# asiz bsiz высота и ширина кадра анимации корабля
# screen это объект window библиотеки curses
# aaa bbb координаты корабля по y и x
# ax bx координаты корабля внутри функции urod чтобы изменение aaa и bbb от нажатия клавиш управления не сбивало анимацию в середине цикла
# b c sym это случайные координаты звёзд и случайный символ для звезды
# rowd cold это поправка к координатам корабля, вызванная нажатием клавиши управления
# aa asuk высота окна screen ,bb, bsuk ширина окна screen



