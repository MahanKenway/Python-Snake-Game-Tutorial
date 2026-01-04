"""
بازی مار (Snake Game)
یک بازی کلاسیک برای یادگیری برنامه‌نویسی بازی با Python و Pygame

نحوه بازی:
- از کلیدهای جهت‌دار (Arrow Keys) برای حرکت مار استفاده کنید
- غذا بخورید تا مار بزرگ‌تر شود
- از برخورد با دیواره‌ها یا خود مار اجتناب کنید
"""

import pygame
import random
import sys

# مقداردهی اولیه Pygame
pygame.init()

# تنظیمات صفحه نمایش
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

# رنگ‌ها
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

# ایجاد صفحه نمایش
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("بازی مار - Snake Game")

# تنظیم ساعت برای کنترل سرعت بازی
clock = pygame.time.Clock()
FPS = 10

# فونت برای نمایش امتیاز
font = pygame.font.Font(None, 36)


class Snake:
    """کلاس مار که حرکت و رشد مار را مدیریت می‌کند"""
    
    def __init__(self):
        # موقعیت اولیه مار در وسط صفحه
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)  # حرکت به راست
        self.grow = False
    
    def move(self):
        """حرکت مار به سمت جهت فعلی"""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # اضافه کردن سر جدید
        self.body.insert(0, new_head)
        
        # اگر باید رشد کند، دم را نگه می‌داریم
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        """تغییر جهت حرکت مار (نمی‌تواند به سمت مخالف برود)"""
        # جلوگیری از حرکت به سمت مخالف
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def check_collision(self):
        """بررسی برخورد با دیوار یا خود مار"""
        head_x, head_y = self.body[0]
        
        # برخورد با دیوار
        if (head_x < 0 or head_x >= WIDTH or 
            head_y < 0 or head_y >= HEIGHT):
            return True
        
        # برخورد با خود
        if self.body[0] in self.body[1:]:
            return True
        
        return False
    
    def eat_food(self, food_pos):
        """بررسی خوردن غذا"""
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False
    
    def draw(self, surface):
        """رسم مار روی صفحه"""
        for i, segment in enumerate(self.body):
            # سر مار را با رنگ متفاوت نشان می‌دهیم
            color = BLUE if i == 0 else GREEN
            pygame.draw.rect(surface, color, 
                           (segment[0], segment[1], CELL_SIZE, CELL_SIZE))


class Food:
    """کلاس غذا که موقعیت غذا را مدیریت می‌کند"""
    
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        """تولید موقعیت تصادفی برای غذا"""
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        return (x, y)
    
    def respawn(self, snake_body):
        """ظاهر شدن مجدد غذا در موقعیت جدید (نه روی مار)"""
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break
    
    def draw(self, surface):
        """رسم غذا روی صفحه"""
        pygame.draw.rect(surface, RED, 
                        (self.position[0], self.position[1], 
                         CELL_SIZE, CELL_SIZE))


def draw_score(surface, score):
    """نمایش امتیاز روی صفحه"""
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))


def game_over_screen(surface, score):
    """صفحه پایان بازی"""
    surface.fill(BLACK)
    
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to restart or ESC to quit", True, WHITE)
    
    surface.blit(game_over_text, 
                (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    surface.blit(score_text, 
                (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    surface.blit(restart_text, 
                (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 2 // 3))
    
    pygame.display.flip()


def main():
    """تابع اصلی بازی"""
    while True:
        # ایجاد اشیاء بازی
        snake = Snake()
        food = Food()
        score = 0
        game_running = True
        
        # حلقه اصلی بازی
        while game_running:
            # بررسی رویدادها
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # کنترل جهت با کلیدهای جهت‌دار
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -CELL_SIZE))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, CELL_SIZE))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-CELL_SIZE, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((CELL_SIZE, 0))
            
            # حرکت مار
            snake.move()
            
            # بررسی خوردن غذا
            if snake.eat_food(food.position):
                score += 10
                food.respawn(snake.body)
            
            # بررسی برخورد
            if snake.check_collision():
                game_running = False
            
            # رسم صفحه
            screen.fill(BLACK)
            snake.draw(screen)
            food.draw(screen)
            draw_score(screen, score)
            
            pygame.display.flip()
            clock.tick(FPS)
        
        # صفحه پایان بازی
        game_over_screen(screen, score)
        
        # منتظر ورودی کاربر برای شروع مجدد یا خروج
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    main()
