    import pygame, sys
    from pygame.locals import *
    import random, time
    
    pygame.init()
    
    FPS = 60
    FramePerSec = pygame.time.Clock()
    
    blue  = (0, 0, 255)
    red  = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    width = 400
    height = 600
    speed= 5
    score = 0

    N = 10 
    coins_collected = 0

    font = pygame.font.SysFont("Roboto", 60)
    font_small = pygame.font.SysFont("Roboto", 20)
    game_over = font.render("Your life is Over!", True, black)
    
    background = pygame.image.load("fon.png")

    DISPLAYSURF = pygame.display.set_mode((400,600))
    DISPLAYSURF.fill(white)
    pygame.display.set_caption("Game by Mukataev Alibek07")

    pygame.mixer.music.load("background.mp3") 
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(0.5)
    
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            self.image = pygame.image.load("zlodei.png")
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(40, width-40), 0)  
    
        def move(self):
            global score
            self.rect.move_ip(0,speed)
            if (self.rect.top > 600):
                score += 1
                self.rect.top = 0
                self.rect.center = (random.randint(40, width - 40), 0)
    
    
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            self.image = pygame.image.load("p1.png")
            self.rect = self.image.get_rect()
            self.rect.center = (160, 520)
            
        def move(self):
            pressed_keys = pygame.key.get_pressed()
            
            if self.rect.left > 0:
                if pressed_keys[K_LEFT]:
                    self.rect.move_ip(-5, 0)
            if self.rect.right < width:        
                if pressed_keys[K_RIGHT]:
                    self.rect.move_ip(5, 0)

    #КЛАСС ДЛЯ ДОБАВЛЕНИЯ В НЕЁ КОИНОВ 
    class Coin(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            rand_val = random.randint(1, 10)
            
            if rand_val > 8: 
                self.image = pygame.image.load("coin2.png")
                self.weight = 5 
            else:
                self.image = pygame.image.load("coin_orig.png") 
                self.weight = 1 

            self.image = pygame.transform.scale(self.image, (40, 40))
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(40, width - 40), 0)

        def move(self):
            self.rect.move_ip(0, speed)
            if (self.rect.top > 600):
                self.kill()
                            
    P1 = Player()
    E1 = Enemy()

    coins = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)
    SPAWN_COIN = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_COIN, 2000)
    coin_count = 0
    
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)

    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)
    
    while True:
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                speed += 0.5     
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SPAWN_COIN:
                new_coin = Coin()
                coins.add(new_coin)
                all_sprites.add(new_coin)

    
        DISPLAYSURF.blit(background, (0,0))
        scores = font_small.render(str(score), True, black)
        DISPLAYSURF.blit(scores, (10,10))

        scores = font_small.render(f"Score: {score}", True, black)
        DISPLAYSURF.blit(scores, (2,2))

        coins_text = font_small.render(f"Coins: {coin_count}", True, black) #ВЫВОДИТ НАДПИСЬ ОТДЕЛЬНО В СТОРОНЕ
        DISPLAYSURF.blit(coins_text, (300, 10))

        coin_collisions = pygame.sprite.spritecollide(P1, coins, True)
        for coin in coin_collisions:
            coin_count += 1 
            score += 5
            score += coin.weight 
            coins_collected += coin.weight # Счетчик для ускорения
        
        if coins_collected >= N: 
            speed += 1 
            coins_collected = 0 
            print("ускорились!")

    
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.Sound('crash.wav').play()
            time.sleep(0.5)
                        
            DISPLAYSURF.fill(red)
            DISPLAYSURF.blit(game_over, (30,250))
            
            pygame.display.update()
            for entity in all_sprites:
                    entity.kill() 
            time.sleep(2)
            pygame.quit()
            sys.exit()        
            
        pygame.display.update()
        FramePerSec.tick(FPS)
        