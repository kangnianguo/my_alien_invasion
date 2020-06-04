import sys
import pygame

from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    # 初始化游戏
    pygame.init()

    ai_settings = Settings()

    # 创建一个屏幕对象的像素
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # 给屏幕对象设置字幕
    pygame.display.set_caption('外星人入侵游戏')

    # 创建开始游戏按钮
    play_button = Button(ai_settings, screen, 'play')
    # 创建一个用于存储游戏统计数据的实例
    stats = GameStats(ai_settings)

    # 创建计分板
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建一个用于存储外星人的编组
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:

            # 调整飞船的位置
            ship.update()

            # 删除已经消失的子弹，并且移动子弹
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            # 调整外星人的位置
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)



        # 更新绘制新屏幕，擦掉旧屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)



run_game()