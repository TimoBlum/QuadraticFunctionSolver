import pygame
pygame.init()

xy = 1000
win = pygame.display.set_mode((xy, xy))
pygame.display.set_caption("Quadratic Function Solver")
clock = pygame.time.Clock()
rows = 10
spacebtwn = xy // rows
run = True


def euclidian(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1) ** 2) + (y2 - y1) ** 2)


def clickedOn(place, radius):
    pos = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed(3)
    if euclidian(pos[0], pos[1], place[0], place[1]) < radius and mouse[0]:
        return True
    else:
        return False


def textOnScreen(x, y, text1, text2, big, color=(220, 200, 200)):
    font = pygame.font.Font('freesansbold.ttf', big)
    txt = str(text1) + str(text2)
    text = font.render(txt, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    win.blit(text, textRect)


def drawGrid():
    """Draw a grid"""
    global win, xy
    x = 0
    y = 0
    for l in range(rows):
        pygame.draw.line(win, (220, 220, 220), (x, 0), (x, xy))
        pygame.draw.line(win, (220, 220, 220), (0, y), (xy, y))

        x = x + spacebtwn
        y = y + spacebtwn
    pygame.draw.line(win, (30, 30, 30), (0, xy/2), (xy, xy/2), width=2)
    pygame.draw.line(win, (30, 30, 30), (xy/2, 0), (xy/2, xy), width=2)


def drawPoint(x, y):
    pygame.draw.circle(win, (50, 255, 40), (x, y), 1)


class Slider:
    def __init__(self, abc):
        if abc == "a":
            self.handleXdef = 50
            self.handleYdef = xy-175
            self.handleX = self.handleXdef
            self.handleY = self.handleYdef
            self.slideX = 50
            self.slideY = xy-150
            self.handleRect = pygame.Rect(self.handleX, self.handleY, 50, 100)
            self.slideRect = pygame.Rect(self.slideX, self.slideY, 250, 50)

        if abc == "b":
            self.handleXdef = 375
            self.handleYdef = xy-175
            self.handleX = self.handleXdef+100
            self.handleY = self.handleYdef
            self.slideX = 375
            self.slideY = xy-150
            self.handleRect = pygame.Rect(self.handleX, self.handleY, 50, 100)
            self.slideRect = pygame.Rect(self.slideX, self.slideY, 250, 50)

        if abc == "c":
            self.handleXdef = xy-300
            self.handleYdef = xy-175
            self.handleX = self.handleXdef+100
            self.handleY = self.handleYdef
            self.slideX = xy-300
            self.slideY = xy-150
            self.handleRect = pygame.Rect(self.handleX, self.handleY, 50, 100)
            self.slideRect = pygame.Rect(self.slideX, self.slideY, 250, 50)

        self.grabbedHandle = False
        self.grabTimer = 0

    def draw(self):
        self.handleRect = pygame.Rect(self.handleX, self.handleY, 50, 100)
        pygame.draw.rect(win, (230, 230, 230), self.slideRect)
        pygame.draw.rect(win, (190, 190, 190), self.handleRect)

    def interact(self):
        mouse = pygame.mouse.get_pressed(3)
        pos = pygame.mouse.get_pos()
        # Detect any presses on the Slider handle and then lock the handle onto the mouse x coordinate until pressed again
        if self.handleRect.collidepoint(pos) and mouse[0] and self.grabTimer < 0 and self.grabbedHandle == False:
            print("grabbed Handle")
            self.grabbedHandle = True
            self.grabTimer = 30
        if self.grabbedHandle and mouse[0] and self.grabTimer < 0:
            self.grabbedHandle = False
            self.grabTimer = 30
            print("lost Handle")
        self.grabTimer -= 1
        # Adds limits to the slider
        if self.grabbedHandle:
            self.handleX = pos[0]-self.handleRect.width/2
            if self.handleX + self.handleRect.width > self.handleXdef + self.slideRect.width:
                self.handleX = self.handleXdef + self.slideRect.width - self.handleRect.width
            elif self.handleX < self.handleXdef:
                self.handleX = self.handleXdef


aSlider = Slider("a")
bSlider = Slider('b')
cSlider = Slider('c')


def func(a, b, c):
    """Takes the vertex form of a quadratic function as such: a(x-b)**2 +c"""
    x = -xy
    while x < 600:
        dx = x
        dy = (0.01*a*((x+b*100)**2)+c*100)
        drawPoint(dx+xy/2, xy/2-dy)
        x += 0.1


def redrawWin():
    win.fill((255, 255, 255))
    drawGrid()
    textOnScreen(150, 50, "Mouse position is: ", str((pygame.mouse.get_pos()[0]/100)-5)[:4]+"  "+str(((pygame.mouse.get_pos()[1]/100)-5)*-1)[:4], 20)
    aSlider.draw(), aSlider.interact()
    bSlider.draw(), bSlider.interact()
    cSlider.draw(), cSlider.interact()
    a = 0.2+(aSlider.handleX-aSlider.handleXdef)/25
    b = -4+(bSlider.handleX-bSlider.handleXdef)/25
    c = -4+(cSlider.handleX-cSlider.handleXdef)/25
    textOnScreen(xy-200, 50, "Quadratic function: ", str(a)[:4]+"(x + " + str(b)[:4] + ")2 + " + str(c)[:4], 20)
    textOnScreen(aSlider.slideX+aSlider.slideRect.width/2, xy-50, "a value is: ", str(a)[:4], 20)
    textOnScreen(bSlider.slideX+bSlider.slideRect.width/2, xy-50, "b value is: ", str(b)[:4], 20)
    textOnScreen(cSlider.slideX+cSlider.slideRect.width/2, xy-50, "c value is: ", str(c)[:4], 20)
    func(a, b, c)
    pygame.display.update()


def main():
    global run
    while run:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if run:
            redrawWin()


main()
