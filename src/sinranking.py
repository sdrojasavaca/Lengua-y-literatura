import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 50)
SMALL_FONT = pygame.font.Font(None, 30)

# Cargar recursos
def load_resources():
    resources = {
        "background_menu": pygame.image.load("resources/images/fondo_menu.jpg"),
        "background_game": pygame.image.load("resources/images/fondo.jpg"),
        "dogs": {
            "dog1": {
                "image": pygame.image.load("resources/images/dog1.png"),
                "sound_bark": pygame.mixer.Sound("resources/sounds/dog1_ladrido.ogg"),
                "sound_hurt": pygame.mixer.Sound("resources/sounds/dog1_herido.ogg")
            },
            "dog2": {
                "image": pygame.image.load("resources/images/dog2.png"),
                "sound_bark": pygame.mixer.Sound("resources/sounds/dog2_ladrido.ogg"),
                "sound_hurt": pygame.mixer.Sound("resources/sounds/dog2_herido.ogg")
            },
            "dog3": {
                "image": pygame.image.load("resources/images/dog3.png"),
                "sound_bark": pygame.mixer.Sound("resources/sounds/dog3_ladrido.ogg"),
                "sound_hurt": pygame.mixer.Sound("resources/sounds/dog3_herido.ogg")
            }
        },
        "hueso_normal": pygame.image.load("resources/images/hueso_normal.png"),
        "hueso_chocolate": pygame.image.load("resources/images/hueso_chocolate.png"),
        "hueso_dorado": pygame.image.load("resources/images/hueso_dorado.png"),
        "sound_death": pygame.mixer.Sound("resources/sounds/dog_muerte.ogg"),
    }
    return resources

resources = load_resources()

# Clase Dog
class Dog(pygame.sprite.Sprite):
    def __init__(self, image, sound_bark, sound_hurt, speed, lives):
        super().__init__()
        self.original_image = image  # Guardar la imagen original
        self.image = self.original_image
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))
        self.sound_bark = sound_bark
        self.sound_hurt = sound_hurt
        self.speed = speed  # Velocidad específica para cada perro
        self.lives = lives  # Vidas específicas para cada perro
        self.score = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.image = pygame.transform.flip(self.original_image, True, False)  # Voltear imagen horizontalmente
        elif keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.image = self.original_image  # Restaurar imagen original

    def play_sound(self, sound):
        sound.play()
# Clase Bone
class Bone(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type):
        super().__init__()
        # Obtener el tamaño original de la imagen
        original_width, original_height = image.get_size()
        
        # Calcular el nuevo tamaño (por ejemplo, reducir el tamaño a un 50%)
        scale_factor = 0.5  # Cambia este valor para ajustar el tamaño
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # Escalar la imagen del hueso manteniendo la relación de aspecto
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = type  # normal, chocolate, dorado
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Clase principal Game
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dog Adventure Juego")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        self.selected_dog_key = None
        self.selected_dog = None
        self.all_sprites = pygame.sprite.Group()
        self.bones = pygame.sprite.Group()  # Grupo para los huesos
        self.create_bones()  # Crear huesos al inicio del juego

    def main_menu(self):
        while self.state == "menu":
            self.screen.blit(resources["background_menu"], (0, 0))
            self.display_text("Dog Adventure Juego", FONT, WHITE, SCREEN_WIDTH // 2, 100)
            self.display_text("Press Enter to Start", FONT, WHITE, SCREEN_WIDTH // 2, 200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = "select_dog"
            pygame.display.flip()

    def select_dog(self):
        while self.state == "select_dog":
            self.screen.blit(resources["background_menu"], (0, 0))
            self.display_text("Select Your Dog", FONT, WHITE, SCREEN_WIDTH // 2, 50)

            # Dimensiones y posiciones
            dog_width, dog_height = resources["dogs"]["dog1"]["image"].get_size()
            spacing = 100  # Espacio entre los perros
            start_x = (SCREEN_WIDTH - (3 * dog_width + 2 * spacing)) // 2  # Centrado en la pantalla

            # Mostrar perros
            for index, dog_key in enumerate(["dog1", "dog2", "dog3"]):
                dog_image = resources["dogs"][dog_key]["image"]
                dog_x = start_x + index * (dog_width + spacing)
                dog_y = 150

                # Fondo blanco transparente
                card_color = (255, 255, 255, 150)  # Cambia 150 a un valor menor para más transparencia
                pygame.draw.rect(self.screen, card_color, (dog_x - 10, dog_y - 10, dog_width + 20, dog_height + 120), border_radius=10)

                # Dibujar perro centrado en la tarjeta
                self.screen.blit(dog_image, (dog_x + 10, dog_y + 10))  # Ajustar +10 para centrar

                # Obtener velocidad, vidas máximas y nombre
                speed = 4 if dog_key == "dog1" else 5 if dog_key == "dog2" else 7
                lives = 5 if dog_key == "dog1" else 4 if dog_key == "dog2" else 3
                dog_name = "Hambriento" if dog_key == "dog1" else "Angurriento" if dog_key == "dog2" else "Apetetito"

                # Mostrar texto de nombre, velocidad y vidas
                self.display_text(dog_name, SMALL_FONT, BLACK, dog_x + dog_width // 2, dog_y + dog_height + 20)
                self.display_text(f"Speed: {speed}", SMALL_FONT, BLACK, dog_x + dog_width // 2, dog_y + dog_height + 40)
                self.display_text(f"Lives: {lives}", SMALL_FONT, BLACK, dog_x + dog_width // 2, dog_y + dog_height + 60)

                # Texto encima de la tarjeta
                self.display_text(f"Press {index + 1} for {dog_name}", SMALL_FONT, BLACK, dog_x + dog_width // 2, dog_y - 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.selected_dog_key = "dog1"
                        self.state = "play"
                    elif event.key == pygame.K_2:
                        self.selected_dog_key = "dog2"
                        self.state = "play"
                    elif event.key == pygame.K_3:
                        self.selected_dog_key = "dog3"
                        self.state = "play"
            pygame.display.flip()

    
    def create_bones(self):
        self.bones.empty()  # Eliminar todos los huesos existentes
        for _ in range(5):  # Cambia el número según cuántos huesos quieras
            # Crear un nuevo hueso en una posición aleatoria en la parte superior
            type = random.choice(["normal", "chocolate", "dorado"])  # Elegir tipo de hueso aleatoriamente
            image = resources[f"hueso_{type}"]
            bone = Bone(image, random.randint(0, SCREEN_WIDTH - 50), -50, type)  # Aparece en la parte superior
            self.bones.add(bone)

    def play(self):
        dog_data = resources["dogs"][self.selected_dog_key]
        
        # Definir diferentes velocidades y vidas para cada perro
        if self.selected_dog_key == "dog1":
            speed = 4
            lives = 5
        elif self.selected_dog_key == "dog2":
            speed = 7
            lives = 4
        elif self.selected_dog_key == "dog3":
            speed = 10
            lives = 2

        self.selected_dog = Dog(dog_data["image"], dog_data["sound_bark"], dog_data["sound_hurt"], speed, lives)
        self.all_sprites.add(self.selected_dog)
        
        # Frecuencias de aparición de cada tipo de hueso
        prob_normal = 0.045   # 4.5% para hueso normal
        prob_chocolate = 0.04  # 4% para hueso chocolate
        prob_dorado = 0.005  # 0.5% para hueso dorado

        while self.state == "play":
            self.screen.blit(resources["background_game"], (0, 0))
            keys = pygame.key.get_pressed()
            self.selected_dog.move(keys)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Generar huesos y manejar colisiones
            if random.random() < (prob_normal + prob_chocolate + prob_dorado):
                type = random.choices(
                    ["normal", "chocolate", "dorado"],
                    weights=[prob_normal, prob_chocolate, prob_dorado],
                    k=1
                )[0]
                image = resources[f"hueso_{type}"]
                bone = Bone(image, random.randint(0, SCREEN_WIDTH - 50), -50, type)  # Aumenta el valor de -50 a -100
                self.all_sprites.add(bone)
                self.bones.add(bone)

            hits = pygame.sprite.spritecollide(self.selected_dog, self.bones, True)
            for hit in hits:
                if hit.type == "normal":
                    self.selected_dog.score += 1
                    self.selected_dog.play_sound(self.selected_dog.sound_bark)
                elif hit.type == "chocolate":
                    self.selected_dog.lives -= 1
                    self.selected_dog.play_sound(self.selected_dog.sound_hurt)
                    if self.selected_dog.lives <= 0:
                        resources["sound_death"].play()
                        self.all_sprites.remove(self.selected_dog)  # Eliminar el perro
                        self.bones.empty()  # Eliminar todos los huesos
                        self.create_bones()  # Crear nuevos huesos en la parte superior
                        self.state = "menu"  # Volver al menú
                elif hit.type == "dorado":
                    self.selected_dog.score += 5
                    self.selected_dog.play_sound(self.selected_dog.sound_bark)

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            # Mostrar puntaje y vidas
            self.display_text(f"Score: {self.selected_dog.score}", SMALL_FONT, WHITE, 100, 20)
            self.display_text(f"Lives: {self.selected_dog.lives}", SMALL_FONT, RED, 700, 20)

            pygame.display.flip()
            self.clock.tick(FPS)

    def display_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        
# Main Execution
if __name__ == "__main__":
    game = Game()
    while game.running:
        if game.state == "menu":
            game.main_menu()
        elif game.state == "select_dog":
            game.select_dog()
        elif game.state == "play":
            game.play()
