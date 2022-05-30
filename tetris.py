# Import libaries
import pygame
import random

# Initialize pygame, a libary used to create games
pygame.init()

# A dict of all the tetromino shapes in the following format:
# type: (
#   area,
#   [
#    rects inside area
#   ],
#   color
# )
tetromino_shapes = {
    'I': (
        (4, 1),
        [
            (0, 0, 4, 1)
        ],
        (0, 255, 255)
    ),
    'S': (
        (3, 2),
        [
            (1, 0, 2, 1),
            (0, 1, 2, 3)
        ],
        (0, 255, 0)
    ),
    'Z': (
        (3, 2),
        [
            (0, 0, 2, 1),
            (1, 1, 2, 3)
        ],
        (255, 0, 0)
    ),
    'O': (
        (2, 2),
        [
            (0, 0, 2, 2)
        ],
        (255, 255, 0)
    ),
    'T': (
        (3, 2),
        [
            (0, 0, 3, 1),
            (1, 1, 1, 1)
        ],
        (255, 0, 255)
    ),
    'L': (
        (2, 3),
        [
            (0, 0, 1, 3),
            (1, 2, 2, 1),
        ],
        (255, 165, 0)
    ),
    'J': (
        (2, 3),
        [
            (1, 0, 1, 3),
            (0, 2, 2, 1),
        ],
        (0, 0, 255)
    )
}

# Define the scale of the tetrominos
scale = 10

# Make a screen 10 blocks by 20 blocks with the title 'Tetris' on the top
screen = pygame.display.set_mode((10 * scale, 20 * scale))
pygame.display.set_caption('Tetris')

# Fill the screen white
screen.fill((255, 255, 255))
pygame.display.flip()

# Define a sprite that represents the fallen tetrominoes and a group that
# contains that sprite so it can be used for collision
tetrominoes = None
tetrominoes_group = pygame.sprite.Group()

# Define the clock, which is used to maintain the frame rate
clock = pygame.time.Clock()

# Set the falling event to go off every 200 miliseconds
fall_speed = 200
pygame.time.set_timer(pygame.USEREVENT, fall_speed)

# Define the sprite current_tetromino and its type and height
current_tetromino = None
tetromino_type = None
height = 0

# Define a function that creats new tetrominos
def new_tetromino():
    global current_tetromino, x, y, height, tetromino_type

    # Pick a random tetromino
    tetromino_type = random.choice(list(tetromino_shapes.keys()))
    tetromino = tetromino_shapes[tetromino_type]

    # Create the new tetromino and change the height and type variable
    area = (tetromino[0][0] * scale, tetromino[0][1] * scale)
    height = area[1]
    surface = pygame.Surface(area, pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    for rect in tetromino[1]:
        scaled_rect = tuple(i * scale for i in rect)
        surface.fill(tetromino[2], scaled_rect)

    # Apply changes to the new tetromino
    current_tetromino = pygame.sprite.Sprite()
    current_tetromino.image = surface
    current_tetromino.rect = current_tetromino.image.get_rect()

    # Reset its position
    current_tetromino.rect.x = screen.get_width() // 2 - scale
    current_tetromino.rect.y = 0

new_tetromino()

# Create a loop that stops when the variable running is false
running = True
while running:
    for event in pygame.event.get():
        # Stop running when the x button is clicked
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Stop running when the escape key is clicked
            if event.key == pygame.K_ESCAPE:
                running = False

            # Move the tetromino with the arrow keys and space bar
            if event.key == pygame.K_UP:
                rotated = pygame.transform.rotate(current_tetromino.image, 90)
                rotated.get_rect().center = current_tetromino.rect.center
                current_tetromino.image = rotated                
                height = current_tetromino.image.get_height()        

            if event.key == pygame.K_DOWN:
                current_tetromino.rect.y += scale

            if event.key == pygame.K_LEFT:
                if current_tetromino.rect.x != 0:
                    current_tetromino.rect.x -= scale

            if event.key == pygame.K_RIGHT:
                if current_tetromino.image.get_width() == 3:
                    if current_tetromino.rect.x + current_tetromino.image.get_width() + scale != screen.get_width():
                            current_tetromino.rect.x += scale
                elif current_tetromino.rect.x + current_tetromino.image.get_width() != screen.get_width():
                    current_tetromino.rect.x += scale

            if event.key == pygame.K_SPACE:
                for i in range(0, 20):
                    current_tetromino.rect.y += scale
                    
                    if pygame.sprite.spritecollide(current_tetromino, tetrominoes_group, False, pygame.sprite.collide_mask):
                        current_tetromino.rect.y -= scale
                        break
                    if current_tetromino.rect.y > screen.get_height() - height - scale:
                        break

        # Decrease tetromino height when the event goes off
        if event.type == pygame.USEREVENT:
            current_tetromino.rect.y += scale

    # Update the tetrominoes sprite and group
    tetrominoes_group.remove(tetrominoes)
    if tetrominoes:
        old_tetrominoes = tetrominoes.image
        tetrominoes = pygame.sprite.Sprite()
        tetrominoes.image = old_tetrominoes
    else:
        tetrominoes = pygame.sprite.Sprite()
        tetrominoes.image = pygame.surface.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    tetrominoes.rect = tetrominoes.image.get_rect()

    # Loop through each block on the screen and keep track of each line
    lines = []
    filled_line = None
    for y in range(0, screen.get_height(), scale):
        line = []
        for x in range(0, screen.get_width(), scale):
            line.append(tetrominoes.image.get_at((x, y)))

        # If a line is filled set the current y to a variable so that all the
        # lines above can be shifted down
        if all(i != (0, 0, 0, 0) for i in line):
            filled_line = line

        # Quit game if the blocks stack up to the top
        if y == 0 and any(i != (0, 0, 0, 0) for i in line):
            running = False

        lines.append(line)

    # If a line is filled:
    if filled_line:
        # Shift all the lines above the filled line down one
        lines.remove(filled_line)
        lines.insert(0, [(0, 0, 0, 0)] * 10)

        # Update the tetrominoes sprite
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                tetrominoes.image.fill(lines[y][x], (x * scale,  y * scale, x * scale + scale, y * scale + scale))

    # Add the tetrominoes sprite to the group so it can be used for collision
    tetrominoes_group.add(tetrominoes)
    
    # If the tetromino has touched another tetronimo:
    if pygame.sprite.spritecollide(current_tetromino, tetrominoes_group, False, pygame.sprite.collide_mask):
        # Move the tetronimo so it is not overlapping
        current_tetromino.rect.y -= scale

        # Add the tetromino to the tetronimo surface so it can keep being
        # rendered
        #tetrominoes.add(current_tetromino)
        tetrominoes.image.blit(current_tetromino.image, current_tetromino.rect)  

        # Make a new tetromino
        new_tetromino()

    # If the tetromino has touched the bottom:
    if current_tetromino.rect.y > screen.get_height() - height - scale:
        # Add the tetromino to the tetronimo surface so it can keep being
        # rendered
        tetrominoes.image.blit(current_tetromino.image, current_tetromino.rect)  

        # Make a new tetromino
        new_tetromino()

    # Clear screen   
    screen.fill((255, 255, 255))

    # Render current tetromino
    screen.blit(current_tetromino.image, current_tetromino.rect)
    
    # Render other tetrominoes
    screen.blit(tetrominoes.image, (0, 0))

    # Update screen
    pygame.display.flip()

    # Delay to maintain 60 fps
    clock.tick(60)

pygame.quit()
