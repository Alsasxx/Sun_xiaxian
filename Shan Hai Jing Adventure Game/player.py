import pygame

pygame.mixer.init()

# 初始化音效
jump_sound = pygame.mixer.Sound('assets/sounds/jump_sound.wav')
jump_sound.set_volume(1.0)

attack_sound = pygame.mixer.Sound('assets/sounds/attack_sound.wav')
attack_sound.set_volume(1.0)

walk_sound = pygame.mixer.Sound('assets/sounds/walk_sound.wav')
walk_sound.set_volume(0.5)

class Player:
    def __init__(self, x, y, character_images, game_map):
        self.x = x  # 玩家初始横坐标 # Initial horizontal coordinates of the player
        self.y = y  # 玩家初始纵坐标# Initial vertical coordinate of the player
        self.character_images = character_images  # 玩家角色图像字典 # Player Character Image Dictionary
        self.game_map = game_map  # 地图实例# Examples of maps
        self.action = 'right_idle'  # 初始动作 # Initial action
        self.direction = 'right'  # 初始方向 # Initial direction
        self.image = self.character_images[self.action][0]  # 当前显示的角色图像# Currently displayed character image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))  # 角色碰撞矩形# Character collision rectangle
        self.speed = 3  # 玩家移动速度# Player movement speed
        self.jump_height = -5  # 玩家跳跃高度# Player jump height
        self.gravity = 0.5  # 重力 # Gravity
        self.velocity_y = 0.5  # 垂直速度# Vertical speed
        self.is_jumping = False  # 是否在跳跃# Is it jumping
        self.frame_index = 0  # 初始化帧索引# Initialise frame index
        self.animation_speed = 0.1  # 控制动画帧速 # Control the animation frame rate
        self.walking_played = False  # 防止重复播放行走音效# Prevent repetition of walking sound effects
        self.jump_cooldown = 0.5  # 跳跃冷却时间

    def is_on_ground(self):
        """检查玩家是否站在地面上"""
        self.rect.topleft = (self.x + 5, self.y + 5)  # 偏移1像素检测地面 # Offset 1 pixel to detect ground
        for tile in self.game_map.tiles:
            if self.rect.colliderect(tile["rect"]):  # 检测玩家底部是否与地图块顶部接触# Detect if the bottom of the player is in contact with the top of the map block
                return tile["rect"]  # 返回碰撞的地图块 # Returns colliding map blocks
        return None

    def update(self, keys):
        # 水平移动
        if keys[pygame.K_LEFT]:
            self.direction = 'left'
            self.action = 'left'
            self.x -= self.speed
            if not self.walking_played:
                walk_sound.play()
                self.walking_played = True
        elif keys[pygame.K_RIGHT]:
            self.direction = 'right'
            self.action = 'right'
            self.x += self.speed
            if not self.walking_played:
                walk_sound.play()
                self.walking_played = True
        elif keys[pygame.K_a]:
            self.action = f'{self.direction}_attack'
            attack_sound.play()
        else:
            if not self.is_jumping:  # 只有在没有跳跃时切换为 idle # Only switch to idle when there's no jump
                self.action = f'{self.direction}_idle'
            if self.walking_played:
                walk_sound.stop()
                self.walking_played = False

        # 检查是否站在地图块上
        ground_tile = self.is_on_ground()

# 跳跃逻辑
        def update(self, keys):
            # 检查是否站在地图块上
            ground_tile = self.is_on_ground()

        if ground_tile:  # 如果站在地面上# If you stand on the ground
            self.y = ground_tile.top - self.rect.height
            self.velocity_y = 0
            self.is_jumping = False
            self.jump_cooldown = 0.5  # 重置跳跃冷却时间

        if keys[pygame.K_SPACE]:  # 按下跳跃键# Press the jump button
            self.velocity_y = self.jump_height
            self.is_jumping = True
            self.action = f'{self.direction}_jump'
            jump_sound.play()

        else:  # 如果不在地面上 # If it's not on the ground
            print("updated y", self.y)
            self.velocity_y += self.gravity
        self.y += self.velocity_y

        # 防止角色掉出屏幕# Prevent characters from falling off the screen
        if self.y > 800:  # 屏幕底部限制 # Bottom of screen restrictions
            self.y = 800
            self.is_jumping = False
            self.velocity_y = 0
        print(self.velocity_y)
        print("jumping", self.is_jumping)
        print("y", self.y)
        # 更新动画帧 #Update the animation frame
        if self.action in self.character_images:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.character_images[self.action]):
                self.frame_index = 0
            self.image = self.character_images[self.action][int(self.frame_index)]

        # 更新碰撞矩形位置# Update the collision rectangle position
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
