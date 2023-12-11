import sys

import pygame
from pygame import mixer
from pygame.locals import *

# Initialize Pygame
pygame.init()
mixer.init()

# Define global variables to track current level
global current_level
current_level = 0  # 0 for start page, 1 for level 1, 2 for level 2 , 3 for level 3 and 4 for end page


# Defining functions for each level
def level_1():

    '''Level 1 of this Pygame-based game sets the stage for
    an engaging adventure where the player controls a character named Astro. T
    he level unfolds in a richly detailed map (map_1), populated with diverse elements
    including the central character Astro, a crucial orb, multiple doors (door_1, door_2, door_3),
    and a designated endpoint (level1_end). The primary objective for the player is to maneuver Astro through the environment,
    steering clear of collisions with the doors while striving to reach and obtain the orb. Upon securing the orb, the endpoint materializes,
    signaling the player to navigate Astro to this spot to conclude the level. This level incorporates pixel-level
    collision detection for precise interactions between Astro, doors, and other game components. Notably,
    the game features the capability to flip Astro's image to reflect the direction of movement,
    adding a layer of realism to the gameplay. Additionally, a restart function is available to enhance replay value and challenge.
    Upon successful completion of Level 1, the game transitions the player to the next level, furthering the adventure.'''

    import sys, pygame
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
        Simple helper to draw a location on the screen, so you can
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

        # Read the image file name. Note: I have put all of my images in a sub-folder named "images"
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
        game_objects["astro"]["pos"] = Vector2(200, 400)  # Reset Astro's position
        game_objects["orb"]["visible"] = True  # Make the orb visible again

    def main():
        global current_level
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

        # This is the main game loop. In it, we must:
        # - check for events
        # - update the scene
        # - draw the scene
        astro_image = pygame.image.load("images/astro.png").convert_alpha()  # Load and convert the image
        astro_image = pygame.transform.smoothscale(astro_image, (50, 50))  # Scale the image
        astro_flipped = pygame.transform.flip(astro_image, True, False)  # Flip the scaled image

        running = True
        cheat_key = pygame.key.get_pressed()
        if cheat_key[pygame.K_c]:
            is_alive = True

        while running and current_level == 1:

            cheat_key = pygame.key.get_pressed()
            if cheat_key[pygame.K_c]:
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
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        is_started = True

            if not key_found:
                game_objects["level1_end"]["visible"] = False

            if not key_found and pixel_collision(game_objects, "astro", "orb"):
                game_objects["orb"]["visible"] = False
                key_found = True
                game_objects["level1_end"]["visible"] = True


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

            label = myfont.render("Press Space to start", True, (0, 0, 0))
            screen.blit(label, (20, 50))

            # Every time through the loop, increase the frame count.
            frame_count += 1
            if not is_alive:  # If the game has ended
                create_button(screen, "Restart", 120, 120, 100, 50, (150, 150, 150), (200, 200, 200), restart_game)
            # Bring drawn changes to the front
            pygame.display.flip()

            # This slows down the code, so it doesn't run more than 30 frames per second
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

    # Start the program
    main()


def level_2():
    '''Level 2 in this game, designed using Pygame,
    offers an intriguing and interactive experience
    where the player controls a character named Astro.
    Set in a detailed map (map2), the level features
    various game objects including moving droids
    (droid1, droid2, droid3, droid1x) that patrol
    the area, an orb that serves as a key, and a specific endpoint
    (level2_end) for level completion.
    The player's goal is to navigate Astro through the level,
    avoiding collisions with droids, which are dynamically moving in both vertical
    and horizontal directions, and reaching the orb. Upon collecting the orb,
    the endpoint becomes visible, signaling the player to guide Astro to this location
    to complete the level. The game incorporates
    pixel-level collision detection to ensure precise interactions between Astro,
    the droids, and other elements in the game. Additionally,
    there's an option to restart the game upon failure,
    enhancing the challenge and replayability of Level 2.'''
    import sys, pygame
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
        Simple helper to draw a location on the screen, so you can
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
        global is_alive, key_found, game_objects,current_level

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
        add_game_object(game_objects, "level2_end", 100, 100, 500, 250)

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
            cheat_key = pygame.key.get_pressed()
            if cheat_key[pygame.K_c]:
                is_alive = True
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

            # Check events by looping over the list of events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if is_alive:
                if is_started:
                    level_2 = True
                    player = game_objects["astro"]
                    keys = pygame.key.get_pressed()
                    cheat_key = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        player["pos"] += Vector2(-5, 0)
                    elif keys[pygame.K_RIGHT]:
                        player["pos"] += Vector2(5, 0)
                    elif keys[pygame.K_UP]:
                        player["pos"] += Vector2(0, -5)
                    elif keys[pygame.K_DOWN]:
                        player["pos"] += Vector2(0, 5)


                else:
                    # if the space button is pressed, start the game
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        is_started = True

            if not key_found:
                game_objects["level2_end"]["visible"] = False
            # Check for game logic situation
            if not key_found and pixel_collision(game_objects, "astro", "orb"):
                game_objects["orb"]["visible"] = False
                key_found = True
                game_objects["level2_end"]["visible"] = True


            # Draw the game objects
            for object in game_objects.values():
                if object["visible"]:
                    draw_image_centered(screen, object["image"], object["pos"])

            # See if we touch the walls
            if pixel_collision(game_objects, "astro", "map2"):
                label = myfont.render("Astro Collided inside the ship!", True, (0, 0, 0))
                screen.blit(label, (20, 80))
                is_alive = False
                pygame.mouse.set_visible(True)

            # # If you need to debug where something is on the screen, you can draw it
            # # using this helper method
            # draw_marker( screen, Vector2(550,350) )
            if pixel_collision(game_objects, "astro", "level2_end"):
                current_level=3
                label = myfont.render("LEVEL 2 COMPLETED", True, (20, 20, 20))
                screen.blit(label, (100, 100))
                game_objects["level2_end"]["visible"] = False
                return

            label = myfont.render("By Kunj rathod and Arsh khan !", True, (0, 0, 0))
            screen.blit(label, (20, 20))

            label = myfont.render("Press Space to start", True, (0, 0, 0))
            screen.blit(label, (20, 50))

            # Every time through the loop, increase the frame count.
            frame_count += 1
            if not is_alive:  # If the game has ended
                create_button(screen, "Restart", 120, 120, 100, 50, (150, 150, 150), (200, 200, 200), restart_game)

            # Bring drawn changes to the front
            pygame.display.flip()

            # This slows down the code, so it doesn't run more than 30 frames per second
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

    # Start the program
    main()


def level_3():
    """Level 3 of this Pygame-based game introduces a significant ramp-up in challenge and interactivity,
    offering a more complex and engaging gameplay experience. In this level, the player continues to control Astro,
    now set in a new and intricate map (map3), filled with a multitude of game elements including a formidable antagonist known as Evil,
    a series of ten crystals randomly placed throughout the level, and an advanced health system for both Astro and the villain.
    The key objective in Level 3 is for the player to navigate Astro through the level, strategically avoiding or confronting Evil,
    while simultaneously seeking out and collecting all ten crystals. The level features sophisticated mechanics such as an attack system,
    allowing Astro to engage in combat with Evil. The villain, on the other hand, is programmed with basic AI behaviors, actively pursuing
    and attacking Astro when within range. The health points of both characters are prominently displayed, adding a layer
    of strategy as players must balance offense and defense. Pixel-level collision detection plays a crucial role in this level,
    governing interactions between Astro, Evil, and the crystals. The gameplay is intensified through a dynamic collision
    system that affects the health of both Astro and Evil upon contact. Additionally, the level includes a crystal counter
    to track the player's progress in collecting crystals.The game environment is designed to be immersive,
    with a detailed map and background music that enhances the ambiance. Upon successful collection of all crystals,
    the player progresses to the next level, marking the completion of Level 3. This level, with its enhanced complexity
    and interactive elements, significantly ups the ante, providing a challenging yet rewarding experience for the player."""
    import random
    import sys, pygame
    from pygame import Vector2

    global is_alive, key_found, game_objects, collision_timer, astro_health, evil_health,current_level
    from pygame import mixer

    # Initialize Pygame
    pygame.init()
    mixer.init()
    mixer.music.load('images/l3.mp3')
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
        Simple helper to draw a location on the screen, so you can
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

    def attack(target, damage):
        if target['health'] > 0:
            target['health'] -= damage
            if target['health'] <= 0:
                target['state'] = 'defeated'

    def villain_behavior(villain, player):
        if villain['state'] != 'defeated':
            # Simple AI: move towards player and attack when close enough
            if villain['pos'].distance_to(player['pos']) < attack_range:
                attack(player, villain_damage)
            else:
                direction_vector = player['pos'] - villain['pos']
                villain['pos'] += direction_vector.normalize() * villain_speed

    global is_alive, key_found, game_objects, collision_timer, astro_health, evil_health

    attack_range = 100  # The range within which the villain will attack
    villain_damage = 20  # The damage the villain's attack does to the player
    player_damage = 20 # The damage the astro's attack does to the player
    villain_speed = 5  # The speed at which the villain moves towards the player

    # Initialize the health and state of the characters
    def display_health(screen, font, astro_health, evil_health, astro_pos, evil_pos):
        # Render the health text
        astro_health_text = font.render(f'Astro Health: {astro_health}', True, (0, 0, 255))
        evil_health_text = font.render(f'Evil Health: {evil_health}', True, (255, 0, 0))

        # Position the text on the screen
        astro_health_pos = (astro_pos.x - 50, astro_pos.y - 120)
        evil_health_pos = (evil_pos.x - 50, evil_pos.y - 120)

        # Draw the health text onto the screen
        screen.blit(astro_health_text, astro_health_pos)
        screen.blit(evil_health_text, evil_health_pos)

    # Initialize the font
    font = pygame.font.SysFont('Arial', 18)

    # Initialize the health for Astro and Evil
    astro_health = 100
    evil_health = 100

    def restart_game():
        global is_alive, key_found, game_objects, collision_timer, astro_health, evil_health
        is_alive = True
        key_found = False
        # Reset other game states as needed
        game_objects["astro3"]["pos"] = Vector2(450, 450)  # Reset Astro's position

    collision_timer = None

    # Function to handle collision and reduce health
    def handle_collision(game_objects, collision_timer, astro_health, evil_health):
        if pixel_collision(game_objects, "astro3", "evil"):
            current_time = pygame.time.get_ticks()

            # Start the timer if not already started
            if collision_timer is None:
                collision_timer = current_time

            # Check if 0.5 seconds have passed since they first collided
            if current_time - collision_timer >= 500:
                astro_health -= 7
                evil_health -= 7
                collision_timer = current_time  # Reset the timer

        else:
            collision_timer = None  # Reset the timer if they are not colliding

        return astro_health, evil_health, collision_timer

    def main():
        # Initialize pygame
        pygame.init()
        global is_alive, key_found, game_objects, collision_timer, astro_health, evil_health,current_level

        # Set up the Level by placing the objects of interest
        game_objects = {}

        #
        # Create the Game Objects and add them to the game_objects dictionary
        #
        # IMPORTANT: You must replace these images with your own.
        # IMPORTANT: the image file name is the name used for the item
        add_game_object(game_objects, "map3", 800 * 2, 600 * 1.5, 400 * 2, 300 * 1.5)
        add_game_object(game_objects, "map3_bg", 800 * 2, 600 * 1.5, 400 * 2, 300 * 1.5)
        add_game_object(game_objects, "astro3", 120, 120, 450, 450)
        add_game_object(game_objects, "evil", 100, 100, 1150, 450)
        add_game_object(game_objects, "crystal1", 70, 70, random.randint(150, 1550), random.randint(150, 850))
        add_game_object(game_objects, "crystal2", 70, 70, random.randint(150, 1550), random.randint(150, 850))
        add_game_object(game_objects, "crystal3", 70, 70, random.randint(150, 1550), random.randint(150, 850))
        add_game_object(game_objects, "crystal4", 70, 70, random.randint(150, 1550), random.randint(150, 850))
        add_game_object(game_objects, "crystal5", 70, 70, random.randint(150, 1550), random.randint(150, 850))
        add_game_object(game_objects, "crystal6", 70, 70, random.randint(150, 1550), random.randint(150, 850))
        add_game_object(game_objects, "crystal7", 70, 70, random.randint(150, 1550), random.randint(150, 850))
        add_game_object(game_objects, "crystal8", 70, 70, random.randint(150, 1550), random.randint(150, 850))
        add_game_object(game_objects, "crystal9", 70, 70, random.randint(150, 1550), random.randint(150, 850))
        add_game_object(game_objects, "crystal10", 70, 70, random.randint(150, 1550), random.randint(150, 850))

        screen = pygame.display.set_mode(game_objects["map3"]["image"].get_size())

        game_objects['astro3']['health'] = 100
        game_objects['astro3']['state'] = 'idle'
        game_objects['evil']['health'] = 100
        game_objects['evil']['state'] = 'idle'
        game_objects['evil']['attack_range'] = attack_range  # pixels
        game_objects['evil']['damage'] = villain_damage
        game_objects['evil']['speed'] = villain_speed
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

        astro_image = pygame.image.load("images/astro3.png").convert_alpha()  # Load and convert the image
        astro_image = pygame.transform.smoothscale(astro_image, (100, 100))  # Scale the image
        astro_flipped = pygame.transform.flip(astro_image, True, False)  # Flip the scaled image

        # This is the main game loop. In it, we must:
        # - check for events
        # - update the scene
        # - draw the scene
        collision_timer = None
        crystal_counter = 0
        all_keys_found = False

        while True:

            # Check events by looping over the list of events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Position the player to the mouse location
            if is_alive:
                if is_started:
                    level_3 = True
                    player = game_objects["astro3"]
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        player["image"] = astro_flipped  # Use the flipped image when moving left
                        player["pos"] += Vector2(-10, 0)
                    elif keys[pygame.K_RIGHT]:
                        player["image"] = astro_image  # Use the original image when moving right
                        player["pos"] += Vector2(10, 0)
                    if keys[pygame.K_UP]:
                        player["pos"] += Vector2(0, -10)
                    if keys[pygame.K_DOWN]:
                        player["pos"] += Vector2(0, 10)

                else:
                    # if the mouse comes near the player, start the game
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        is_started = True
            if game_objects['astro3']['state'] != 'defeated':
                # Check for player's attack input (e.g., pressing a key)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    attack(game_objects['evil'], player_damage)
            astro_health, evil_health, collision_timer = handle_collision(game_objects, collision_timer, astro_health,
                                                                          evil_health)

            # Display the health of both characters
            display_health(screen, font, astro_health, evil_health, game_objects['astro3']['pos'],
                           game_objects['evil']['pos'])

            pygame.display.flip()
            pygame.time.Clock().tick(60)

            villain_behavior(game_objects['evil'], game_objects['astro3'])

            # After processing events, check for defeated states
            if game_objects['astro3']['state'] == 'defeated':
                is_alive = False


            # Draw the game objects
            for object in game_objects.values():
                if object["visible"]:
                    draw_image_centered(screen, object["image"], object["pos"])

            display_health(screen, font, astro_health, evil_health, game_objects['astro3']['pos'],
                           game_objects['evil']['pos'])

            if pixel_collision(game_objects, "astro3", "crystal1"):
                crystal_counter += 1
                game_objects["crystal1"]["visible"] = False
                print(crystal_counter)
            elif pixel_collision(game_objects, "astro3", "crystal2"):
                crystal_counter += 1
                game_objects["crystal2"]["visible"] = False
                print(crystal_counter)
            elif pixel_collision(game_objects, "astro3", "crystal3"):
                crystal_counter += 1
                game_objects["crystal3"]["visible"] = False
                print(crystal_counter)
            elif pixel_collision(game_objects, "astro3", "crystal4"):
                crystal_counter += 1
                game_objects["crystal4"]["visible"] = False
                print(crystal_counter)
            elif pixel_collision(game_objects, "astro3", "crystal5"):
                crystal_counter += 1
                game_objects["crystal5"]["visible"] = False
                print(crystal_counter)
            elif pixel_collision(game_objects, "astro3", "crystal6"):
                crystal_counter += 1
                game_objects["crystal6"]["visible"] = False
                print(crystal_counter)
            elif pixel_collision(game_objects, "astro3", "crystal7"):
                crystal_counter += 1
                game_objects["crystal7"]["visible"] = False
                print(crystal_counter)
            elif pixel_collision(game_objects, "astro3", "crystal8"):
                crystal_counter += 1
                game_objects["crystal8"]["visible"] = False
                print(crystal_counter)
            elif pixel_collision(game_objects, "astro3", "crystal9"):
                crystal_counter += 1
                game_objects["crystal9"]["visible"] = False
                print(crystal_counter)
            elif pixel_collision(game_objects, "astro3", "crystal10"):
                crystal_counter += 1
                game_objects["crystal10"]["visible"] = False
                print(crystal_counter)

            if crystal_counter == 10 or crystal_counter > 10:
                all_keys_found = True

            # See if we touch the maze walls
            if pixel_collision(game_objects, "astro3", "map3"):
                label = myfont.render("Astro Collided inside the ship!", True, (0, 0, 0))
                screen.blit(label, (20, 80))
                is_alive = False
                pygame.mouse.set_visible(True)

            if (game_objects["crystal1"]["visible"] == False and game_objects["crystal2"]["visible"] == False )\
                    and (game_objects["crystal3"]["visible"] == False and game_objects["crystal4"]["visible"] == False )\
                    and (game_objects["crystal5"]["visible"] == False and game_objects["crystal6"]["visible"] == False )\
                    and (game_objects["crystal7"]["visible"] == False and game_objects["crystal8"]["visible"] == False )\
                    and (game_objects["crystal9"]["visible"] == False and game_objects["crystal10"]["visible"] == False ):
                current_level = 4
                return


            label = myfont.render("By Kunj rathod and Arsh khan !", True, (0, 0, 0))
            screen.blit(label, (20, 20))

            label = myfont.render("Press Space to start", True, (0, 0, 0))
            screen.blit(label, (20, 50))

            frame_count += 1
            if not is_alive:  # If the game has ended
                create_button(screen, "Restart", 120, 120, 100, 50, (150, 150, 150), (200, 200, 200), restart_game)

            # Bring drawn changes to the front
            pygame.display.flip()

            # This slows down the code, so it doesn't run more than 30 frames per second
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
    background_image = pygame.image.load('images/starting_img.png')  # Replace with your image path

    # Set up the button text
    font = pygame.font.Font(None, 36)
    text = font.render('Start', True, (230, 240, 220), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (1400, 300)  # Center of the screen or where you want it
    myfont = pygame.font.SysFont('times new roman', 30)

    running = True
    while running and current_level == 0:
        screen.blit(background_image, (0, 0))
        label = myfont.render("Astro\'s Adventure", True, (255, 255, 255))
        screen.blit(label, (1200, 100))
        label = myfont.render("By Kunj rathod and Arsh khan !", True, (255, 255, 255))
        screen.blit(label, (1200, 140))

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

def end_page():
    mixer.music.load('images/l4.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)

    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption('Game End')

    end_screen = pygame.image.load('Images/end_screen.png')
    end_screen = pygame.transform.scale(end_screen, (1600, 900))
    # Main loop
    running = True
    end_time = pygame.time.get_ticks() + 25000  # 25 seconds from now

    while running and current_level==4:
        screen.blit(end_screen, (0, 0))
        myfont = pygame.font.SysFont('times new roman', 72)
        label = myfont.render("ASTRO DEFEATS EVIL", True, (0, 0, 0))
        screen.blit(label, (750, 250))
        label = myfont.render("This was Astro's Adventure", True, (0, 0, 0))
        screen.blit(label, (750, 350))
        label = myfont.render("Game by Kunj and Arsh", True, (0, 0, 0))
        screen.blit(label, (750, 450))


        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        pygame.display.flip()

        if pygame.time.get_ticks() >= end_time:
            running = False
    # Clean up and quit
    pygame.quit()
    sys.exit()
while True:
    # Main game loop
    while True:
        if current_level == 0:
            start_page()
        elif current_level == 1:
            level_1()
        elif current_level == 2:
            level_2()
        elif current_level == 3:
            level_3()
        elif current_level == 4:
            end_page()

# Properly quit Pygame
pygame.quit()