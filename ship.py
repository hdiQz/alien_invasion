import pygame
from pygame.sprite import Sprite

class Ship(Sprite): # 负责管理飞船的大部分行为；导入了Sprite，让Ship继承Sprite

    def __init__(self, ai_settings, screen): # 添加ai_settings，让飞船能够获取其速度设置
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings # 将形参ai_settings的值存储在一个属性中，以便能够在update()中使用它

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp') # 加载飞船图像
        self.rect = self.image.get_rect() # 获取相应surface的属性rect
        self.screen_rect = screen.get_rect() # 将表示屏幕的矩形存储在self.screen_rect中

        # 将每款新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx # 将self.rect.centerx（飞船中心的x坐标）设置为表示屏幕的矩形的属性centerx
        self.rect.bottom = self.screen_rect.bottom # 将self.rect.bottom（飞船下边缘的y坐标）设置为表示屏幕的矩形的属性bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx) # 为准确地存储飞船的位置，定义了一个可存储小数值的属性self.center

        # 移动标志
        self.moving_right = False # 添加该属性，并将其初始值设置为False
        self.moving_left = False
    
    def update(self): # 在前述标志为True时向右移动飞船
        """根据移动标志调整飞船的位置"""
        # 更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right: # self.rect.right返回飞船外接矩形的右边缘的x坐标，如果这个值小于self.screen_rect.right的值，就说明飞船未触及屏幕右边缘
            self.center += self.ai_settings.ship_speed_factor # 将self.center的值增加或减去ai_settings.ship_speed_factor的值
        if self.moving_left and self.rect.left > 0: # 如果rect的左边缘的x坐标大于零，就说明飞船未触及屏幕左边缘
            self.center -= self.ai_settings.ship_speed_factor
        
        # 根据self.center更新rect对象
        self.rect.centerx = self.center # 更新self.center后，再根据它来更新控制飞船位置的self.rect.centerx
    
    def blitme(self): # 根据self.rect指定的位置将图像绘制到屏幕上
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
