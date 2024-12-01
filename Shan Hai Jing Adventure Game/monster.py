import pygame

class Monster:
    def __init__(self, x, y, images, health=3, speed=2, start_x=200, end_x=800):
        """
        初始化怪物
        :param x: 初始横坐标
        :param y: 初始纵坐标
        :param images: 怪物的两张图片，用于循环动画
        :param health: 怪物的生命值
        :param speed: 怪物的运动速度
        :param start_x: 怪物运动的起始位置
        :param end_x: 怪物运动的结束位置
        """
        self.x = x
        self.y = y
        self.images = images  # 两张图片用于动画
        self.image_index = 0
        self.animation_speed = 0.1  # 动画播放速度
        self.health = health  # 怪物的生命值
        self.speed = speed  # 怪物的速度
        self.start_x = start_x  # 起始位置
        self.end_x = end_x  # 结束位置
        self.rect = self.images[0].get_rect(topleft=(self.x, self.y))  # 怪物的碰撞矩形
        self.alive = True  # 怪物是否存活

    def update(self):
        """更新怪物的动画和运动"""
        if self.alive:
            # 动画逻辑
            self.image_index += self.animation_speed
            if self.image_index >= len(self.images):
                self.image_index = 0

            # 限制怪物只在 start_x 和 end_x 之间来回运动
            self.x += self.speed
            if self.x <= self.start_x or self.x >= self.end_x:  # 碰到指定范围时反向
                self.speed = -self.speed  # 反向运动

            # 更新位置
            self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        """绘制怪物"""
        if self.alive:
            screen.blit(self.images[int(self.image_index)], self.rect)

    def take_damage(self):
        """怪物受到攻击，减少生命值"""
        if self.alive:
            self.health -= 1
            print(f"Monster took damage! Remaining health: {self.health}")
            if self.health <= 0:
                self.die()

    def die(self):
        """怪物死亡"""
        self.alive = False
        print("Monster is dead!")
