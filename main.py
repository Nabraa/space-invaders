import pygame
import random

pygame.init()

screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
pygame.display.set_caption(' Space Invaders ')

pygame.mixer.init()
sound = pygame.mixer.Sound('data/intro.ogg')
sound.play()
while pygame.mixer.get_busy():
    pygame.time.delay(100)

bullet_cooldown = 30  # The time (in ticks) to wait between firing bullets
bullet_cooldown_timer = 0

# załaduj obrazek statku
statek = pygame.image.load('data/orzel7.png')

pociski = 0
ilosc = 5
punkty = 0
runda = 1
v_kosmitow = 5
granica = 20

kosmita = []
k_pos = []
pocisk = []
p_pos = []
boo = []

running = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 130)

font = pygame.font.Font(pygame.font.get_default_font(), 20)
font2 = pygame.font.Font(pygame.font.get_default_font(), 40)

zwyciestwo = False
przegrana = False
intro = True
grafika = True

while intro:
    sound = pygame.mixer.Sound('data/muzyka.ogg')
    sound.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            intro = False
            grafika = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            intro = False

    screen.fill("darkblue")
    tekst3 = font.render("Wciśnij ENTER, żeby rozpocząć", True, (255, 255, 0))
    screen.blit(tekst3, (150, 200))

    pygame.display.flip()
    clock.tick(60)

while grafika:

    screen.fill("darkblue")
    tekst3 = font.render("Wybierz grafike pocisku", True, (255, 255, 0))
    screen.blit(tekst3, (200, 100))

    tekst5 = font.render("1", True, (255, 255, 0))
    screen.blit(tekst5, (100, 300))
    screen.blit(pygame.image.load('data/pocisk.png'), (100, 200))

    tekst6 = font.render("2", True, (255, 255, 0))
    screen.blit(tekst6, (300, 300))
    screen.blit(pygame.image.load('data/pocisk2.png'), (300, 200))

    tekst7 = font.render("3", True, (255, 255, 0))
    screen.blit(tekst7, (500, 300))
    screen.blit(pygame.image.load('data/pocisk3.png'), (475, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            grafika = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            pociskg = pygame.image.load('data/pocisk.png')
            grafika = False
        if keys[pygame.K_2]:
            pociskg = pygame.image.load('data/pocisk2.png')
            grafika = False
        if keys[pygame.K_3]:
            pociskg = pygame.image.load('data/pocisk3.png')
            grafika = False
    pygame.display.flip()
    clock.tick(60)

while running:
    screen.fill("darkblue")
    screen.blit(statek, (player_pos.x, player_pos.y))

    tekst = font.render(("Punkty: " + str(punkty)), True, (255, 255, 0))
    screen.blit(tekst, (0, 0))
    tekst4 = font.render(("Runda: " + str(runda)), True, (255, 255, 0))
    screen.blit(tekst4, (0, 25))

    if punkty == granica:
        runda += 1
        v_kosmitow += 3
        punkty = 0
        granica += 5

    if runda >= 5 and not zwyciestwo:
        zwyciestwo = True
        czas_zwyciestwa = pygame.time.get_ticks()

    if zwyciestwo:
        czas_teraz = pygame.time.get_ticks()
        if czas_teraz - czas_zwyciestwa < 5000:

            tekst2 = font2.render("Zwycięstwo!", True, (255, 255, 0))
            screen.blit(tekst2, (200, 100))
        else:
            running = False

    if len(kosmita) < 5:
        for i in range(0, ilosc):
            kosmita.append(pygame.image.load('data/kurvinox.png'))
            k_pos.append(pygame.Vector2(random.randint(0, 550), random.randint(0, 100)))
            boo.append(True)

    for i in range(0, ilosc):  # kolizja pocisku z kosmita
        for j in range(0, len(pocisk)):
            if p_pos[j].x + 20 > k_pos[i].x and p_pos[j].x < k_pos[i].x + 80 and p_pos[j].y + 20 > k_pos[i].y and p_pos[
                j].y < k_pos[i].y + 80:
                k_pos[i] = pygame.Vector2(random.randint(0, 550), random.randint(0, 100))
                boo[i] = True
                punkty += 1
                p_pos[j] *= (-1)
                break

        if i >= len(kosmita) or i >= len(k_pos):
            print(f"Index {i} out of range.")
        else:
            screen.blit(kosmita[i], (k_pos[i].x, k_pos[i].y))

    for i in range(ilosc):  # kolizja z graczem
        if player_pos.x + 80 > k_pos[i].x and player_pos.x < k_pos[i].x + 80 and player_pos.y + 30 > k_pos[
            i].y and player_pos.y < k_pos[i].y + 30:
            przegrana = True
            czas_przegranej = pygame.time.get_ticks()
            break

    if przegrana:
        czas_teraz = pygame.time.get_ticks()
        if czas_teraz - czas_przegranej < 5000:
            tekst2 = font.render("Przegrana!", True, (255, 0, 0))
            screen.blit(tekst2, (200, 100))
        else:
            running = False

    if player_pos.x < 0:
        player_pos.x = 1
    elif player_pos.x > 550:
        player_pos.x = 549

    for i in range(0, ilosc):
        if k_pos[i].x <= 0:
            k_pos[i].y += 10
            k_pos[i].x = 20
            boo[i] = True
        elif k_pos[i].x >= 550:
            k_pos[i].y += 10
            k_pos[i].x = 530
            boo[i] = False

        if boo[i] == True:
            k_pos[i].x += v_kosmitow
        elif boo[i] == False:
            k_pos[i].x -= v_kosmitow

    for event in pygame.event.get():
        # zdarzenie zamknięcia programu
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos.x -= 10
        if keys[pygame.K_d]:
            player_pos.x += 10
        if keys[pygame.K_SPACE] and bullet_cooldown_timer <= 0:
            pocisk.insert(pociski, pociskg)
            screen.blit(pocisk[pociski], (player_pos.x, player_pos.y))
            p_pos.append(pygame.Vector2(player_pos.x + 50, player_pos.y))
            pociski += 1
            bullet_cooldown_timer = bullet_cooldown

    i = 0
    while i <= len(pocisk) - 1:
        screen.blit(pocisk[i], (p_pos[i].x, p_pos[i].y))
        p_pos[i].y -= 2
        i += 1

    if bullet_cooldown_timer > 0:
        bullet_cooldown_timer -= 1

    pygame.display.flip()
    clock.tick(60)

# zamknięcie programu
pygame.quit()