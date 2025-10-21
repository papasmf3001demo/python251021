import pygame
import random

class Game:
    def __init__(self):
        self.width = 800
        self.height = 600
        # 패들 폭이 3배(300)로 커졌으므로 중앙 위치 계산을 -150으로 조정
        self.paddle = Paddle(self.width // 2 - 150, self.height - 30)
        self.ball = Ball(self.width // 2, self.height - 50)
        self.bricks = self.create_bricks()
        self.items = []    # 떨어지는 아이템 목록
        self.bullets = []  # 발사된 총알 목록
        self.can_shoot = False
        self.ammo = 0
        self.shoot_cooldown = 300  # ms
        self._last_shot = 0
        self.running = True
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)

    def create_bricks(self):
        bricks = []
        # 더 화려한 색상 팔레트 (상단부터 차례로)
        colors = [
            (255, 102, 204),  # 핑크
            (255, 153, 51),   # 주황
            (255, 255, 51),   # 노랑
            (102, 255, 178),  # 연두
            (102, 178, 255)   # 하늘
        ]
        for i in range(5):
            for j in range(10):
                color = colors[i % len(colors)]
                bricks.append(Brick(j * 80 + 10, i * 30 + 10, color))
        return bricks

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move(-7)
        if keys[pygame.K_RIGHT]:
            self.paddle.move(7)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if not self.can_shoot:
            return
        now = pygame.time.get_ticks()
        if now - self._last_shot < self.shoot_cooldown:
            return
        if self.ammo <= 0:
            return
        # 총알은 패들 중앙에서 위로 발사
        bx = self.paddle.x + self.paddle.width // 2
        by = self.paddle.y - 5
        self.bullets.append(Bullet(bx, by))
        self.ammo -= 1
        self._last_shot = now
        # 만약 탄약이 다 떨어지면 쏠 수 없음
        if self.ammo <= 0:
            self.can_shoot = False

    def update(self):
        self.ball.move()
        if self.ball.y + self.ball.radius > self.height:
            self.running = False
        if self.ball.collides_with(self.paddle):
            self.ball.bounce()

        # 공과 벽돌 충돌
        for brick in list(self.bricks):
            if self.ball.collides_with(brick):
                self.ball.bounce()
                self.bricks.remove(brick)
                # 벽돌 파괴 시 아이템 생성 (확률적으로)
                if random.random() < 0.8:  # 80% 확률로 아이템 드롭
                    self.spawn_item(brick.x + brick.width // 2, brick.y + brick.height // 2)
                break

        # 총알 업데이트 및 벽돌 충돌
        for bullet in list(self.bullets):
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)
                continue
            for brick in list(self.bricks):
                if bullet.collides_with(brick):
                    self.bullets.remove(bullet)
                    self.bricks.remove(brick)
                    # 총알로 부순 벽돌도 아이템 드롭 가능
                    if random.random() < 0.8:
                        self.spawn_item(brick.x + brick.width // 2, brick.y + brick.height // 2)
                    break

        # 아이템 업데이트 및 패들과 충돌 검사
        for item in list(self.items):
            item.move()
            if item.y > self.height:
                self.items.remove(item)
                continue
            if item.collides_with(self.paddle):
                self.items.remove(item)
                # 아이템을 먹으면 총알 사용 권한과 탄약을 부여
                self.can_shoot = True
                self.ammo += item.ammo_amount
                # 제한: 너무 많은 탄약 방지
                if self.ammo > 50:
                    self.ammo = 50

    def spawn_item(self, x, y):
        # 중앙 x,y 좌표를 받아 아이템 객체 생성 (떨어지는 방식)
        self.items.append(Item(x, y))

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.paddle.draw(screen)
        self.ball.draw(screen)
        for brick in self.bricks:
            brick.draw(screen)
        for item in self.items:
            item.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
        # HUD: 총알 가능 여부와 탄약 수 표시
        status = f"Shoot: {'ON' if self.can_shoot else 'OFF'}  Ammo: {self.ammo}"
        text = self.font.render(status, True, (255,255,255))
        screen.blit(text, (10, self.height - 25))
        pygame.display.flip()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input()
            self.update()
            self.render(screen)
            clock.tick(60)

        pygame.quit()


class Paddle:
    def __init__(self, x, y):
        # 폭을 3배로 증가
        self.width = 300
        self.height = 10
        self.x = x
        self.y = y

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        if self.x > 800 - self.width:
            self.x = 800 - self.width

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))


class Ball:
    def __init__(self, x, y):
        self.radius = 10
        self.x = x
        self.y = y
        self.dx = 4
        self.dy = -4

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x - self.radius <= 0 or self.x + self.radius >= 800:
            self.dx *= -1
        if self.y - self.radius <= 0:
            self.dy *= -1

    def bounce(self):
        self.dy *= -1

    def collides_with(self, obj):
        if isinstance(obj, Paddle):
            return (self.x > obj.x and self.x < obj.x + obj.width and
                    self.y + self.radius > obj.y and self.y - self.radius < obj.y + obj.height)
        elif isinstance(obj, Brick):
            return (self.x > obj.x and self.x < obj.x + obj.width and
                    self.y + self.radius > obj.y and
                    self.y - self.radius < obj.y + obj.height)
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)


class Brick:
    def __init__(self, x, y, color=(255, 0, 0)):
        self.width = 80
        self.height = 30
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # 테두리 추가로 더 화려하게 보이게 함
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)


class Item:
    def __init__(self, x, y):
        # x,y는 중앙 좌표로 전달됨 -> 아이템의 좌표를 왼쪽 상단 기준으로 변경
        self.width = 20
        self.height = 20
        self.x = int(x - self.width // 2)
        self.y = int(y - self.height // 2)
        self.dy = 3
        # 아이템 종류별로 탄약 수를 달리할 수 있음
        self.ammo_amount = random.choice([3, 5, 8])

    def move(self):
        self.y += self.dy

    def collides_with(self, paddle):
        return (self.x < paddle.x + paddle.width and
                self.x + self.width > paddle.x and
                self.y < paddle.y + paddle.height and
                self.y + self.height > paddle.y)

    def draw(self, screen):
        # 화려한 색상의 아이템
        pygame.draw.rect(screen, (255, 215, 0), (self.x, self.y, self.width, self.height))
        # 탄약 수 표시 (작게)
        # (간단성을 위해 표시는 생략하거나 추후 추가 가능)


class Bullet:
    def __init__(self, x, y):
        self.width = 4
        self.height = 10
        self.x = int(x - self.width // 2)
        self.y = int(y - self.height)
        self.dy = -8

    def move(self):
        self.y += self.dy

    def collides_with(self, brick):
        return (self.x < brick.x + brick.width and
                self.x + self.width > brick.x and
                self.y < brick.y + brick.height and
                self.y + self.height > brick.y)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.width, self.height))


if __name__ == "__main__":
    game = Game()
    game.run()