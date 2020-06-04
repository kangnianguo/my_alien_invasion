import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    一个对飞船发射的子弹进行管理的类
    """
    def __init__(self, ai_settings, screen, ship):
        # 调用父类的构造函数
        super().__init__()
        self.screen = screen

        # 初始化子弹的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)

        # 子弹的位置
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top

        # 用小数表示子弹的位置（纵坐标）
        self.y = float(self.rect.y)

        # 子弹的颜色
        self.color = ai_settings.bullet_color

        # 子弹的速度
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 更新子弹位置的小数值
        self.y -= self.speed_factor
        # 更新子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        # 绘制长方形
        pygame.draw.rect(self.screen, self.color, self.rect)



