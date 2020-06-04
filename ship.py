import pygame

from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """
        初始化飞船并设置其初始位置
        """
        super().__init__()

        self.screen = screen

        # 设置信息
        self.ai_settings = ai_settings

        # 加载飞船图像
        self.image = pygame.image.load('images/ship.bmp')

        # 获取飞船的外接矩形
        self.rect = self.image.get_rect()

        # 获取整个屏幕的外界矩形
        self.screen_rect = screen.get_rect()

        # 将飞船放在屏幕的底部中央的位置
        # 只设置 centerx 值，并没有设置 centery 值
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 设置飞船的center的小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """
        在指定位置绘制飞船
        :return:
        """
        # 参数 图片 位置
        self.screen.blit(self.image, self.rect)

    def update(self):
        """
        根据移动标志调整飞船的位置
        :return:
        """
        # 更新飞船的center值，而不是rect值
        # 向右移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        # 向左移动
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据飞船的center值更新rect对象
        self.rect.centerx = self.center

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.centerx = self.screen_rect.centerx