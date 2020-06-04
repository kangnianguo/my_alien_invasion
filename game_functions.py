import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        # 创建一颗子弹
        new_bullet = Bullet(ai_settings, screen, ship)
        # 并将其加入到编组bullets中
        bullets.add(new_bullet)

def check_keydown_event(event, ai_settings, screen, ship, bullets):
    # 如果点击了右键
    if event.key == pygame.K_RIGHT:
        # 设置向右移动标志
        ship.moving_right = True
    # 如果点击了左键
    elif event.key == pygame.K_LEFT:
        # 设置向左移动标志
        ship.moving_left = True
    # 如果点击了空格
    elif event.key == pygame.K_SPACE:
        # 如果满足条件就开火
        fire_bullet(ai_settings, screen, ship, bullets)
    # 如果点击了 q 键
    elif event.key == pygame.K_q:
        # 退出游戏
        sys.exit()

def check_keyup_event(event, ship):
    # 如果松开了右键
    if event.key == pygame.K_RIGHT:
        # 设置向右移动的标志
        ship.moving_right = False
    # 如果松开了左键
    if event.key == pygame.K_LEFT:
        # 设置向左移动的标志
        ship.moving_left = False
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家点击了play按钮后开始游戏"""
    button_cliked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_cliked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """
    处理事件循环，响应按键和鼠标事件
    :return:
    """
    for event in pygame.event.get():
        # 点击了关闭按钮
        if event.type == pygame.QUIT:
            # 游戏结束
            sys.exit()
        # 如果点击了按钮
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        # 如果检测到按键事件
        elif event.type == pygame.KEYDOWN:
            # 处理点击事件
            check_keydown_event(event,ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            # 处理松开事件
            check_keyup_event(event, ship)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():

            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)

    # 如果外星人数量为零
    if len(aliens) == 0:
        # 清空所有子弹
        bullets.empty()

        # 加快游戏节奏
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        # 更新显示等级
        sb.prep_level()
        # 重建一群外星人
        create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹
    for bullet in bullets.sprites():
        bullet.update()

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)



def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """
    更新屏幕上的图像，并切换到新屏幕
    """
    # 设置背景颜色
    screen.fill(ai_settings.bg_color)

    # 绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()

    # 绘制外星人
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # 擦去旧屏幕，让最近绘制的屏幕可见
    pygame.display.flip()

def get_number_aliens_x(ai_settings, alien_width):
    # 计算一行可容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行的外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放到当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人
    alien = Alien(ai_settings, screen)

    # 计算每行可容纳多少个外星人
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        # 创建一行外星人
        for alien_number in range(number_aliens_x):
            # 创建一个外星人
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新外星人群所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底部
    check_aliens_bottom(ai_settings,  screen, stats, sb, ship, aliens, bullets)

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到飞船"""
    if stats.ships_left > 0:
        # 将ships_left减去一
        stats.ships_left -= 1
        sb.prep_ships()
        # 清空外星人列表
        aliens.empty()
        # 清空子弹列表
        bullets.empty()
        # 创建一群外星人
        create_fleet(ai_settings, screen, ship, aliens)
        # 将飞船放到中央
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_setting, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞一样处理
            ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()