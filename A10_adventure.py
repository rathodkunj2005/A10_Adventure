import sys
import pygame
from pygame.locals import *
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Define global variables to track game state
global current_level
current_level = 0  # 0 for start page, 1 for level 1, 2 for level 2 , 3 for level 3

# Define functions for each level
def level_1():
    import sys, pygame, math
    from pygame import Vector2

    global is_alive, key_found, game_objects, current_level
    mixer.music.load('images/l1.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)

    def pixel_collision(game_objects, item1, item2):
        """
            Given two game objects (by name), check if the non-transparent pixels of
            one mask contacts the non-transparent pixels of the other.

        :param game_objects: the dictionary of all items in the game
        :param item1 (string): the name of the first game object that is being compared to the second
        :param item2 (string): the name of the second game object
        :return: (boolean) True if they overlap
        """
        pos1 = game_objects[item1]["pos"]
        pos2 = game_objects[item2]["pos"]
        mask1 = game_objects[item1]["mask"]
        mask2 = game_objects[item2]["mask"]

        # shift images back to 0,0 for collision detection
        pos1_temp = pos1 - Vector2(mask1.get_size()) / 2
        pos2_temp = pos2 - Vector2(mask2.get_size()) / 2
        offset = pos2_temp - pos1_temp

        # See if the two masks at the offset are overlapping.
        overlap = mask1.overlap(mask2, offset)
        return overlap != None

    def draw_marker(screen, position):
        """
        Simple helper to draw a location on the screen so you can
        see if your thoughts of what a position match Python's "thoughts".
        :param screen:  surface you are drawing on
        :param position: Vector2 : location to draw a circle
        :return: -NA-
        """
        pygame.draw.circle(screen, "black", position, 5)

    def create_button(screen, message, x, y, width, height, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(screen, active_color, (x, y, width, height))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, inactive_color, (x, y, width, height))

        small_text = pygame.font.SysFont("times new roman", 25)
        text_surf = small_text.render(message, True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = ((x + (width / 2)), (y + (height / 2)))
        screen.blit(text_surf, text_rect)

    def draw_image_centered(screen, image, pos):
        """
        On the screen, draw the given image **centered** on the given position.

        :param screen:  what we are drawing on
        :param image:   what we are drawing
        :param pos: Vector2 :  where to center the image
        :return: -NA-
        """

        containing_rectangle = image.get_rect()
        screen.blit(image, (pos.x - containing_rectangle.width / 2, pos.y - containing_rectangle.height / 2))

    def add_game_object(game_objects, name, width, height, x, y):
        """
        Create and add a new game object (based on the provided params) to the game_objects dictionary.

        :param game_objects: dictionary of all objects in the game
        :param name:    the name of the object AND the image file
        :param width:   how wide to make the object/image in the game
        :param height:  how tall to make the object/image in the game
        :param x:       where in the game the object is
        :param y:       where in the game the object is
        :return: -NA-  The game_objects dictionary will have the new object inserted based on the name
        """
        information = {}
        game_objects[name] = information  # put the new object in the dictionary

        # Read the image file name. Note: I have put all of my images in a subfolder named "images"
        image = pygame.image.load("images/" + name + ".png")  # .convert_alpha()

        information["name"] = name
        information["pos"] = Vector2(x, y)
        information["image"] = pygame.transform.smoothscale(image, (width, height))
        information["mask"] = pygame.mask.from_surface(information["image"])
        information["visible"] = True
        information["solid"] = True

        # Note: this code does not support animations.  If you want animations (and you should)
        #       you will need to update it based on the lab code!

    def restart_game():
        global is_alive, key_found, game_objects
        is_alive = True
        key_found = False
        # Reset other game states as needed
        game_objects["astro"]["pos"] = Vector2(200, 400)  # Reset Astro's position
        game_objects["orb"]["visible"] = True  # Make the orb visible again
        # Add any other game elements that need to be reset

    def main():
        global current_level
        # Initialize pygame
        pygame.init()
        global is_alive, key_found, game_objects

        # Set up the Level by placing the objects of interest
        game_objects = {}

        #
        # Create the Game Objects and add them to the game_objects dictionary
        #
        # IMPORTANT: You must replace these images with your own.
        # IMPORTANT: the image file name is the name used for the item
        add_game_object(game_objects, "map_background_hd", 800 * 2, 600 * 1.5, 400 * 2, 300 * 1.5)
        add_game_object(game_objects, "map_1", 800 * 2, 600 * 1.5, 400 * 2, 300 * 1.5)
        add_game_object(game_objects, "astro", 50, 50, 200, 400)
        add_game_object(game_objects, "orb", 80 * 1.5, 80 * 1.5, 620 * 2, 100 * 1.5)
        add_game_object(game_objects, "door_1", 100, 100, 700, 190)
        add_game_object(game_objects, "door_2", 100, 100, 1125, 190)
        add_game_object(game_objects, "door_3", 100, 100, 415, 410)

        add_game_object(game_objects, "level1_end", 100, 100, 550, 400)

        # create the window based on the map size
        screen = pygame.display.set_mode(game_objects["map_1"]["image"].get_size())

        # The frame count records how many times the program has
        # gone through the main loop.  Normally you don't need this information
        # but if you want to do an animation, you can use this variable to
        # indicate which sprite frame to draw
        frame_count = 0

        # Get a font to use to write on the screen.
        myfont = pygame.font.SysFont('times new roman', 30)

        # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
        is_alive = True

        # "start" the game when the mouse moves over the player
        is_started = False

        # has the player found (moved on top of) the key to the door?
        key_found = False

        # check if player has completed the level
        level_1 = False

        cheat = True  # <----------------------------------------------------------------------   CHEAT MODE KEY

        # This is the main game loop. In it, we must:
        # - check for events
        # - update the scene
        # - draw the scene
        astro_image = pygame.image.load("images/astro.png").convert_alpha()  # Load and convert the image
        astro_image = pygame.transform.smoothscale(astro_image, (50, 50))  # Scale the image
        astro_flipped = pygame.transform.flip(astro_image, True, False)  # Flip the scaled image

        running = True
        vol_keys = pygame.key.get_pressed()
        while running and current_level == 1:
            if vol_keys[pygame.K_p]:
                mixer.music.pause()
            elif vol_keys[pygame.K_u]:
                mixer.music.unpause()
            elif vol_keys[pygame.K_s]:
                mixer.music.stop()
                break

            if cheat:
                is_alive = True

            # Check events by looping over the list of events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Position the player to the mouse location
            if is_alive:
                if is_started:
                    player = game_objects["astro"]
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        player["image"] = astro_flipped  # Use the flipped image when moving left
                        player["pos"] += Vector2(-5, 0)
                    elif keys[pygame.K_RIGHT]:
                        player["image"] = astro_image  # Use the original image when moving right
                        player["pos"] += Vector2(5, 0)
                    elif keys[pygame.K_UP]:
                        player["pos"] += Vector2(0, -5)
                    elif keys[pygame.K_DOWN]:
                        player["pos"] += Vector2(0, 5)

                else:
                    # if the mouse comes near the player, start the game
                    if Vector2(pygame.mouse.get_pos()).distance_to(game_objects["astro"]["pos"]) < 5:
                        is_started = True

            if not key_found:
                game_objects["level1_end"]["visible"] = False
            # Check for game logic situation
            if not key_found and pixel_collision(game_objects, "astro", "orb"):
                game_objects["orb"]["visible"] = False
                key_found = True
                game_objects["level1_end"]["visible"] = True
                # if pixel_collision(game_objects, "astro", "level1_end"):
                #     label = myfont.render("Level completed", True, (0, 0, 0))
                #     screen.blit(label, (20, 40))

            # Draw the game objects
            for object in game_objects.values():
                if object["visible"]:
                    draw_image_centered(screen, object["image"], object["pos"])

            # See if we touch the maze walls
            if pixel_collision(game_objects, "astro", "map_1"):
                label = myfont.render("Astro Collided inside the ship!", True, (0, 0, 0))
                screen.blit(label, (20, 80))
                is_alive = False
                pygame.mouse.set_visible(True)

                # checks if we collide with door
            if pixel_collision(game_objects, "astro", "door_1") or pixel_collision(game_objects, "astro",
                                                                                   "door_2") or pixel_collision(
                    game_objects, "astro", "door_3"):
                if game_objects["door_1"]["visible"] == True or game_objects["door_2"]["visible"] == True or \
                        game_objects["door_3"]["visible"] == True:
                    label = myfont.render("Astro Collided with the door", True, (0, 0, 0))
                    screen.blit(label, (20, 70))
                    game_objects["astro"]["pos"] -= Vector2(100, 0)
                    if key_found:
                        game_won = True
                        game_objects["door_1"]["visible"] = False
                        game_objects["door_2"]["visible"] = False
                        game_objects["door_3"]["visible"] = False
            if pixel_collision(game_objects, "astro", "level1_end"):
                level_1 = False
                label = myfont.render("LEVEL 1 COMPLETED", True, (20, 20, 20))
                screen.blit(label, (60, 50))
                game_objects["level1_end"]["visible"] = False
                current_level = 2  # Transition to Level 2
                return

            # # If you need to debug where something is on the screen, you can draw it
            # # using this helper method
            # draw_marker( screen, Vector2(550,350) )

            # Write some text to the screen. You can do something like this to show some hints or whatever you want.
            label = myfont.render("By Kunj rathod and Arsh khan !", True, (0, 0, 0))
            screen.blit(label, (20, 20))

            label = myfont.render("Put cursor on Astro to start", True, (0, 0, 0))
            screen.blit(label, (20, 50))

            # Every time through the loop, increase the frame count.
            frame_count += 1
            if not is_alive:  # If the game has ended
                create_button(screen, "Restart", 120, 120, 100, 50, (150, 150, 150), (200, 200, 200), restart_game)
            # Bring drawn changes to the front
            pygame.display.flip()

            # This slows down the code so it doesn't run more than 30 frames per second
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

    # Start the program
    main()
def level_2():
    import sys, pygame, math
    from pygame import Vector2
    global is_alive, key_found, game_objects, level_2
    from pygame import mixer

    # Initialize Pygame
    pygame.init()
    mixer.init()
    mixer.music.load('images/l2.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)

    def pixel_collision(game_objects, item1, item2):
        """
            Given two game objects (by name), check if the non-transparent pixels of
            one mask contacts the non-transparent pixels of the other.

        :param game_objects: the dictionary of all items in the game
        :param item1 (string): the name of the first game object that is being compared to the second
        :param item2 (string): the name of the second game object
        :return: (boolean) True if they overlap
        """
        pos1 = game_objects[item1]["pos"]
        pos2 = game_objects[item2]["pos"]
        mask1 = game_objects[item1]["mask"]
        mask2 = game_objects[item2]["mask"]

        # shift images back to 0,0 for collision detection
        pos1_temp = pos1 - Vector2(mask1.get_size()) / 2
        pos2_temp = pos2 - Vector2(mask2.get_size()) / 2
        offset = pos2_temp - pos1_temp

        # See if the two masks at the offset are overlapping.
        overlap = mask1.overlap(mask2, offset)
        return overlap != None

    def draw_marker(screen, position):
        """
        Simple helper to draw a location on the screen so you can
        see if your thoughts of what a position match Python's "thoughts".
        :param screen:  surface you are drawing on
        :param position: Vector2 : location to draw a circle
        :return: -NA-
        """
        pygame.draw.circle(screen, "black", position, 5)

    def create_button(screen, message, x, y, width, height, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(screen, active_color, (x, y, width, height))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, inactive_color, (x, y, width, height))

        small_text = pygame.font.SysFont("times new roman", 25)
        text_surf = small_text.render(message, True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = ((x + (width / 2)), (y + (height / 2)))
        screen.blit(text_surf, text_rect)

    def draw_image_centered(screen, image, pos):
        """
        On the screen, draw the given image **centered** on the given position.

        :param screen:  what we are drawing on
        :param image:   what we are drawing
        :param pos: Vector2 :  where to center the image
        :return: -NA-
        """

        containing_rectangle = image.get_rect()
        screen.blit(image, (pos.x - containing_rectangle.width / 2, pos.y - containing_rectangle.height / 2))

    def add_game_object(game_objects, name, width, height, x, y):
        """
        Create and add a new game object (based on the provided params) to the game_objects dictionary.

        :param game_objects: dictionary of all objects in the game
        :param name:    the name of the object AND the image file
        :param width:   how wide to make the object/image in the game
        :param height:  how tall to make the object/image in the game
        :param x:       where in the game the object is
        :param y:       where in the game the object is
        :return: -NA-  The game_objects dictionary will have the new object inserted based on the name
        """
        information = {}
        game_objects[name] = information  # put the new object in the dictionary

        # Read the image file name. Note: I have put all of my images in a subfolder named "images"
        image = pygame.image.load("images/" + name + ".png")  # .convert_alpha()

        information["name"] = name
        information["pos"] = Vector2(x, y)
        information["image"] = pygame.transform.smoothscale(image, (width, height))
        information["mask"] = pygame.mask.from_surface(information["image"])
        information["visible"] = True

        # Note: this code does not support animations.  If you want animations (and you should)
        #       you will need to update it based on the lab code!

    def restart_game():
        global is_alive, key_found, game_objects
        is_alive = True
        key_found = False
        # Reset other game states as needed
        game_objects["astro"]["pos"] = Vector2(450, 450)  # Reset Astro's position
        game_objects["orb"]["visible"] = True  # Make the orb visible again
        # Add any other game elements that need to be reset

    def move_droid_y(game_objects, droid_name, min_y, max_y, droid_speed):
        """
        Move the droid up and down between the min_y and max_y bounds.
        :param game_objects: dictionary of all objects in the game
        :param droid_name: the name of the droid in the game_objects dictionary
        :param min_y: the minimum y boundary
        :param max_y: the maximum y boundary
        """
        droid = game_objects[droid_name]
        # If 'direction' key is not present in the droid's dictionary, initialize it
        if 'direction' not in droid:
            droid['direction'] = 1  # Set initial direction to downwards

        # Move droid along the y-axis
        droid["pos"].y += droid_speed * droid['direction']

        # Change direction if the droid hits the top or bottom boundary
        if droid["pos"].y <= min_y or droid["pos"].y >= max_y:
            droid['direction'] *= -1  # Reverse direction

    def move_droid_x(game_objects, droid_name, min_x, max_x, droid_speed):
        """
        Move the droid up and down between the min_y and max_y bounds.
        :param game_objects: dictionary of all objects in the game
        :param droid_name: the name of the droid in the game_objects dictionary
        :param min_x: the minimum x boundary
        :param max_x: the maximum x boundary
        """
        droid = game_objects[droid_name]
        # If 'direction' key is not present in the droid's dictionary, initialize it
        if 'direction' not in droid:
            droid['direction'] = 1  # Set initial direction to downwards

        # Move droid along the y-axis
        droid["pos"].x += droid_speed * droid['direction']

        # Change direction if the droid hits the top or bottom boundary
        if droid["pos"].x <= min_x or droid["pos"].x >= max_x:
            droid['direction'] *= -1  # Reverse direction

    def main():
        # Initialize pygame
        pygame.init()
        global is_alive, key_found, game_objects

        # Set up the Level by placing the objects of interest
        game_objects = {}

        #
        # Create the Game Objects and add them to the game_objects dictionary
        #
        # IMPORTANT: You must replace these images with your own.
        # IMPORTANT: the image file name is the name used for the item
        add_game_object(game_objects, "map2", 800 * 2, 600 * 1.5, 400 * 2, 300 * 1.5)
        add_game_object(game_objects, "map2_bg", 800 * 2, 600 * 1.5, 400 * 2, 300 * 1.5)
        add_game_object(game_objects, "astro", 50, 50, 450, 450)
        add_game_object(game_objects, "droid1", 100, 100, 590, 100)
        add_game_object(game_objects, "droid2", 100, 100, 780, 100)
        add_game_object(game_objects, "droid3", 100, 100, 1030, 100)
        add_game_object(game_objects, "droid1x", 100, 100, 1030, 400)
        add_game_object(game_objects, "orb", 80 * 1.5, 80 * 1.5, 620 * 2, 300 * 1.5)

        add_game_object(game_objects, "level2_end", 100, 100, 500, 400)

        # create the window based on the map size
        screen = pygame.display.set_mode(game_objects["map2"]["image"].get_size())

        # The frame count records how many times the program has
        # gone through the main loop.  Normally you don't need this information
        # but if you want to do an animation, you can use this variable to
        # indicate which sprite frame to draw
        frame_count = 0

        # Get a font to use to write on the screen.
        myfont = pygame.font.SysFont('times new roman', 30)

        # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
        is_alive = True

        # "start" the game when the mouse moves over the player
        is_started = False

        # has the player found (moved on top of) the key to the door?
        key_found = False

        # check if player has completed the level
        level_2 = False

        cheat = True  # <----------------------------------------------------------------------   CHEAT MODE KEY

        # Define vertical bounds for droid movement based on your game's map layout
        min_y = 100  # Minimum y position
        max_y = 800  # Maximum y position
        min_x = 400  # Minimum X position
        max_x = 1200  # Maximum X position

        # This is the main game loop. In it, we must:
        # - check for events
        # - update the scene
        # - draw the scene
        while True:
            move_droid_y(game_objects, "droid1", min_y, max_y, 10)
            move_droid_y(game_objects, "droid2", min_y, max_y, 20)
            move_droid_y(game_objects, "droid3", min_y, max_y, 30)
            move_droid_x(game_objects, "droid1x", min_x, max_x, 10)

            # Check for collision with Astro
            if (pixel_collision(game_objects, "astro", "droid1")
                    or pixel_collision(game_objects, "astro", "droid2")
                    or pixel_collision(game_objects, "astro", "droid3")
                    or pixel_collision(game_objects, "astro", "droid1x")):
                is_alive = False  # End the game if Astro collides with the droid

            if cheat:
                is_alive = True

            # Check events by looping over the list of events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Position the player to the mouse location
            if is_alive:
                if is_started:
                    level_2 = True
                    player = game_objects["astro"]
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        player["pos"] += Vector2(-5, 0)
                    if keys[pygame.K_RIGHT]:
                        player["pos"] += Vector2(5, 0)
                    if keys[pygame.K_UP]:
                        player["pos"] += Vector2(0, -5)
                    if keys[pygame.K_DOWN]:
                        player["pos"] += Vector2(0, 5)

                else:
                    # if the mouse comes near the player, start the game
                    if Vector2(pygame.mouse.get_pos()).distance_to(game_objects["astro"]["pos"]) < 5:
                        is_started = True

            if not key_found:
                game_objects["level2_end"]["visible"] = False
            # Check for game logic situation
            if not key_found and pixel_collision(game_objects, "astro", "orb"):
                game_objects["orb"]["visible"] = False
                key_found = True
                game_objects["level2_end"]["visible"] = True
                # if pixel_collision(game_objects, "astro", "level1_end"):
                #     label = myfont.render("Level completed", True, (0, 0, 0))
                #     screen.blit(label, (20, 40))

            # Draw the game objects
            for object in game_objects.values():
                if object["visible"]:
                    draw_image_centered(screen, object["image"], object["pos"])

            # See if we touch the maze walls
            if pixel_collision(game_objects, "astro", "map2"):
                label = myfont.render("Astro Collided inside the ship!", True, (0, 0, 0))
                screen.blit(label, (20, 80))
                is_alive = False
                pygame.mouse.set_visible(True)

            # # If you need to debug where something is on the screen, you can draw it
            # # using this helper method
            # draw_marker( screen, Vector2(550,350) )
            if pixel_collision(game_objects, "astro", "level2_end"):
                level_2 = False
                label = myfont.render("LEVEL 2 COMPLETED", True, (20, 20, 20))
                screen.blit(label, (100, 100))
                game_objects["level2_end"]["visible"] = False

            # Write some text to the screen. You can do something like this to show some hints or whatever you want.
            label = myfont.render("By Kunj rathod and Arsh khan !", True, (0, 0, 0))
            screen.blit(label, (20, 20))

            label = myfont.render("Put cursor on Astro to start", True, (0, 0, 0))
            screen.blit(label, (20, 50))

            # Every time through the loop, increase the frame count.
            frame_count += 1
            if not is_alive:  # If the game has ended
                create_button(screen, "Restart", 120, 120, 100, 50, (150, 150, 150), (200, 200, 200), restart_game)

            # Bring drawn changes to the front
            pygame.display.flip()

            # This slows down the code so it doesn't run more than 30 frames per second
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

    # Start the program
    main()


def start_page():
    global current_level

    # Set up display
    screen = pygame.display.set_mode((1600, 900))  # Set to your desired resolution
    pygame.display.set_caption('Astro\'s Adventures')

    # Load background image for the start page
    background_image = pygame.image.load('images/starting_page.png')  # Replace with your image path

    # Set up the button text
    font = pygame.font.Font(None, 36)
    text = font.render('Start', True, (0, 0, 0), (0, 255, 0))
    text_rect = text.get_rect()
    text_rect.center = (400, 300)  # Center of the screen or where you want it
    myfont = pygame.font.SysFont('times new roman', 30)
    label = myfont.render("Astro\'s Adventure", True, (0, 0, 0))
    screen.blit(label, (20, 20))
    label = myfont.render("By Kunj rathod and Arsh khan !", True, (0, 0, 0))
    screen.blit(label, (20, 20))

    running = True
    while running and current_level == 0:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    current_level = 1  # Start Level 1
                    running = False

        pygame.draw.rect(screen, (0, 255, 0), text_rect)  # Draw button
        screen.blit(text, text_rect)  # Draw text

        pygame.display.update()

# Main game loop
while True:
    # Main game loop
    while True:
        if current_level == 0:
            start_page()
        elif current_level == 1:
            level_1()
        elif current_level == 2:
            level_2()

# Properly quit Pygame
pygame.quit()
