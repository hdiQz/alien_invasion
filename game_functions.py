import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets): # 编组bullets传递给了check_keydown_events()，按空格键创建一颗新子弹
    if event.key == pygame.K_RIGHT: # 读取属性event.key，以检查按下的是否是右箭头键
        # 向右移动飞船
        ship.moving_right = True # 将ship.rect.centerx的值加1，从而将飞船向右移动；不直接调整飞船的位置，而只是将moving_right设置为True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE: # 使用方法add()将新子弹加入到编组bullets中
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q: # 按Q时结束游戏
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets): # 将发射子弹的代码移到一个独立的函数中
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    # 创建新子弹并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets): # 需要添加形参bullets
    """响应按键和鼠标事件"""
    for event in pygame.event.get(): # 访问pygame检测到的事件
        if event.type == pygame.QUIT: # 玩家单机游戏窗口的关闭按钮
            sys.exit() # 退出游戏
        elif event.type == pygame.KEYDOWN: # 添加elif模块以便在pygame检测到KEYDOWN事件时作出响应
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP: # 用于响应KEYUP事件，玩家松开右箭头键时，我们将moving_right设置为False
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN: # 只在单击Play按钮时作出响应
            mouse_x, mouse_y = pygame.mouse.get_pos() # 返回一个元组，包含单击时鼠标的坐标
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y) # 坐标传递给该函数

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y) # True或False
    if button_clicked and not stats.game_active: # 检查鼠标单击位置是否在Play按钮的rect内；当单击了Play按钮且游戏当前处于非活动状态时，游戏才重新开始
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats() # 重置游戏统计信息
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships() # 让玩家知道有多少艘飞船

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty() # 清空编组aliens和bullets

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button): # 添加形参bullets
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color) # 用背景色填充屏幕；使用ai_settings来访问背景色
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites(): # 方法bullets.sprites()返回一个列表，其中包含编组bullets中的所有精灵
        bullet.draw_bullet() # 每个精灵调用draw_bullet()
    ship.blitme() # 将飞船绘制到屏幕上，确保它出现在背景前面
    aliens.draw(screen) # 让外星人出现在屏幕上；将blitme修改为draw，在屏幕上绘制编组中的每个外星人；

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip() # 不断更新屏幕，以显示元素的新位置，并在原来的位置隐藏元素，从而营造平滑移动的效果

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update() # 将为编组bullets中的每颗子弹调用bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy(): # 
        if bullet.rect.bottom <= 0: # 检查每颗子弹，看看是否已从屏幕顶端消失
            bullets.remove(bullet) # 删除子弹
    # print(len(bullets)) # 显示当前还有多少颗子弹
    check_bullets_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullets_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹集中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) # 每当有子弹和外星人的rect重叠时，groupcollide()就在它返回的字典中添加一个键-值对。两个实参True告诉Pygame删除发生碰撞的子弹和外星人。

    if collisions:
        for aliens in collisions.values(): # 遍历字典collisions，确保将消灭的每个外星人的点数都记入得分
            stats.score += ai_settings.alien_points * len(aliens) # 有子弹撞到外星人时，pygame返回一个字典（collisions），如果这个字典存在，就将得分加上一个外星人值的点数
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0: # 检查编组aliens是否为空。
        # 删除现有的子弹，加快游戏节奏，并新建一群外星人
        # 如果整群外星人都被消灭，就提高一个等级
        bullets.empty() # 删除编组中余下的所有精灵，从而删除现有的所有子弹。
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1 # 将stats.level的值加1
        sb.prep_level() # 显示新等级

        create_fleet(ai_settings, screen, ship, aliens) # 再次在屏幕上显示一群外星人

def get_number_aliens_x(ai_settings, alien_width): # 来自create_fleet()
    """计算每行可容纳多少个外星人"""
    availiable_space_x = ai_settings.screen_width - 2 * alien_width # 计算可用于放置外星人的水平空间；
    number_aliens_x = int(availiable_space_x / (2 * alien_width)) # 整数化外星人数量
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height): # 计算屏幕可容纳多少行外星人
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number): # 来自create_fleet()
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen) # 创建一个新的外星人
    alien_width = alien.rect.width # 从外星人的rect属性中获取外星人宽度，并将这个值存储到alien_width中；
    alien.x = alien_width + 2 * alien_width * alien_number # 将外星人宽度乘以2，得到每个外星人占据的空间，再据此计算当前外星人在当前行的位置
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number # 修改外星人的y坐标，并在第一行外星人上方留出与外星人等高的空白区域。相邻外星人行的y坐标相差外星人高度的两倍，因此将外星人高度乘以2，再乘以行号。
    aliens.add(alien) # 将每个新创建的外星人都添加到编组aliens中

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen) # 创建一个外星人，用于知道外星人的宽度和高度；
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width) # 将计算可用水平空间的代码替换为对get_number_aliens_x()的调用
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建第一行外星人；创建外星人群
    for row_number in range(number_rows):# 外部循环创建所有行
        for alien_number in range(number_aliens_x): # 内部循环创建一行外星人
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number) # 将创建外星人的代码替换为对create_alien()的调用

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges(): # 如果check_edges()返回True，就知道相应的外星人位于屏幕边缘，需要改变外星人群的方向
            change_fleet_direction(ai_settings, aliens) # 改变外星人的方向
            break # 退出循环

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed # 遍历所有外星人，将每个外星人下移fleet_drop_speed设置的值
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_lefts减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships() # 损失飞船后更新飞船数
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True) # 游戏进入非活动状态后，立即让光标可见

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # 暂停
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新外星人群中所有外星人的位置"""
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings, aliens) # 确定是否有外星人位于屏幕边缘
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens): # 如果没有发生碰撞，spritecollideany()将返回None，因此if代码块不会执行。
        #print("Ship hit!!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score # 更新high_score的值
        sb.prep_high_score() # 更新包含最高得分的图像
