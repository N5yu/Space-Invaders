#импортирую все необходимые библиотеки
import pygame
import random
import sys
import math

#состояние игры
running = True
#Необходимые для игры группы спрайтов для игрока, врагов и боссов.
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
bosses = pygame.sprite.Group()
# Инициализация Pygame
pygame.init()

pygame.mixer.music.load('assets/sound effects/Remi_Gallego_-_Malware_Injection_67119636.mp3')# Загрузка файла с музыкой
shoot_sound = pygame.mixer.Sound('assets/sound effects/shoot_sound.mp3')
pause_sound = pygame.mixer.Sound('assets/sound effects/pause.mp3')
invade_kill = pygame.mixer.Sound('assets/sound effects/inv_kill.mp3')
player_kill = pygame.mixer.Sound('assets/sound effects/player_kill.mp3')

# Размеры экрана
screen_width = 800
screen_height = 600

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (230, 117, 92)

# Верхний левый угол текста
text_position = (50, 50)



# Создание экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Загрузка изображений
player_img = pygame.image.load("assets/player.png")
enemy_shot = pygame.image.load("assets/shoot.png")
enemy_img = pygame.image.load("assets/enemy.png")
img_win = pygame.image.load("assets/img_win.png")
img_win = pygame.transform.scale(img_win, (screen_width, screen_height))
enemy_armor = pygame.image.load("assets/armoredEnemy.png")
menu_background = pygame.image.load("assets/menu_background.png")
bullet_img = pygame.image.load("assets/bullet.png")
img_gv = pygame.image.load("assets/img_gameover.png")
boss_img = pygame.image.load("assets/boss1.png")
boss_inv = pygame.image.load("assets/boss1_inv.png")
bg_img = pygame.image.load("assets/starfield.png")  # Загрузка изображения фона
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))  # Масштабирование фона


#класс Button, который используется для создания кнопок в меню игры.
class Button:
    def __init__(self, x, y, width, height, text=None, color=(173, 216, 230), highlighted_color=(191, 239, 255)):# метод-конструктор инициализирует объект кнопка при его создании, принимает несколько аргументов
        self.rect = pygame.Rect(x, y, width, height)#Создается прямоугольник (объект класса pygame.Rect), который определяет положение и размер кнопки на экране. Координаты верхнего левого угла кнопки указываются в аргументах x и y, а ширина и высота - в аргументах width и height.
        self.color = color#Задается основной цвет кнопки, который указан в аргументе color.
        self.highlighted_color = highlighted_color#Задается цвет кнопки при наведении мыши, указанный в аргументе highlighted_color.
        self.text = text#Задается текст, который будет отображаться на кнопке. Если text равен None, то кнопка не будет содержать текст.
        if self.text is not None:
            self.font = pygame.font.Font("assets/space_invaders.ttf", 20)#шрифт используемый при написании текста на кнопке и его размер
            self.text_surface = self.font.render(self.text, True, (255, 255, 255))#Создается поверхность (surface), содержащая текст кнопки. Эта поверхность создается из текста self.text с использованием шрифта self.font. Также задается цвет текста (белый) и параметр True, который указывает на сглаживание текста.
        self.is_highlighted = False# Инициализируется атрибут is_highlighted, который показывает, находится ли указатель мыши над кнопкой (по умолчанию False).

    def check_mouseover(self, pos):# Это метод, который проверяет, находится ли указатель мыши над кнопкой
        if self.rect.collidepoint(pos):#Это условие проверяет, пересекается ли прямоугольник кнопки (self.rect) с точкой, на которой находится указатель мыши (pos). Если это условие выполняется, значит указатель мыши находится над кнопкой.
            self.is_highlighted = True# Если указатель мыши находится над кнопкой, то атрибут is_highlighted кнопки устанавливается в True, что означает, что кнопка подсвечивается.
        else:
            self.is_highlighted = False#Если указатель мыши не находится над кнопкой, то атрибут is_highlighted кнопки устанавливается в False, что означает, что кнопка не подсвечивается.

    def draw(self, screen):# Это метод, который рисует кнопку на экране.
        color = self.highlighted_color if self.is_highlighted else self.color#Здесь определяется цвет, который будет использоваться для отрисовки кнопки. Если атрибут is_highlighted равен True, то используется цвет highlighted_color (цвет кнопки при наведении мыши), иначе используется color (основной цвет кнопки)
        pygame.draw.rect(screen, color, self.rect)# Эта строка рисует прямоугольник (кнопку) на поверхности screen с указанным цветом color. Размер и позиция кнопки задаются атрибутом self.rect.
        if self.text is not None:#Это условие проверяет, есть ли текст на кнопке.
            text_rect = self.text_surface.get_rect(center=self.rect.center)#Здесь создается прямоугольник, который будет содержать текст кнопки. Этот прямоугольник будет центрирован по отношению к прямоугольнику кнопки (self.rect).
            screen.blit(self.text_surface, text_rect)#Эта строка отображает текст кнопки (self.text_surface) на поверхности screen в соответствии с прямоугольником text_rect, который был создан ранее. Текст будет отцентрирован внутри кнопки.
# Функция для вывода текста на экран
def draw_text(text, font_size, x, y):#Функция для написания текста с определенными параметрами
    font = pygame.font.Font("assets/space_invaders.ttf", font_size)#Шрифт используемый при написании текста на кнопке и его размер
    text_surface = font.render(text, True, WHITE)#Эта строка создает поверхность (text_surface), на которой будет отображен текст. Функция render берет текст (text), указанный шрифт (font), и цвет текста (WHITE), чтобы создать изображение текста.
    text_rect = text_surface.get_rect()#Здесь создается прямоугольник (text_rect), который охватывает изображение текста. Этот прямоугольник будет использоваться для центрирования текста на экране.
    text_rect.center = (x, y)#Этот код устанавливает координаты центра прямоугольника text_rect в соответствии с переданными аргументами x и y
    screen.blit(text_surface, text_rect)#Эта строка отображает текстовую поверхность text_surface на экране (screen) с учетом прямоугольника text_rect.

def draw_textred(text, font_size, x, y):#Тоже самое только цвет другой
    font = pygame.font.Font("assets/space_invaders.ttf", font_size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_text1(text, font_size, x, y):#Тоже самое только шрифт другой
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Функция для отображения gameover
def gameover_screen():
    gameover = True#Эта строка создает переменную gameover и устанавливает ее значение в True. Эта переменная используется для управления циклом отображения экрана "Game Over".
    menu_button = Button(350, 350, 100, 50, 'Menu', color=(128, 128, 128))#Здесь создается экземпляр класса Button (кнопки) с заданными параметрами.
    while gameover:# Это начало цикла, который будет выполняться, пока значение переменной gameover равно True
        for event in pygame.event.get():#Этот блок начинает цикл для обработки событий Pygame, таких как нажатие клавиш или мыши.
            if event.type == pygame.QUIT:#Это условие проверяет, если происходит событие закрытия окна (нажатие крестика), то игра завершается. Функции pygame.quit() и sys.exit() используются для корректного завершения игры.
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:# Это условие проверяет, если происходит событие нажатия кнопки мыши.
                if event.button == 1:#Это условие проверяет, если нажата левая кнопка мыши (код 1), то выполняются следующие действия.
                    if menu_button.is_highlighted:#Это условие проверяет, если кнопка menu_button под курсором мыши была выделена (highlighted), что означает, что курсор находится над кнопкой "Menu".
                        gameover = False# Если кнопка "Menu" была выделена и нажата левая кнопка мыши, то значение переменной gameover устанавливается в False, что приводит к завершению цикла gameover и выходу из него.
                        main_menu()#Эта функция вызывает главное меню игры, чтобы игрок мог вернуться в основное меню.
                        reset_game()#Эта функция вызывается для сброса игры к начальному состоянию.
        mouse_pos = pygame.mouse.get_pos()#Эта строка получает текущие координаты курсора мыши на экране и сохраняет их в переменной mouse_pos.
        menu_button.check_mouseover(mouse_pos)# Здесь вызывается метод check_mouseover кнопки menu_button с передачей текущих координат курсора мыши. Этот метод определяет, выделена ли кнопка курсором, и устанавливает соответствующее значение is_highlighted.
        screen.blit(img_gv, (0, 0))# Эта строка отображает изображение "img_gv" на экране в позиции (0, 0), что создает фон для экрана "Game Over".
        draw_textred("GAME", 32, screen_width // 2, 120,)#Здесь вызывается функция draw_textred для отображения текста "GAME" с размером шрифта 32, в центре экрана по горизонтали и на высоте 120 пикселей по вертикали.
        draw_textred("OVER!", 32, screen_width // 2, 162)#Тоже самое
        draw_text("Your score: " + str(score), 32, screen_width // 2,204)
        draw_text("Press the menu button to return to the main menu.", 22, screen_width // 2, 250)
        menu_button.draw(screen)#Здесь отображается кнопка "Menu" на экране с учетом текущего состояния (выделена или нет).
        pygame.display.update()#Этот код обновляет экран, чтобы отобразить все изменения, сделанные в текущем кадре.


class Slider:#Это определение класса Slider, который представляет ползунок для регулировки громкости. Он содержит методы для отображения и управления ползунком.
    def __init__(self, x, y, width, height, min_val, max_val, init_val, color=(255, 255, 255), sounds=None):#Это конструктор класса Slider, который инициализирует ползунок с указанными параметрами: x, y: Координаты верхнего левого угла прямоугольника ползунка. width, height: Ширина и высота прямоугольника ползунка. min_val, max_val: Минимальное и максимальное значение ползунка. init_val: Начальное значение ползунка. color: Цвет ползунка (по умолчанию белый).
        self.rect = pygame.Rect(x, y, width, height)#Создает прямоугольник для рамки ползунка.
        self.handle_rect = pygame.Rect(self.rect.right, y, 10, height) #Создает прямоугольник для "ручки" ползунка, начиная справа от рамки.
        self.min = min_val#Устанавливает минимальное значение ползунка.
        self.max = max_val#Устанавливает максимальное значение ползунка.
        self.range = self.max - self.min#Рассчитывает диапазон значений ползунка.
        self.value = init_val#Устанавливает текущее значение ползунка.
        self.color = color#Устанавливает цвет ползунка.
        self.dragging = False#Переменная для отслеживания состояния "перетаскивания" ползунка.
        self.sounds = sounds

    def draw(self, screen):#Метод для отрисовки ползунка на экране
        pygame.draw.rect(screen, self.color, self.rect, 2)#Эта строка рисует рамку ползунка на экране. Вот, что означают аргументы: screen: Это объект экрана, на котором будет выполнена отрисовка. self.color: Это цвет рамки, который был определен при создании экземпляра класса Slider. self.rect: Это прямоугольник, представляющий рамку ползунка, с координатами и размерами, которые были заданы при создании экземпляра класса Slider. 2: Это толщина линии рамки. Здесь устанавливается значение 2, что означает, что рамка будет нарисована линией толщиной в 2 пикселя.
        pygame.draw.rect(screen, self.color, self.handle_rect)#Эта строка рисует "ручку" ползунка.

    def check_mouseover(self, pos):#Этот метод проверяет, находится ли указатель мыши (представленный координатами pos) на "ручке" ползунка
        if self.handle_rect.collidepoint(pos):#Это проверка, используя метод collidepoint(), определенный для прямоугольника self.handle_rect. Метод collidepoint() проверяет, находится ли заданная точка (в данном случае, pos) внутри прямоугольника self.handle_rect. Если pos находится внутри self.handle_rect, это означает, что указатель мыши находится на "ручке" ползунка, и условие становится True.
            self.dragging = True
        else:
            self.dragging = False#Если условие self.handle_rect.collidepoint(pos) оценивается как False, то это означает, что указатель мыши не находится на "ручке" ползунка. В таком случае, флаг self.dragging устанавливается в False, указывая, что перетаскивание не выполняется.

    def move_slider(self, pos, is_button_down):#Эта строка проверяет два условия. Во-первых, self.dragging - это флаг, который устанавливается в True, если пользователь начал перетаскивание ползунка, иначе он равен False. Во-вторых, is_button_down - это флаг, который указывает, нажата ли кнопка мыши. Таким образом, это условие выполняется только тогда, когда ползунок перетаскивается и кнопка мыши удерживается.
        if self.dragging and is_button_down:
            self.handle_rect.centerx = pos[0]# Эта строка устанавливает горизонтальную координату центра прямоугольника handle_rect (ползунка) в pos[0], что является текущей горизонтальной координатой указателя мыши. Это перемещает ползунок горизонтально в соответствии с движением мыши.
            if self.handle_rect.left < self.rect.left:#Это условие проверяет, не вышел ли ползунок за левую границу слайдера. Если да, то self.handle_rect.left устанавливается на позицию левой границы слайдера (self.rect.left), что предотвращает выход за границы.
                self.handle_rect.left = self.rect.left
            if self.handle_rect.right > self.rect.right:#Это условие проверяет, не вышел ли ползунок за правую границу слайдера. Если да, то self.handle_rect.right устанавливается на позицию правой границы слайдера (self.rect.right), что также предотвращает выход за границы.
                self.handle_rect.right = self.rect.right
            self.value = (((self.handle_rect.centerx-self.rect.left) / self.rect.width) * self.range) + self.min#Эта строка обновляет значение переменной self.value, которая представляет выбранное пользователем значение на слайдере
            '''
            (self.handle_rect.centerx - self.rect.left) - Это вычисляет текущее положение ползунка относительно левой границы слайдера.
            self.rect.width - Это ширина слайдера.
            ((self.handle_rect.centerx - self.rect.left) / self.rect.width) - Это отношение положения ползунка к ширине слайдера и показывает, насколько далеко перетащен ползунок от левой границы.
            ((self.handle_rect.centerx - self.rect.left) / self.rect.width) * self.range - Это масштабирует значение в диапазоне от 0 до self.range.
            ((self.handle_rect.centerx - self.rect.left) / self.rect.width) * self.range + self.min - Это смещает масштабированное значение, чтобы оно находилось в диапазоне от self.min до self.max. В итоге это значение представляет выбранное положение ползунка в числовом диапазоне, установленном при создании слайдера.
            '''
            if self.sounds is not None:  # Это условное выражение, которое проверяет, существует ли атрибут self.sounds объекта self и не равен ли он None. Если это условие истинно, то выполнится следующий блок кода.
                for sound in self.sounds:  # Это начало цикла for, который перебирает элементы из объекта self.sounds. self.sounds является итерируемым объектом, списком или другой структурой данных, содержащей звуковые объекты.
                    sound.set_volume(self.value)  # Эта строка вызывает метод set_volume для каждого объекта sound в self.sounds. Метод set_volume вызывается с аргументом self.value, который, содержит значение громкости или уровня громкости, который будет применен к текущему звуковому объекту.



def settings_menu():#Эта функция представляет экран настроек звука в игре.
    global running
    back_button = Button(350, 400, 110, 60, 'Back', color=(128, 128, 128))#Создается экземпляр класса Button с параметрами, которые определяют кнопку "Back" в меню настроек звука. Эта кнопка позволит пользователю вернуться в главное меню.
    music_volume_slider = Slider(100, 250, 600, 20, 0, 1, pygame.mixer.music.get_volume())#Создается экземпляр класса Slider с параметрами, которые определяют ползунок для настройки громкости музыки. Параметры включают начальные координаты (100, 250), ширину и высоту ползунка (600, 20), минимальное и максимальное значение (0 и 1 соответственно) и начальное значение громкости, которое берется из текущего значения громкости музыки в Pygame (pygame.mixer.music.get_volume()).
    shoot_volume_slider = Slider(100, 350, 600, 20, 0, 1, shoot_sound.get_volume(), sounds=[shoot_sound, invade_kill, pause_sound, player_kill])

    while running:#Это бесконечный цикл, который выполняется, пока переменная running установлена в True. Этот цикл используется для отображения экрана настроек звука и взаимодействия с пользователем.
        screen.blit(menu_background, (0, 0))#Здесь задний фон для экрана настроек звука (menu_background) рисуется на экране, начиная с координат (0, 0).
        draw_text("Sound Settings", 36, screen_width // 2, 30)#Эта строка рисует текст "Sound Settings" на экране.
        draw_text("Audio", 32, screen_width // 2, 230)#Здесь рисуется текст "Audio" на экране.
        draw_text("Sound Effects", 32, screen_width // 2, 330)
        mouse_pos = pygame.mouse.get_pos()# Эта строка получает текущие координаты указателя мыши в переменной mouse_pos. Эти координаты будут использоваться для определения, на какие элементы экрана указывает пользователь, в частности, на кнопку "Back" и ползунок громкости музыки.

        for event in pygame.event.get():#Этот цикл перебирает все события, которые произошли в Pygame.
            if event.type == pygame.MOUSEBUTTONDOWN:#Этот блок проверяет, произошло ли событие нажатия кнопки мыши.
                if event.button == 1:#Этот блок проверяет, была ли нажата левая кнопка мыши (1 - левая кнопка, 2 - средняя кнопка, 3 - правая кнопка).
                    back_button.check_mouseover(mouse_pos)#Если левая кнопка мыши была нажата, выполняется функция check_mouseover для кнопки "Back". Это проверяет, находится ли указатель мыши над кнопкой "Back" и, если да, устанавливает флаг is_highlighted для кнопки.
                    music_volume_slider.check_mouseover(mouse_pos)#Аналогично, проверяется, находится ли указатель мыши над ползунком громкости музыки, и устанавливает флаг dragging для ползунка, если он находится в области ползунка.
                    shoot_volume_slider.check_mouseover(mouse_pos)
            if event.type == pygame.MOUSEMOTION:#Этот блок проверяет события движения мыши.
                shoot_volume_slider.move_slider(mouse_pos, pygame.mouse.get_pressed()[0])
                shoot_sound.set_volume(shoot_volume_slider.value)
                music_volume_slider.move_slider(mouse_pos, pygame.mouse.get_pressed()[0])#Если событие MOUSEMOTION произошло, функция move_slider вызывается для ползунка громкости музыки. Эта функция обновляет положение ползунка, основываясь на текущем положении мыши. Если левая кнопка мыши удерживается (условие pygame.mouse.get_pressed()[0]), то ползунок перемещается.
                pygame.mixer.music.set_volume(music_volume_slider.value)#Устанавливается громкость музыки в Pygame в соответствии с текущим положением ползунка. music_volume_slider.value - это текущее значение ползунка, и оно используется для установки громкости музыки.
            if event.type == pygame.MOUSEBUTTONUP:#Этот блок проверяет, произошло ли событие отпускания кнопки мыши.
                if event.button == 1:#Этот блок проверяет, была ли отпущена левая кнопка мыши.
                    if back_button.is_highlighted:#Если левая кнопка мыши была отпущена и кнопка "Back" была выделена (указатель мыши находился над кнопкой "Back"), то функция settings_menu() завершает выполнение и возвращается в предыдущий экран (главное меню).
                        return
            if event.type == pygame.QUIT:#Этот блок проверяет, произошло ли событие закрытия окна.
                running = False

        back_button.draw(screen)#Этот вызов отрисовывает кнопку "Back" на экране. Кнопка рисуется с заданными координатами и цветом на поверхности screen.
        music_volume_slider.draw(screen)#Этот вызов отрисовывает ползунок громкости музыки на экране.
        shoot_volume_slider.draw(screen)

        pygame.display.update()#Этот вызов обновляет отображение на экране.
        clock.tick(60)#Этот вызов ограничивает скорость обновления экрана до 60 кадров в секунду.
#Функция для отображения стартового меню
def main_menu():
    global running#Эта строка указывает на то, что переменная running будет использоваться внутри этой функции и изменение её значения будет влиять на глобальное значение этой переменной.
    quit_button = Button(350, 430, 120, 60, 'Quit', color=(255, 0, 0))#Здесь создается экземпляр класса Button для кнопки "Quit" с заданными параметрами.
    start_button = Button(350, 270, 120, 60, 'Start', color=(128, 128, 128))#Эта строка создает экземпляр класса Button для кнопки "Start" с аналогичными параметрами.
    setting_button = Button(350, 350, 120, 60, 'Settings', color=(128, 128, 128))
    running = True#Здесь устанавливается значение переменной running в True, что указывает на то, что игра находится в активном состоянии.
    reset_game()#Эта функция вызывается для сброса игры к начальному состоянию.
    pygame.mixer.music.play(-1) #Воспроизводить музыку бесконечно. Если хотите воспроизвести музыку один раз, поставьте 0 или просто вызовите функцию без аргументов.
    while running:#Это начало цикла, который будет выполняться, пока значение переменной running равно True.
        screen.blit(menu_background, (0, 0))#Эта строка отображает изображение "menu_background" на экране, создавая фон для главного меню.
        draw_text("SPACE", 82, screen_width // 2, screen_height // 4)#Отображение текста при помощи функции draw_text
        draw_text("INVADERS", 44, screen_width // 2, 210)#Тоже самое
        draw_text("Ver: 1.1.1", 15, 45, 590)#Тоже самое
        mouse_pos = pygame.mouse.get_pos()#Эта строка получает текущие координаты курсора мыши на экране и сохраняет их в переменной mouse_pos.
        start_button.check_mouseover(mouse_pos)
        setting_button.check_mouseover(mouse_pos)
        quit_button.check_mouseover(mouse_pos)#Здесь вызываются методы check_mouseover для кнопок "Start" и "Quit" с передачей текущих координат курсора мыши. Эти методы определяют, выделена ли кнопка курсором мыши, и устанавливают соответствующее значение is_highlighted.
        for event in pygame.event.get():#Обработка событий
            if event.type == pygame.MOUSEBUTTONDOWN:#Это условие проверяет, если происходит событие нажатия кнопки мыши.
                if event.button == 1:#Это условие проверяет, если нажата левая кнопка мыши (код 1), то выполняются следующие действия.
                    if start_button.is_highlighted:#Это условие проверяет, если кнопка "Start" выделена курсором, то возвращается True, что означает начало игры.
                        pygame.mixer.music.stop()  # Остановить музыку, когда вы выходите из меню
                        return True  # Начинаем игру
                    if setting_button.is_highlighted:
                        settings_menu()#Вызываем меню настроек по нажатию одноименной клавиши
                    if quit_button.is_highlighted:# Если кнопка "Quit" выделена, то возвращается False, и игра завершается.
                        pygame.quit()# Завершаем Pygame
                        sys.exit()
                        return False
            if event.type == pygame.QUIT:  # Событие сгенерированно при нажатии "крестика"
                running = False  # Перестаем обрабатывать события
                pygame.quit()  # Завершаем Pygame
                sys.exit()


        start_button.draw(screen)
        setting_button.draw(screen)
        quit_button.draw(screen)#Здесь кнопки "Start" и "Quit" отображаются на экране с учетом их текущего состояния (выделена или нет).
        pygame.display.update()#Этот код обновляет экран, чтобы отобразить все изменения, сделанные в текущем кадре.
        clock.tick(60)#Здесь ограничивается частота обновления экрана до 60 кадров в секунду, чтобы сделать игру более плавной и наглядной.


def reset_game():
    global level, score, level_index, all_sprites, enemies, bullets, player

    # Удаление всех игровых объектов
    for sprite in all_sprites:
        sprite.kill()

    # Сброс игровых переменных и счетчиков
    score = 0
    level_index = 0
    level = 1

    # Пересоздание групп спрайтов
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Пересоздание игрока
    player = Player()
    all_sprites.add(player)

    # Создание врагов для первого уровня
    create_enemies()

#Фуекция создания экрана победы
def win_screen():
    win = True
    menu_button = Button(screen_width // 2 - 50, screen_height // 2 + 50, 100, 50, 'Menu', color=(128, 128, 128))#Добавление кнопки меню

    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_button.is_highlighted:
                        win = False
                        main_menu()
                        reset_game()

        mouse_pos = pygame.mouse.get_pos()
        menu_button.check_mouseover(mouse_pos)

        # В этом месте мы ставим изображение на задний план
        screen.blit(img_win, (0, 0))

        draw_text("You win!", 64, screen_width // 2, screen_height // 4)
        draw_text("Your score: " + str(score), 32, screen_width // 2, screen_height // 3)
        draw_text("Press the menu button to return to the main menu.", 22, screen_width // 2, screen_height // 2)

        menu_button.draw(screen)
        pygame.display.update()#Этот код обновляет экран, чтобы отобразить все изменения, сделанные в текущем кадре.



# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):#Это метод-конструктор класса Player, который вызывается при создании объекта этого класса.
        super().__init__()#Этот вызов конструктора родительского класса pygame.sprite.Sprite. Он инициализирует объект Player как спрайт.
        self.image = pygame.transform.scale(player_img, (64, 64))#Здесь устанавливается изображение игрока. player_img - это изображение игрока, которое масштабируется до размера 64x64 пикселя с помощью pygame.transform.scale, и результат сохраняется в self.image
        self.rect = self.image.get_rect()#Создается прямоугольник self.rect, который ограничивает изображение игрока
        self.rect.x = screen_width // 2 - 32#Устанавливает начальное положение игрока по горизонтали в центре экрана.
        self.rect.y = screen_height - 100#Устанавливает начальное положение игрока по вертикали, 100 пикселей выше нижней границы экрана.
        self.speed_x = 0#Устанавливает начальную горизонтальную скорость игрока на ноль, что означает, что игрок в начале не двигается.
        self.shoot_delay = 600  # Задержка между выстрелами игрока в миллисекундах. В данном случае, это 600 миллисекунд, или 0.6 секунды.
        self.last_shot = pygame.time.get_ticks()#Эта строка устанавливает self.last_shot в текущее время в миллисекундах с помощью pygame.time.get_ticks(). Эта переменная будет использоваться для определения, когда можно сделать следующий выстрел.
        self.shooting = False#Изначально устанавливается значение False для переменной shooting, что означает, что игрок не стреляет.
        self.lives = 3#Добавление жизней (экспериментально)

    def update(self):#Этот метод вызывается каждый кадр игры и обновляет состояние игрока.
        self.rect.x += self.speed_x#Обновляет положение игрока по горизонтали на основе его скорости speed_x.
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen_width - 64:
            self.rect.x = screen_width - 64#Проверяют, не выходит ли игрок за границы экрана. Если да, то его положение ограничивается, чтобы он не мог уйти за пределы экрана.
        self.shoot()#Вызывает метод shoot(), который обрабатывает выстрел игрока.

    def shoot(self):#Этот метод отвечает за создание пуль игрока и добавление их в группы спрайтов all_sprites и player_bullets.
        if self.shooting:# Проверяет, активно ли стрельба игрока (переменная shooting равна True).
            now = pygame.time.get_ticks()#Получает текущее время в миллисекундах.
            if now - self.last_shot > self.shoot_delay:#Проверяет, прошло ли достаточно времени с момента последнего выстрела. Если да, то создается объект bullet (пуля) и добавляется в группы спрайтов all_sprites и player_bullets.
                self.last_shot = now
                bullet = Bullet(self.rect.x + 27, self.rect.y - 32, 1)#Здесь создается новый объект пули (bullet).
                all_sprites.add(bullet)# Эта строка добавляет созданный объект bullet в группу спрайтов all_sprites
                player_bullets.add(bullet)# Эта строка добавляет ту же пулю (bullet) в отдельную группу player_bullets.
                shoot_sound.play()

# Класс для врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, shooting=False):#Это конструктор класса Enemy. Он принимает один аргумент shooting, который по умолчанию равен False, но может быть установлен в True, чтобы создать врага, способного стрелять.
        super().__init__()
        if shooting:
            self.image = pygame.transform.scale(enemy_shot, (32, 32))
        else:
            self.image = pygame.transform.scale(enemy_img, (32, 32))#В зависимости от значения shooting, загружается изображение врага (снарядящегося или нет) и устанавливается соответствующий размер для изображения.
        self.rect = self.image.get_rect()#Здесь создается прямоугольник, который охватывает изображение врага. Этот прямоугольник будет использоваться для обнаружения столкновений и расположения врага на экране.
        self.shooting = shooting
        intersect = True
        #Затем идет блок кода, который гарантирует, что начальное положение врага не пересекается с другими врагами в группе enemies. Враги размещаются случайным образом, и проверяется их начальное расположение на пересечение с другими врагами. Если есть пересечение, то начальные координаты перегенерируются до тех пор, пока не будет найдено подходящее местоположение.
        while intersect:
            intersect = False
            self.rect.x = random.randint(0, screen_width - 32)
            self.rect.y = random.randint(32, screen_height // 2)
            for enemy in enemies:   # используется переменная enemies
                if self.rect.colliderect(enemy.rect):
                    intersect = True
            self.speed_x = random.randint(6, 6)#Устанавливается начальная горизонтальная скорость врага. Сделанно для избежания пересечения моделей Enemy друг с другом во время пересечения границы x
            self.speed_y = 0#Начальная вертикальная скорость врага устанавливается равной 0.
            self.change_direction = False#Этот атрибут служит для отслеживания изменения направления движения врага.
        if self.shooting:#Это условие проверяет, стреляет ли данный экземпляр класса Enemy. Если self.shooting истинно (True), значит, враг может стрелять, и соответственно, устанавливаются параметры для его стрельбы.
            self.shoot_delay = random.randrange(1000, 3000)#В этой строке устанавливается случайная задержка (в миллисекундах) между выстрелами врага
            self.last_shot = pygame.time.get_ticks()#Здесь записывается текущее время (в миллисекундах) с использованием функции pygame.time.get_ticks().

    def update(self):
        self.rect.x += self.speed_x#Это обновление позиции врага по горизонтали на основе его скорости speed_x. Враг движется вправо или влево, в зависимости от значения speed_x.
        if self.rect.x <= 0 or self.rect.x >= screen_width - 32:#Это условие проверяет, достиг ли враг края экрана по горизонтали. Если враг достиг левого или правого края (меньше или равен 0 или больше или равен screen_width - 32), то меняется направление движения.
            self.speed_x *= -1#Если враг достиг края экрана, то его скорость инвертируется, что означает изменение направления движения на противоположное.
            self.change_direction = True

        if self.change_direction:#Если меняется направление движения
            self.rect.y += 20#Здесь изменяется вертикальная позиция врага, добавляя 20 к текущей позиции. Это означает, что враг будет двигаться вниз.
            self.change_direction = False#После того как вертикальное движение вниз выполнено, флаг self.change_direction устанавливается обратно в False, чтобы при следующем обновлении не выполнять это движение снова.
            if self.rect.y >= 460:#Если вертикальная позиция врага достигает или превышает 460 пикселей, то вызывается функция gameover_screen()
                gameover_screen()
        self.shoot()#Метод отвечающий за стрельбу врага

    def shoot(self):#Этот метод shoot предназначен для реализации стрельбы врагов.
        if self.shooting:# Это условие проверяет, способен ли враг стрелять.
            now = pygame.time.get_ticks()#Здесь записывается текущее время в миллисекундах с использованием pygame.time.get_ticks(). Это нужно для контроля задержки между выстрелами.
            if now - self.last_shot > self.shoot_delay:# Это условие проверяет, прошла ли достаточная задержка с момента последнего выстрела.
                self.last_shot = now#Здесь обновляется время последнего выстрела, чтобы отслеживать задержку до следующего выстрела.
                bullet = Bullet(self.rect.x + 12, self.rect.y + 32, -1)#: Создается объект пули (bullet). Параметры self.rect.x + 12 и self.rect.y + 32 определяют начальную позицию пули на экране. self.rect.x - это текущая горизонтальная позиция врага, и self.rect.y - его вертикальная позиция. Значение -1 передается как аргумент, чтобы указать, что пуля летит вниз (в сторону игрока).
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)#Пуля также добавляется в отдельную группу enemy_bullets, сделанно для того чтобы эта пуля убивала только игрока а врагов просто пролетала насквозь

    def move_down(self):#Эта строка кода изменяет вертикальную позицию врага (self.rect.y) путем добавления значения self.speed_y. self.speed_y представляет собой вертикальную скорость врага, и она может быть положительной или отрицательной
        self.rect.y += self.speed_y
# Класс для пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()#Этот вызов инициализирует базовый класс pygame.sprite.Sprite
        self.image = pygame.transform.scale(bullet_img, (16, 16))#Эта строка кода устанавливает изображение пули и масштабирует его до размера 16x16 пикселей.
        self.rect = self.image.get_rect()#Создается объект прямоугольника, который охватывает изображение пули.
        self.rect.x = x
        self.rect.y = y#Эти строки кода устанавливают начальные координаты пули в соответствии с переданными значениями x и y
        self.speed_y = -7 * direction#Здесь устанавливается вертикальная скорость пули. Скорость self.speed_y умножается на direction, что определяет направление движения пули (вверх или вниз).

    def update(self):#Этот метод вызывается на каждом кадре игры для обновления состояния пули.
        self.rect.y += self.speed_y#Эта строка кода обновляет вертикальную позицию пули, двигая ее вверх или вниз, в зависимости от значения self.speed_y.
        if self.rect.y < -16 or self.rect.y > screen_height:#Это условие проверяет, находится ли пуля за пределами экрана сверху или снизу. Если это так, то пуля удаляется из группы спрайтов, в которой она находится, с помощью метода self.kill().
            self.kill()

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):#Это конструктор класса. Он вызывается при создании нового объекта типа BossBullet и принимает три параметра: x, y и angle. x и y - это начальные координаты пули, а angle определяет угол, под которым пуля движется.
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (16, 16))#Эта строка кода устанавливает изображение пули и масштабирует его до размера 16x16 пикселей.
        self.rect = self.image.get_rect()#Создается объект прямоугольника, который охватывает изображение пули.
        self.rect.x = x
        self.rect.y = y#Эти строки кода устанавливают начальные координаты пули в соответствии с переданными значениями x и y.
        self.speed = 5#Здесь устанавливается скорость пули. Пуля будет двигаться в соответствии с этой скоростью в направлении, заданном углом self.angle.
        self.angle = angle#: Угол, под которым пуля движется.

    def update(self):#Этот метод вызывается на каждом кадре игры для обновления состояния пули.
        self.rect.x += self.speed * math.sin(math.radians(self.angle))
        self.rect.y += self.speed * math.cos(math.radians(self.angle))#десь обновляются координаты пули в соответствии с текущим углом движения. Эти строки кода используют тригонометрические функции sin и cos, чтобы определить, как пуля двигается вдоль горизонтальной и вертикальной осей.
        if self.rect.y < -16 or self.rect.y > screen_height:#: Это условие проверяет, находится ли пуля за пределами экрана сверху или снизу. Если это так, то пуля удаляется из группы спрайтов, в которой она находится, с помощью метода self.kill().
            self.kill()


class Vide(pygame.sprite.Sprite):#Класс для одной из атак босса
    def __init__(self, x, y):
        super().__init__()#Этот вызов инициализирует базовый класс
        self.image = pygame.transform.scale(enemy_shot, (16, 16))  #Эта строка кода устанавливает изображение волны и масштабирует его до размера 16x16 пикселей.
        self.rect = self.image.get_rect()#Создается объект прямоугольника, который охватывает изображение волны.
        self.rect.x = x
        self.rect.y = y#Эти строки кода устанавливают начальные координаты миссили в соответствии с переданными значениями x и y
        self.speed_y = 3#Здесь устанавливается вертикальная скорость миссили.

    def update(self):#Этот метод вызывается на каждом кадре игры для обновления состояния волны.
        self.rect.y += self.speed_y#Здесь обновляются координаты волны вниз по экрану на расстояние, заданное self.speed_y.
        if self.rect.y > screen_height:#Это условие проверяет, находится ли волна ниже нижней границы экрана. Если это так, то волна удаляется из группы спрайтов, в которой она находится, с помощью метода self.kill()
            self.kill()

# Класс для босса
class Boss(pygame.sprite.Sprite):
    def __init__(self):#Это конструктор класса. Он вызывается при создании нового объекта типа Boss.
        super().__init__()
        self.shots_fired = 0
        self.hits_taken = 0#Эти переменные отслеживают количество выпущенных выстрелов и количество полученных попаданий босса. Они инициализируются нулем.
        self.image = pygame.transform.scale(boss_img, (128, 128))# Эта строка кода устанавливает изображение босса и масштабирует его до размера 128x128 пикселей.
        self.rect = self.image.get_rect()#Создается объект прямоугольника, который охватывает изображение босса.
        self.rect.x = screen_width // 2 - 64#Здесь устанавливаются начальные координаты босса.
        self.rect.y = -128
        self.speed_y = 1#Это вертикальная скорость босса. Значение 1 означает, что босс будет двигаться вниз на 1 пиксель за кадр.
        self.shoot_delay = random.randrange(2200, 2500)#Эта переменная устанавливает случайную задержку перед следующим выстрелом босса
        self.last_shot = pygame.time.get_ticks()# Это метка времени (в миллисекундах), которая представляет время последнего выстрела босса
        self.invulnerability_toggle_time = pygame.time.get_ticks()#Это метка времени, которая отслеживает, когда последний раз был включен/выключен режим "неуязвимости" для босса.
        self.invulnerable = False# Это логическая переменная, которая указывает, находится ли босс в режиме "неуязвимости" (True) или нет (False).

    def update(self):
        if pygame.time.get_ticks() > self.invulnerability_toggle_time:#Эта строка проверяет, прошло ли определенное количество времени с момента последнего переключения режима "неуязвимости" босса.
            self.invulnerable = not self.invulnerable#Если прошло достаточно времени, режим "неуязвимости" переключается между включенным и выключенным (при помощи оператора not).
            self.invulnerability_toggle_time = pygame.time.get_ticks() + 5000#Здесь обновляется метка времени для следующего переключения "неуязвимости". В данном случае, она устанавливается на текущее время плюс 5000 миллисекунд (5 секунд).
        if self.invulnerable:#Эта строка проверяет, включен ли режим "неуязвимости" для босса. Если это так, то используется изображение boss_inv
            self.image = pygame.transform.scale(boss_inv,(128, 128))
        else:
            self.image = pygame.transform.scale(boss_img, (128, 128))
        self.rect.y += self.speed_y#Здесь обновляется вертикальная позиция босса, перемещая его вниз на величину, указанную в self.speed_y.
        if self.rect.y >= 0:#Это условие проверяет, достиг ли босс верхней границы экрана (его rect.y больше или равно нулю).
            self.speed_y = 0#Если босс достиг верхней границы экрана, его вертикальная скорость устанавливается в 0, что останавливает движение вниз.
            if random.choice([True, False]):#Эта строка выбирает случайным образом, следует ли вызывать метод self.boss_shoot() (выстрел босса) или метод self.boss_vibe_attack()
                self.boss_shoot()
            else:
                self.boss_vibe_attack()
        self.rect.y = 0#Здесь босс вручную перемещается вверх, в случае если его вертикальная позиция была установлена выше нуля.

    def boss_shoot(self):
        now = pygame.time.get_ticks()#Создается переменная now, которая получает текущее время в миллисекундах с использованием pygame.time.get_ticks().
        if now - self.last_shot > self.shoot_delay:#Здесь проверяется, прошло ли достаточное количество времени с момента последнего выстрела босса. Это осуществляется сравнением текущего времени now с временем последнего выстрела self.last_shot, и сравнением с self.shoot_delay - задержкой между выстрелами.
            self.last_shot = now#Время последнего выстрела обновляется на текущее время, чтобы начать подсчет времени для следующего выстрела.
            bullet_angles = [-45, -20, 0, 20, 45]#Здесь определены углы под которыми будут выпущены пули.
            for angle in bullet_angles:
                bullet = BossBullet(self.rect.centerx, self.rect.bottom, angle)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)#Далее, в цикле for angle in bullet_angles:, создаются пули с разными углами, и каждая из них добавляется как экземпляр класса BossBullet в группы all_sprites и enemy_bullets.
    def boss_vibe_attack(self):
        now = pygame.time.get_ticks()#Создается переменная now, которая получает текущее время в миллисекундах с использованием pygame.time.get_ticks().
        if now - self.last_shot > self.shoot_delay:#Здесь проверяется, прошло ли достаточное количество времени с момента последней атаки босса. Это осуществляется сравнением текущего времени now с временем последней атаки self.last_shot, и сравнением с self.shoot_delay - задержкой между атаками.
            self.last_shot = now#Время последней атаки обновляется на текущее время, чтобы начать подсчет времени для следующей атаки.
            self.shots_fired += 1#Увеличивается счетчик выстрелов self.shots_fired на 1.
            min_hole_x = 150  #Минимальное расстояние от "дырки" до левого края экрана
            max_hole_x = screen_width - 150  #Максимальное расстояние от "дырки" до правого края экрана
            hole_width = 100  # Замените на желаемую ширину "дырки"

            # Генерируем случайные координаты для "дырки"
            hole_x = random.randint(min_hole_x, max_hole_x)

            for x in range(0, screen_width, 32):
                # Проверяем, попадает ли текущая координата в "дырку"
                if hole_x <= x <= hole_x + hole_width:
                    continue  # Пропускаем создание пули в "дырке"
                vibe = Vide(x, self.rect.bottom)
                all_sprites.add(vibe)
                enemy_bullets.add(vibe)

# Класс для врагов со броней (умирают после двух попаданий)
class ArmoredEnemy(Enemy):
    def __init__(self, shooting=False):
        super().__init__(shooting)
        self.hits_taken = 0#Счётчик попаданий по врагу
        self.image = pygame.transform.scale(enemy_armor, (32, 32))  #Изображение врага с бронёй

    def get_hit(self):#Этот метод вызывается, когда объект ArmoredEnemy получает попадание.
        self.hits_taken += 1#Он увеличивает счетчик попаданий self.hits_taken на 1.
        if self.hits_taken >= 2:#Здесь проверяется, получил ли враг два или более попаданий. Если это так, то вызывается метод kill(), который удаляет объект из всех соответствующих групп спрайтов и, таким образом, удаляет врага из игры.
            self.kill()
            invade_kill.play()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)

# Уровни игры
levels = [
    [1, 0, 0],  # Уровень 1: 5 врагов, 2 пули
    [1, 1, 0],  # Уровень 2: 7 врагов, 3 пули
    [1, 1, 1]  # Уровень 3: 10 врагов, 4 пули
]


# Текущий уровень
level_index = 0#Это переменная, которая указывает на текущий уровень.

# Создание врагов для текущего уровня
def create_enemies():#Эта функция создает врагов для текущего уровня. Сначала она получает текущий уровень из списка levels с использованием level_index. Затем она создает врагов в соответствии с данными уровня.
    global level_index
    current_level = levels[level_index]#В зависимости от индекса в списке уровня добавляются разные враги
    for _ in range(current_level[0]):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    for _ in range(current_level[1]):
        enemy = Enemy(shooting=True)
        enemy.image = pygame.transform.scale(enemy_shot, (32, 32))
        all_sprites.add(enemy)
        enemies.add(enemy)
    for _ in range(current_level[2]):
        armored_enemy = ArmoredEnemy()#создаем экземпляр ArmoredEnemy
        all_sprites.add(armored_enemy)
        enemies.add(armored_enemy)

# Создание босса
def create_boss():#Это функция, которая создает и добавляет босса (Boss) в группу спрайтов all_sprites и в группу врагов enemies.
    boss = Boss()
    all_sprites.add(boss)
    enemies.add(boss)

# Создание врагов для первого уровня
create_enemies()

# Пауза
resume_button = Button(350, 270, 120, 60, 'Resume', color=(128, 128, 128))
menu_button = Button(350, 350, 120, 60, 'Menu', color=(128, 128, 128))
def pause_game():
    paused = True#Создается локальная переменная paused и устанавливается в значение True, что означает, что игра находится в режиме паузы.
    pause_sound.play()
    while paused:#Начинается цикл while, который продолжает выполняться, пока переменная paused остается истинной (True)
        for event in pygame.event.get():#Запускается цикл, который перебирает все события Pygame, которые произошли с момента последней проверки.
            if event.type == pygame.QUIT:#Проверяется, является ли текущее событие событием выхода из игры (например, закрытие окна).
                running = False
                pygame.quit()#Завершается работа библиотеки Pygame.
                sys.exit()#Завершается выполнение программы.
            elif event.type == pygame.MOUSEBUTTONDOWN:#Если текущее событие - это событие нажатия мыши.
                if event.button == 1:#Проверяется, была ли нажата левая кнопка мыши (1 - это код для левой кнопки).
                    if resume_button.is_highlighted:#Проверяется, была ли нажата кнопка возобновления игры. Если условие выполняется, переменная paused устанавливается в False, что позволяет продолжить игру.
                        paused = False
                    if menu_button.is_highlighted:#Проверяется, была ли нажата кнопка перехода в главное меню. Если условие выполняется, переменная paused устанавливается в False, и вызывается функция main_menu(), а затем reset_game().
                        paused = False
                        main_menu()
                        reset_game()

        mouse_pos = pygame.mouse.get_pos()#олучается текущее положение курсора мыши.
        resume_button.check_mouseover(mouse_pos)#Проверяется, находится ли курсор мыши над кнопкой возобновления игры.
        menu_button.check_mouseover(mouse_pos)#Проверяется, находится ли курсор мыши над кнопкой перехода в главное меню.

        screen.blit(bg_img, (0, 0))#На экран (вероятно, это поверхность Pygame) наносится изображение фона bg_img в координатах (0, 0).
        draw_text("Game Paused", 64, screen_width / 2, 200)#Рисуется текст "Game Paused" с размером шрифта 64 и позицией по центру экрана по вертикали и на высоте 200 пикселей.

        resume_button.draw(screen)#Рисуется кнопка возобновления игры на экране.
        menu_button.draw(screen)#Рисуется кнопка перехода в главное меню на экране.

        pygame.display.flip()#Обновляется содержимое экрана.
        clock.tick(15)#Ограничивается частота обновления экрана до 15 кадров в секунду, чтобы управлять производительностью игры.

# Основной игровой цикл
clock = pygame.time.Clock()#Создается экземпляр объекта Clock из модуля pygame.time. Этот объект используется для контроля частоты обновления экрана и поддержания заданного FPS
score = 0#Создается переменная score, которая будет использоваться для отслеживания счета игрока.
level = 1#Создается переменная level, которая будет использоваться для отслеживания текущего уровня игры.
running = main_menu()#Вызывается функция main_menu(), которая отображает главное меню игры и возвращает булево значение True, если игра должна быть запущена, и False, если игра должна быть завершена. Переменная running принимает это значение.
while running:#Это начало главного цикла игры. Цикл будет выполняться, пока running имеет значение True, то есть пока игра должна продолжаться.
    for event in pygame.event.get():#Здесь начинается обработка событий Pygame. Этот блок цикла будет выполняться для каждого события в очереди событий.
        if event.type == pygame.QUIT:#Этот блок проверяет, если произошло событие завершения игры (например, нажатие на "крестик" в окне), то переменная running устанавливается в False, что приведет к завершению игры.
            running = False
        elif event.type == pygame.KEYDOWN:#Если событие является нажатием клавиши на клавиатуре, то происходит обработка клавиш.
            if event.key == pygame.K_LEFT:#Если нажата клавиша "влево" (pygame.K_LEFT), то установка скорости игрока влево.
                player.speed_x = -6
            elif event.key == pygame.K_RIGHT:#Если нажата клавиша "вправо" (pygame.K_RIGHT), то установка скорости игрока вправо.
                player.speed_x = 6
            elif event.key == pygame.K_SPACE:#Если нажата клавиша "пробел" (pygame.K_SPACE), то устанавливается флаг player.shooting в True, что указывает на начало стрельбы игрока, и вызывается метод player.shoot(), чтобы игрок выпустил пулю.
                player.shooting = True
                player.shoot()
            elif event.key == pygame.K_ESCAPE:  # Проверка нажатия клавиши "p" для паузы
                pause_game()
        elif event.type == pygame.KEYUP:#Если событие является отпусканием клавиши на клавиатуре, то происходит обработка отпускания клавиш.
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:#Если отпущена клавиша "влево" или "вправо", то скорость игрока сбрасывается до 0, останавливая движение игрока влево или вправо.
                player.speed_x = 0
            if event.key == pygame.K_SPACE:
                player.shooting = False#Если отпущена клавиша "пробел", то флаг player.shooting устанавливается в False, что останавливает стрельбу игрока.

    all_sprites.update()#Вызывается метод update() для всех спрайтов в группе all_sprites. Это обновляет позиции и состояния всех спрайтов в игре.
    for enemy in enemies:#В цикле перебираются все враги, находящиеся в группе enemies.
        if enemy.rect.y >= screen_height - enemy.rect.height:# Проверяется, достиг ли враг нижней границы экрана. Если враг достиг, выводится сообщение о проигрыше, и переменная running устанавливается в False, что завершает игру.
            print("Проигрыш. Враг достигнил границы с кораблем.")
            running = False

    # Проверка столкновений игрока с врагами
        hits = pygame.sprite.spritecollide(player, enemy_bullets, False)#Проверяется столкновение игрока с пулями врагов. Если столкновение произошло, вызывается функция gameover_screen(), и все пули врагов, которые столкнулись с игроком (enemy_bullets), не уничтожаются (параметр False).
        if hits:
            player.lives -= 1#Если враг попадает, отнимается 1 жизнь. Всего их 3
            if player.lives <= 0:#Если жизней 0 наступает gameover
                player_kill.play()
                gameover_screen()
            for enemy in hits:#hits здесь является списком всех врагов, которые столкнулись со спрайтом игрока.
                enemy.kill()#Метод kill() удаляет врага из всех групп спрайтов, в которые он был добавлен (например, all_sprites, enemies и т.д.), эффективно "уничтожая" врага в контексте игры. Это не удаляет объект из памяти, но он больше не будет обрабатываться в главном цикле игры и не будет отображаться на экране.

    # Проверка столкновений пуль с врагами
    for bullet in player_bullets:#Далее выполняется проверка столкновений пуль игрока с врагами
        enemy_hits = pygame.sprite.spritecollide(bullet, enemies, False)
        if enemy_hits:#Проверяется столкновение пули игрока с врагами.
            bullet.kill()#Пуля игрока уничтожается.
            for enemy in enemy_hits:
                if isinstance(enemy, Boss):#Проверяется, является ли враг объектом класса Boss. Если да, то выполняется следующее:
                    if not enemy.invulnerable:#Проверяется, что босс не находится в режиме "неуязвимости".
                        score += 50#Игроку начисляются 50 очков за попадание в босса.
                        enemy.hits_taken += 1#Увеличивается счетчик попаданий в босса.
                        if enemy.hits_taken >= 2:#Проверяется, достиг ли счетчик попаданий в босса значения 1
                            enemy.kill()#Если да, то босс уничтожается.
                            win_screen()#Запускается экран победы.
                elif isinstance(enemy, ArmoredEnemy):#Если враг является экземпляром класса ArmoredEnemy, то выполняется следующее:
                    score += 10#Игроку начисляются 10 очков за попадание в бронированного врага.
                    enemy.get_hit()#Вызывается метод get_hit() у объекта enemy, чтобы учесть попадание в бронированного врага. Если этот враг получает достаточно попаданий, он будет уничтожен.
                else:#Если враг не является ни боссом, ни бронированным врагом, то выполняется следующее:
                    score += 10#Игроку начисляются 10 очков за попадание в обычного врага.
                    enemy.kill()#Враг уничтожается.
                    invade_kill.play()


# Переход на следующий уровень
    if len(enemies) == 0:#Проверяется, если количество врагов (enemies) становится равным нулю. Это означает, что игрок уничтожил всех врагов на текущем уровне.
        level_index += 1#Если это условие выполняется, level_index увеличивается на 1, что переводит игру на следующий уровень.
        level += 1#Текущий уровень (level) также увеличивается на 1.
        if level_index >= len(levels):#Это условное выражение проверяет, достигнут ли текущий уровень (level_index) конца списка уровней (levels). Если это условие выполняется, то значит игра достигла уровня, где должен появиться босс.
            create_boss()
        else:
            create_enemies()

    screen.blit(bg_img, (0, 0))#Эта строка рисует задний фон на игровом экране, начиная с координат (0, 0), что позволяет обновить фон перед отрисовкой остальных спрайтов.
    all_sprites.draw(screen)#Здесь все спрайты из группы all_sprites отрисовываются на игровом экране.

    # Отображение счета

    font = pygame.font.Font(None, 36)#Создается объект шрифта с размером 36 (отсутствие аргумента None означает использование шрифта по умолчанию).
    lives_text = font.render("Lives: " + str(player.lives), True, white)#Создается текстовый объект с текстом "Lives: " и текущим значением счета.
    screen.blit(lives_text, (20, 60))#Жизни отображаются на экране, начиная с координат (20, 60).
    score_text = font.render("Score: " + str(score), True, white)#Создается текстовый объект с текстом "Score: " и текущим значением счета. Флаг True
    level_text = font.render("Level: " + str(level), True, white)#Аналогично создается текстовый объект для отображения текущего уровня.
    screen.blit(score_text, (20, 20))#Счет отображается на экране, начиная с координат (20, 20).
    screen.blit(level_text, (screen_width - 150, 20))#Уровень отображается на экране в верхнем правом углу

    pygame.display.flip()#Этой строкой обновляется игровой экран, чтобы отобразить все отрисованные спрайты и текст.
    clock.tick(60)#Эта строка ограничивает количество кадров в секунду (FPS) игры до 60, что обычно делается для стабильности и предсказуемости производительности.
pygame.quit()# Когда игровой цикл завершается (когда running становится False), вызывается pygame.quit() для корректного завершения работы Pygame и закрытия окна игры.