import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right: # 如果外星人的rect的right属性大于或等于屏幕的rect的right属性，就说明外星人位于屏幕右边缘
            return True
        elif self.rect.left <= 0: # 如果外星人的rect的left属性小于或等于0，就说明外星人位于屏幕左边缘
            return True

    def update(self):
        """向左或向右移动外星人"""
        # self.x += self.ai_settings.alien_speed_factor # 每次更新外星人位置时，都将它向右移动，移动量为alien_speed_factor的值。我们使用属性self.x跟踪每个外星人的准确位置
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction) # 将移动量设置为外星人速度和fleet_direction的乘积，让外星人向左或向右移
        self.rect.x = self.x # 用self.x的值来更新外星人的rect的位置
