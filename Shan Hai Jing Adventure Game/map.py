import pygame

class Map:
    def __init__(self, tile_data):
        self.tiles = []  # 存储地图块
        self.load_tiles(tile_data)

    def load_tiles(self, tile_data):
        for (x, y, image_path) in tile_data:
            image = pygame.image.load(image_path)
            rect = image.get_rect(topleft=(x, y))
            self.tiles.append({"image": image, "rect": rect})

    def get_collision_tiles(self, player_rect):
        # 返回与玩家碰撞的地图块
        return [tile["rect"] for tile in self.tiles if player_rect.colliderect(tile["rect"])]

    def draw(self, screen):
        for tile in self.tiles:
            screen.blit(tile["image"], tile["rect"])

