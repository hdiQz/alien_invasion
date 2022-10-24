import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg): # 其中msg是要在按钮中显示的文本
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50 # 设置按钮的尺寸
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48) # 指定字体和文本的字号

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height) # 创建一个表示按钮的rect对象
        self.rect.center = self.screen_rect.center # 将对象的center属性设置为屏幕的center属性

        # 按钮的标签只需创建一次
        self.prep_msg(msg) # 将要显示的字符串渲染为图像来处理文本

    def prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) # 将存储在msg中的文本转换为图像，然后将该图像存储在msg_image中。布尔实参指定开启还是关闭反锯齿功能
        self.msg_image_rect = self.msg_image.get_rect() # 根据文本图像创建一个rect
        self.msg_image_rect.center = self.rect.center # 将文本图像的center属性设置为按钮的center属性
    
    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect) # 绘制表示按钮的矩形
        self.screen.blit(self.msg_image, self.msg_image_rect) # 在屏幕上绘制文本图像