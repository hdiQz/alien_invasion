import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init() # 初始化背景设置
    ai_settings = Settings() # 创建一个Settings实例，并将其存储在变量ai_settings中
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height)) # 创建一个名为screen的显示窗口
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play") # 创建一个名为play_button的实例

    # 创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats) # 创建一个名为sb的ScoreBoard实例

    # 设置背景颜色
    bg_color = (230, 230, 230)

    # 创建一艘飞船、一个用于存储子弹的编组，和一个外星人编组
    ship = Ship(ai_settings, screen) # 创建飞船实例，避免每次循环都创建飞船
    bullets = Group() # 创建一个Group实例，并将其命名为bullets
    #alien = Alien(ai_settings, screen) # 创建alien实例
    aliens = Group() # 创建了一个空编组，用于存储所有的外星人

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens) # 调用create_fleet()，并将ai_settings、对象screen和空编组aliens传递给它

    # 开始游戏的主循环
    while True: # while循环控制游戏

        # 响应按键
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets) # 需要在玩家按空格键时处理bullets

        if stats.game_active:
            # 允许不断移动
            ship.update()

            # 删除已消失的子弹
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            # 更新每个外星人的位置
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
        # 每次循环时都重绘屏幕，让最近绘制的屏幕可见
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button) # 需要更新要绘制到屏幕上的bullets；传递一个外星人实例；修改alien为aliens，让它能够访问外星人编组；将play_button传递给该方法，以便能够在屏幕更新时显示按钮；

run_game()
