import random

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIDropdown


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Astral Sentinel"

TEXTURE_PATHS = ["ship1.png", "ship2.png", "ship3.png"]
ENEMY_TEXTURE_PATH = "enemy.png"
BULLET_TEXTURE_PATH = "bullet.png"

explosion_textures = []
for i in range(8):
    texture_path = f"explosion/enemy_explosion_{i}.png"
    explosion_textures.append(arcade.load_texture(texture_path))


class Explosion(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.textures = explosion_textures
        self.set_texture(0)
        self.center_x = x
        self.center_y = y
        self.current_frame = 0
        self.animation_speed = 0.1  # время между кадрами
        self.time_elapsed = 0

    def update(self, delta_time):
        self.time_elapsed += delta_time

        if self.time_elapsed >= self.animation_speed:
            self.time_elapsed = 0
            self.current_frame += 1

            if self.current_frame < len(self.textures):
                self.set_texture(self.current_frame)

            else:
                self.remove_from_sprite_lists()


class Particle:
    def __init__(self, x, y, kind="explosion"):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.kind = kind

        if self.kind == "shot":
            self.color = arcade.color.WHITE

        else:
            self.color = random.choice([arcade.color.ORANGE, arcade.color.RED])

        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-1, 3)
        self.lifetime = 30  # кадров
        self.alpha = 255

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1

        if self.lifetime > 0:
            self.alpha = int(255 * (self.lifetime / 30))
        else:
            self.alpha = 0

    def draw(self):
        arcade.draw_circle_filled(
            self.x, self.y,
            self.size,
            (self.color[0], self.color[1], self.color[2], self.alpha)
        )


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.APPLE_GREEN
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        title = UILabel(
            text="The Astral Sentinel",
            font_size=30,
            text_color=arcade.color.WHITE,
            width=400
        )
        self.box_layout.add(title)

        start_button = arcade.gui.UIFlatButton(text="Начать", width=200)
        start_button.on_click = self.on_start
        self.box_layout.add(start_button)

        rules_button = arcade.gui.UIFlatButton(text="Прочитать правила", width=200)
        rules_button.on_click = self.on_read_rules
        self.box_layout.add(rules_button)

        results_button = arcade.gui.UIFlatButton(text="Посмотреть результаты", width=200)
        results_button.on_click = self.on_view_results
        self.box_layout.add(results_button)

        ship_label = UILabel(
            text="Выберите корабль:",
            font_size=20,
            text_color=arcade.color.WHITE,
            width=300
        )
        self.box_layout.add(ship_label)

        self.option_list = ["Случайный", "Первый", "Второй", "Третий"]
        self.textures = TEXTURE_PATHS
        self.player_texture = self.textures[0]

        self.dropdown = UIDropdown(options=self.option_list, width=200)
        self.dropdown.on_change = self.on_change
        self.box_layout.add(self.dropdown)

        difficulty_label = UILabel(
            text="Выберите уровень:",
            font_size=20,
            text_color=arcade.color.WHITE,
            width=300
        )
        self.box_layout.add(difficulty_label)

        self.difficulty_options = ["Обычный", "Сложный"]
        self.difficulty = self.difficulty_options[0]

        self.difficulty_dropdown = UIDropdown(
            options=self.difficulty_options,
            width=200
        )
        self.difficulty_dropdown.on_change = self.on_difficulty_change
        self.box_layout.add(self.difficulty_dropdown)

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

        self.ship_sprite_list = arcade.SpriteList()
        x_pos = SCREEN_WIDTH - 150
        y_start = SCREEN_HEIGHT - 250
        y_step = 80

        for texture_path in self.textures:
            sprite = arcade.Sprite(texture_path, scale=0.9)
            sprite.center_x = x_pos
            sprite.center_y = y_start - len(self.ship_sprite_list) * y_step
            self.ship_sprite_list.append(sprite)

    def on_difficulty_change(self, event):
        self.difficulty = self.difficulty_dropdown.value
        print(f"Выбран уровень: {self.difficulty}")

    def on_start(self, event):
        game_view = GameView(
            player_texture=self.player_texture,
            difficulty=self.difficulty
        )
        self.window.show_view(game_view)

    def on_read_rules(self, event):
        rules_view = RulesView()
        self.window.show_view(rules_view)

    def on_view_results(self, event):
        results_view = ResultsView()
        self.window.show_view(results_view)

    def on_change(self, event):
        i = self.option_list.index(self.dropdown.value)
        if i == 0:
            self.player_texture = random.choice(self.textures)
        elif i == 1:
            self.player_texture = self.textures[0]
        elif i == 2:
            self.player_texture = self.textures[1]
        elif i == 3:
            self.player_texture = self.textures[2]

    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.ship_sprite_list.draw()


class RulesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.rules_lines = [
            "Правила игры:",
            "1. Управляйте космическим кораблем стрелками.",
            "2. Стреляйте по врагам, нажимая пробел.",
            "3. Избегайте столкновений с врагами.",
            "4. Постарайтесь набрать как можно больше очков.",
            "",
            "Нажмите любую клавишу для возврата."
        ]
        self.text_objects = []
        y = SCREEN_HEIGHT - 150

        for line in self.rules_lines:
            text_obj = arcade.Text(
                text=line,
                x=50,
                y=y,
                color=arcade.color.WHITE,
                font_size=14
            )
            self.text_objects.append(text_obj)
            y -= 20

    def on_draw(self):
        self.clear()
        for text_obj in self.text_objects:
            text_obj.draw()

    def on_key_press(self, key, modifiers):
        menu_view = MenuView()
        self.window.show_view(menu_view)


class ResultsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.results_text = []
        try:
            with open("results.txt", "r") as f:
                self.results_text = f.readlines()
        except FileNotFoundError:
            self.results_text = ["Результаты еще не сохранены."]
        self.text_objects = []
        y = SCREEN_HEIGHT - 50

        for line in self.results_text:
            text_obj = arcade.Text(
                text=line.strip(),
                x=50,
                y=y,
                color=arcade.color.WHITE,
                font_size=14
            )
            self.text_objects.append(text_obj)
            y -= 20
        self.instruction = arcade.Text("Нажмите любую клавишу для возврата", x=50, y=20, color=arcade.color.WHITE,
                                       font_size=14)

    def on_draw(self):
        self.clear()
        for text_obj in self.text_objects:
            text_obj.draw()
        self.instruction.draw()

    def on_key_press(self, key, modifiers):
        menu_view = MenuView()
        self.window.show_view(menu_view)


class FinalResultsView(arcade.View):
    def __init__(self, final_score):
        super().__init__()
        self.final_score = final_score
        self.manager = UIManager()
        self.manager.enable()

        layout = UIAnchorLayout()
        box = UIBoxLayout(vertical=True, space_between=20, align="center")
        box.center_x = SCREEN_WIDTH // 2
        box.center_y = SCREEN_HEIGHT // 2

        title = UILabel(text="Игра завершена!", font_size=30, text_color=arcade.color.WHITE)
        box.add(title)

        score_label = UILabel(text=f"Ваш результат: {self.final_score} очков", font_size=20,
                              text_color=arcade.color.WHITE)
        box.add(score_label)

        best_score = self.get_best_score()
        best_label = UILabel(text=f"Лучший результат: {best_score} очков", font_size=20,
                             text_color=arcade.color.GOLD)
        box.add(best_label)

        menu_button = arcade.gui.UIFlatButton(text="В главное меню", width=200)
        menu_button.on_click = self.on_return
        box.add(menu_button)

        exit_button = arcade.gui.UIFlatButton(text="Выйти", width=200)
        exit_button.on_click = self.on_exit
        box.add(exit_button)

        layout.add(box)
        self.manager.add(layout)

    def get_best_score(self):
        try:
            with open("results.txt", "r") as f:
                lines = f.readlines()
            scores = []
            for line in lines:
                if "набрали" in line:
                    parts = line.split("набрали")

                    if len(parts) > 1:
                        score_str = parts[1].split("очков")[0].strip()

                        if score_str.isdigit():
                            scores.append(int(score_str))

            return max(scores) if scores else 0
        except (FileNotFoundError, ValueError):
            return 0

    def on_return(self, event):
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def on_exit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()


class GameView(arcade.View):
    def __init__(self, player_texture, difficulty):
        super().__init__()
        self.player_texture = player_texture
        self.difficulty = difficulty

        self.all_sprites = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.particles = []

        self.player_sprite = arcade.Sprite(self.player_texture, 0.5)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = 50
        self.all_sprites.append(self.player_sprite)

        self.score = 0
        self.spawn_enemy_timer = 0
        self.player_change_x = 0
        self.shoot_timer = 0

        self.setup_difficulty()

        self.shoot_sound = arcade.load_sound("shoot.wav")
        self.explosion_sound = arcade.load_sound("explosion.wav")


    def setup_difficulty(self):
        if self.difficulty == "Обычный":
            self.enemy_speed = 2
            self.shoot_cooldown = 0.5
            self.life = 5

        elif self.difficulty == "Сложный":
            self.enemy_speed = 3
            self.shoot_cooldown = 0.5
            self.life = 3


    def on_draw(self):
        self.clear()
        self.all_sprites.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.explosion_list.draw()

        for particle in self.particles:
            particle.draw()

        arcade.draw_text(f"Очки: {self.score}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Жизни: {self.life}", 10, SCREEN_HEIGHT - 40, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        self.player_sprite.center_x += self.player_change_x
        self.player_sprite.center_x = max(0, min(SCREEN_WIDTH, self.player_sprite.center_x))

        for enemy in self.enemy_list:
            enemy.center_y -= self.enemy_speed

            if enemy.center_y < 0:
                enemy.remove_from_sprite_lists()
                self.life -= 1

                if self.life <= 0:
                    self.game_over()

        for bullet in self.bullet_list:
            bullet.center_y += 5

            if bullet.center_y > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        for enemy in self.enemy_list:
            if arcade.check_for_collision(self.player_sprite, enemy):
                enemy.remove_from_sprite_lists()
                self.life -= 1

                if self.life <= 0:
                    self.game_over()

        for enemy in self.enemy_list[:]:
            for bullet in self.bullet_list[:]:

                if arcade.check_for_collision(bullet, enemy):

                    explosion = Explosion(enemy.center_x, enemy.center_y)
                    self.explosion_list.append(explosion)

                    arcade.play_sound(self.explosion_sound)

                    enemy.remove_from_sprite_lists()
                    bullet.remove_from_sprite_lists()
                    self.score += 1

                    for _ in range(10):
                        particle = Particle(enemy.center_x, enemy.center_y)
                        self.particles.append(particle)


        self.spawn_enemy_timer += delta_time

        if self.spawn_enemy_timer > 1.0:
            self.spawn_enemy()
            self.spawn_enemy_timer = 0

        if self.shoot_timer > 0:
            self.shoot_timer -= delta_time

        for particle in self.particles:
            particle.update()

        self.particles = [p for p in self.particles if p.lifetime > 0]

        for explosion in self.explosion_list:
            explosion.update(delta_time)

    def spawn_enemy(self):
        enemy = arcade.Sprite(ENEMY_TEXTURE_PATH, 0.5)
        enemy.center_x = random.uniform(0, SCREEN_WIDTH)
        enemy.center_y = SCREEN_HEIGHT + 20
        self.enemy_list.append(enemy)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_change_x = -5

        elif key == arcade.key.RIGHT:
            self.player_change_x = 5

        elif key == arcade.key.SPACE:
            self.shoot()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player_change_x = 0

    def shoot(self):
        if self.shoot_timer <= 0:
            bullet = arcade.Sprite(BULLET_TEXTURE_PATH, 0.5)
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            self.bullet_list.append(bullet)

            self.shoot_timer = self.shoot_cooldown

            if self.shoot_sound is not None:
                arcade.play_sound(self.shoot_sound)

            for _ in range(5):
                particle = Particle(
                    x=self.player_sprite.center_x,
                    y=self.player_sprite.center_y,
                    kind="shot"
                )
                self.particles.append(particle)

    def game_over(self):
        with open("results.txt", "a") as f:
            f.write(f"Вы набрали {self.score} очков.\n")
        final_view = FinalResultsView(self.score)
        self.window.show_view(final_view)



def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()