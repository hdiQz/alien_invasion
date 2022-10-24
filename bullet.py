import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height) # 创建子弹的属性rect，使用pygame.Rect()类从空白开始创建一个矩形，矩形左上角的x坐标，矩形右上角的y坐标，矩形的宽度，矩形的高度
        self.rect.centerx = ship.rect.centerx # 将子弹的centerx设置为飞船的rect.centerx
        self.rect.top = ship.rect.top # 将表示子弹的rect的top属性设置为飞船的rect的top属性，让子弹看起来像是从飞船中射出的

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y) # 将子弹的y坐标存储为小数值，以便能够微调子弹的速度

        self.color = ai_settings.bullet_color # 将子弹的颜色和速度设置分别储存到self.color和self.speed_factor中
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self): # 管理子弹的位置
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor # 子弹在屏幕中向上移动，这意味着y坐标将不断减少
        # 更新表示子弹的rect的位置
        self.rect.y = self.y # 将self.rect设置为self.y的值
    
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect) # 使用存储在self.color中的颜色填充表示子弹的rect占据的屏幕部分

