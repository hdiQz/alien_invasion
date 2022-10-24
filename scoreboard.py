import pygame.font
from pygame.sprite import Group

from ship import Ship

class ScoreBoard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30) # 设置文本颜色
        self.font = pygame.font.SysFont(None, 48) # 实例化一个字体对象

        # 准备初始得分图像；准备包含最高得分和当前得分的图像
        self.prep_score() # 将要显示的文本转换为图像
        self.prep_high_score() # 显示包含最高得分的图像
        self.prep_level()
        self.prep_ships()
    
    def prep_ships(self):
        """显示还余下多少艘飞船"""
        self.ships = Group() # 方法prep_ships()创建一个空编组self.ships，用于存储飞船实例
        for ship_number in range(self.stats.ships_left): # 根据玩家还有多少艘飞船运行一个循环相应的次数
            ship = Ship(self.ai_settings, self.screen) # 创建一艘新飞船
            ship.rect.x = 10 + ship_number * ship.rect.width # 设置新飞船的x坐标，让整个飞船编组都位于屏幕左边，且每艘飞船的左边距都为10像素
            ship.rect.y = 10 # 将y坐标设置为离屏幕上边缘10像素，让所有飞船都与得分图像对齐
            self.ships.add(ship) # 将每艘新飞船都添加到编组ships中
    
    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = int(round(self.stats.high_score, -1)) # 将最高得分圆整到最近的10的整数倍
        high_score_str = "{:,}".format(high_score) # 添加了用逗号表示的千分位分隔符
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color) # 根据最高得分生成一幅图像

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx # 使图像水平居中
        self.high_score_rect.top = self.score_rect.top # 将图像top属性设置为当前得分图像的top属性

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1)) # 让python将stats.score的值圆整到最近的10的整数倍，并将结果存储到rounded_score中
        # score_str = str(self.stats.score) # 将数字值stats.score转换为字符串
        score_str = "{:,}".format(rounded_score) # 一个字符串格式设置指令，让python将数值转换为字符串时在其中插入逗号
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color) # 将这个字符串传递给创建图像的render()

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect() # 确保得分始终锚定在屏幕右边
        self.score_rect.right = self.screen_rect.right - 20 # 让得分右边缘与屏幕右边缘相距20像素
        self.score_rect.top = 20 # 让得分上边缘与屏幕上边缘相距20像素
    
    def show_score(self):
        """在屏幕上显示等级和得分"""
        self.screen.blit(self.score_image, self.score_rect) # 在屏幕右上角显示当前得分
        self.screen.blit(self.high_score_image, self.high_score_rect) # 在屏幕顶部中央显示最高得分
        self.screen.blit(self.level_image, self.level_rect) # 在屏幕上显示等级图像
        # 绘制飞船
        self.ships.draw(self.screen) # 绘制飞船

    def prep_level(self):
        """将等级转换为渲染的图像"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color) # 根据存储在stats.level中的值创建一幅图像

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right # 将图像的right属性设置为得分的right属性
        self.level_rect.top = self.score_rect.bottom + 10 # 将top属性设置为比得分图像的bottom属性大10像素，以便在得分和等级之间留出一定的空间
