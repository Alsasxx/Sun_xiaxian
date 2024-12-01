import pygame
import sys
from player import Player
from map_data import tile_data
from map import Map
from monster import Monster


# 初始化 pygame。
pygame.init()

# 设置游戏窗口大小  
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置窗口标题
pygame.display.set_caption("山海经冒险游戏")

# 定义帧率
clock = pygame.time.Clock()

# 加载背景图片 (png格式)
background = pygame.image.load('assets/images/background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))  # 调整背景图大小

# 加载新的背景图片 (png格式)
game_background = pygame.image.load('assets/images/new_background.png')
game_background = pygame.transform.scale(game_background, (screen_width, screen_height))  # 调整背景图大小

# 加载中文字体
font_path_chinese = 'assets/fonts/FZZiZLDJW.TTF'  # 中文字体
font_chinese = pygame.font.Font(font_path_chinese, 72)

# 加载英文字体
font_path_english = 'assets/fonts/joystix.ttf'  # 英文字体
font_english = pygame.font.Font(font_path_english, 28)  # 英文字体大小为28

# 加载音效文件
click_sound = pygame.mixer.Sound('assets/sounds/click_sound.wav')
intro_sound = pygame.mixer.Sound('assets/sounds/intro_sound.wav')  # 开场背景音效

# 加载按钮图片 (png格式)
button_image = pygame.image.load('assets/images/start_button.png').convert_alpha()
button_rect = button_image.get_rect(center=(screen_width // 2, screen_height // 1.3))  # 按钮位置在屏幕下方

# 加载角色图像（12张图）# Character images loaded (12 images)
character_images = {
    'right_idle': [pygame.image.load('assets/images/character/right_idle.png')],
    'left_idle': [pygame.image.load('assets/images/character/left_idle.png')],
    'right': [pygame.image.load('assets/images/character/right1.png'),
              pygame.image.load('assets/images/character/right2.png')],
    'left': [pygame.image.load('assets/images/character/left1.png'),
             pygame.image.load('assets/images/character/left2.png')],
    'right_attack': [pygame.image.load('assets/images/character/right_attack1.png'),
                     pygame.image.load('assets/images/character/right_attack2.png')],
    'left_attack': [pygame.image.load('assets/images/character/left_attack1.png'),
                    pygame.image.load('assets/images/character/left_attack2.png')],
    'right_jump': [pygame.image.load('assets/images/character/right_jump.png')],
    'left_jump': [pygame.image.load('assets/images/character/left_jump.png')],
}

# 将角色图像缩小到适当尺寸# Reduce character images to appropriate size
def resize_images(character_images, scale_factor=0.12):
    for key in character_images:
        character_images[key] = [pygame.transform.scale(img, (int(img.get_width() * scale_factor),
                                                              int(img.get_height() * scale_factor))) for img in character_images[key]]

resize_images(character_images)  # 缩小角色图像

# 加载怪物图像（2张图）# Load monster images (2 images)
monster_images = [
    pygame.image.load('assets/images/moster/left_whelk1.png'),
    pygame.image.load('assets/images/moster/left_whelk2.png')
]

# 在 main.py 中添加传送门
portal_image = pygame.image.load('assets/images/tiles/853_23.png')
portal_image = pygame.transform.scale(portal_image, (100, 100))  # 传送门图片大小
portal_rect = portal_image.get_rect(topleft=(853, 23))  # 设置传送门的位置，假设在(500, 100)处


# 开场页面显示# Opening page display
def show_intro():
    # 播放开场背景音效   # Play the opening background sound effect
    intro_sound.play(-1)  # -1 表示循环播放背景音效

    running = True
    fade_in_time = 0.5  # 字体逐渐浮现的时间（秒）
    fade_in_speed = 300 / (fade_in_time * 120)  # 每帧字体透明度增加量（每秒120帧）

    # 中文文字
    text_chinese = font_chinese.render("山海经冒险游戏", True, (255, 255, 255))  # 白色文字
    text_rect_chinese = text_chinese.get_rect(center=(screen_width // 2, screen_height // 3))  # 中文文字位置调整

    # 英文文字
    text_english = font_english.render("Shan Hai Jing Adventure Game", True, (255, 255, 255))  # 白色文字
    text_rect_english = text_english.get_rect(center=(screen_width // 2, screen_height // 2.3))  # 英文文字在中文下方

    # 设置透明度初始值
    alpha_value = 0
    start_game = False  # 新增标志位

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos) and alpha_value >= 255:  # 确保完全显示后才可点击
                    click_sound.play()  # 播放点击音效
                    pygame.time.delay(500)  # 等待音效播放完成
                    intro_sound.stop()  # 停止背景音效
                    start_game = True  # 标志进入游戏
                    running = False

        # 填充背景
        screen.blit(background, (0, 0))

        # 逐渐增加透明度
        if alpha_value < 255:
            alpha_value += fade_in_speed
        else:
            alpha_value = 255

        # 应用透明度到文字
        text_chinese.set_alpha(alpha_value)
        text_english.set_alpha(alpha_value)

        # 应用透明度到按钮
        button_image.set_alpha(alpha_value)

        # 绘制文字
        screen.blit(text_chinese, text_rect_chinese)
        screen.blit(text_english, text_rect_english)

        # 绘制按钮
        screen.blit(button_image, button_rect)

        # 刷新显示
        pygame.display.flip()
        clock.tick(60)  # 设置帧率

    return start_game  # 返回标志位

def game_loop():
    """游戏主循环"""
    game_map = Map(tile_data)  # 加载地图块数据# Load map block data
    player = Player(100, 600, character_images, game_map)  # 初始化玩家

    #创建怪物 #Creating Monsters
    monster1 = Monster(500, 580, monster_images, start_x=487, end_x=560)
    monster2 = Monster(235, 151, monster_images, start_x=235, end_x=320)
    monster3 = Monster(580, 317, monster_images, start_x=579, end_x=710)
    
    #创建传送门
    portal_image = pygame.image.load('assets/images/tiles/853_23.png')
    portal_image = pygame.transform.scale(portal_image, (100, 100))
    portal_rect = portal_image.get_rect(topleft=(853, 23))  # 传送门的位置


    running = True
    while running:
        keys = pygame.key.get_pressed()  # 获取按键状态
        player.update(keys)  # 更新玩家位置和动画
        monster1.update()  #更新怪物
        monster2.update()
        monster3.update()
        
        # 检测传送门碰撞
        if player.rect.colliderect(portal_rect):  # 玩家与传送门碰撞
            print("You have reached the portal! Game Over.")  # 输出提示信息
            
            # 显示“游戏结束”的提示信息
            font = pygame.font.SysFont("arial", 36)
            text = font.render("You have reached the portal! Game Over.", True, (255, 255, 255))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))  # 居中显示
            pygame.display.flip()
            
            # 等待 3 秒钟显示提示
            pygame.time.delay(3000) 
            
            running = False  # 结束游戏

        # 绘制场景    # Drawing the scene
        screen.fill((0, 0, 0))  # 清空屏幕
        screen.blit(background, (0, 0))  # 绘制背景
        game_map.draw(screen)  # 绘制地图块
        player.draw(screen)  # 绘制玩家角色
        monster1.draw(screen)  # 绘制怪物1
        monster2.draw(screen)  # 绘制怪物2
        monster3.draw(screen)  # 绘制怪物3
        screen.blit(portal_image, portal_rect.topleft)  # 绘制传送门

        # 事件监听 # Event Listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:  # 假设A键是攻击键
                if player.rect.colliderect(monster1.rect):  # 如果主角与怪物碰撞
                    monster1.take_damage()  # 怪物1受到攻击
                if player.rect.colliderect(monster2.rect):  # 如果主角与怪物2碰撞
                    monster2.take_damage()  # 怪物2受到攻击
                if player.rect.colliderect(monster3.rect):  # 如果主角与怪物3碰撞
                    monster3.take_damage()  # 怪物3受到攻击


        pygame.display.flip()  # 更新显示
        clock.tick(60)  # 设置帧率

    pygame.quit()

# 主循环# Main loop
def main():
    if show_intro():  # 如果用户点击按钮进入游戏
        global background  # 声明修改全局变量
        background = game_background  # 切换背景为游戏背景

    game_loop()  # 进入游戏主循环

    pygame.quit()
    sys.exit()

# 启动主循环
if __name__ == "__main__":
    main()