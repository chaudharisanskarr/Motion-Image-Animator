import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np
import math
import imgui
from imgui.integrations.glfw import GlfwRenderer
import pygame

def load_texture(path):
    img = Image.open(path)
    img = img.transpose(Image.FLIP_TOP_BOTTOM) 
    img_data = np.array(list(img.getdata()), np.uint8)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture

def load_black_overlay(opacity):
    img = Image.new('RGBA', (1000, 800), color=(0, 0, 0, int(opacity * 255)))  # Convert opacity to 0-255 range
    img_data = np.array(img)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture

def main():
    
    if not glfw.init():
        return

    window = glfw.create_window(1000, 800, "Layered Animation", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    imgui.create_context()  # Initialize ImGui context
    renderer = GlfwRenderer(window)

    # Load background texture
    background_texture = load_texture("background2.png")
    # Load cloud texture
    cloud_texture = load_texture("cloud2.png")
    # Load boat texture
    boat_texture = load_texture("boat2.png")
    # Load tree texture
    tree_texture = load_texture("tree2.png")
    # Load water texture
    water_texture = load_texture("water3.png")
    # Load black overlay texture
    black_overlay_opacity = 0.5  # Initial opacity
    black_overlay_texture = load_black_overlay(black_overlay_opacity)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    cloud_position = 0.0
    cloud_speed = 0.00005

    boat_position_y = 0.0
    boat_amplitude = 0.008  # Adjust amplitude of boat wobble
    boat_speed = 1  # Adjust speed of boat wobble

    tree_position_x = 0.0
    tree_amplitude = 0.008  # Adjust amplitude of tree movement
    tree_speed = 1.0  # Adjust speed of tree movement

    water_position_x = 0.0
    water_amplitude = 0.008  # Adjust amplitude of water movement
    water_speed = 1.0  # Adjust speed of water movement

    # Initialize Pygame mixer for audio
    pygame.mixer.init()
    wave_sound = pygame.mixer.Sound("wave.wav")
    wave_sound.set_volume(0.5)  # Adjust volume here

    # Day-Night Cycle
    day_time = True
    ambient_light = [0.7, 0.7, 0.7, 1.0]  # Daytime ambient light
    night_ambient_light = [0.1, 0.1, 0.1, 1.0]  # Nighttime ambient light
    glfw.set_time(0.0)  # Start with daytime

    toggle_opacity = False  # Flag to toggle opacity
    black_overlay_opacity_step = 0.5  # Opacity step for toggling

    while not glfw.window_should_close(window):
        glfw.poll_events()
        renderer.process_inputs()

        # Toggle day/night cycle
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            day_time = not day_time

        # Update ambient light based on time of day
        if day_time:
            ambient_light = [0.7, 0.7, 0.7, 1.0]
        else:
            ambient_light = [0.1, 0.1, 0.1, 1.0]

        # Toggle black overlay opacity
        if glfw.get_key(window, glfw.KEY_N) == glfw.PRESS and not toggle_opacity:
            black_overlay_opacity = 0.0 if black_overlay_opacity == 0.5 else 0.5
            black_overlay_texture = load_black_overlay(black_overlay_opacity)
            toggle_opacity = True
        elif glfw.get_key(window, glfw.KEY_N) == glfw.RELEASE:
            toggle_opacity = False

        # Start playing sound
        wave_sound.play()

        # Rendering
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        imgui.new_frame()

        imgui.begin("Speed Controls")

        # Cloud Speed Control
        _, cloud_speed = imgui.slider_float("Cloud Speed", cloud_speed, 0.0, 0.0001)

        # Boat Speed Control
        _, boat_speed = imgui.slider_float("Boat Speed", boat_speed, 0.0, 2.0)

        # Tree Speed Control
        _, tree_speed = imgui.slider_float("Tree Speed", tree_speed, 0.0, 2.0)

        # Water Speed Control
        _, water_speed = imgui.slider_float("Water Speed", water_speed, 0.0, 2.0)

        imgui.end()

        # Set ambient light
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)

        # Draw background (water)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, background_texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex2f(-1.0, 1.0)
        glTexCoord2f(1.0, 1.0); glVertex2f(1.0, 1.0)
        glTexCoord2f(1.0, 0.0); glVertex2f(1.0, -1.0)
        glTexCoord2f(0.0, 0.0); glVertex2f(-1.0, -1.0)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

        # Draw cloud
        glBindTexture(GL_TEXTURE_2D, cloud_texture)
        cloud_position = (cloud_position + cloud_speed) % 1.0
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex2f(cloud_position - 1, 0.7)  # Adjust height here
        glTexCoord2f(1.0, 1.0); glVertex2f(cloud_position, 0.7)     # Adjust height here
        glTexCoord2f(1.0, 0.0); glVertex2f(cloud_position, 0.2)     # Adjust height here
        glTexCoord2f(0.0, 0.0); glVertex2f(cloud_position - 1, 0.2)  # Adjust height here
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

        # Draw tree
        glBindTexture(GL_TEXTURE_2D, tree_texture)
        tree_position_x = math.sin(glfw.get_time() * tree_speed) * tree_amplitude
        tree_size_x = 1  # Adjust tree width
        tree_size_y = 1  # Adjust tree height
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex2f(-tree_size_x + tree_position_x, tree_size_y)  # Adjust tree size and position here
        glTexCoord2f(1.0, 1.0); glVertex2f(tree_size_x + tree_position_x, tree_size_y)   # Adjust tree size and position here
        glTexCoord2f(1.0, 0.0); glVertex2f(tree_size_x + tree_position_x, -tree_size_y)  # Adjust tree size and position here
        glTexCoord2f(0.0, 0.0); glVertex2f(-tree_size_x + tree_position_x, -tree_size_y) # Adjust tree size and position here
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

        # Draw water
        glBindTexture(GL_TEXTURE_2D, water_texture)
        water_position_x = math.sin(glfw.get_time() * water_speed) * water_amplitude
        water_size_x = 1  # Adjust water width
        water_size_y = 1  # Adjust water height
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex2f(-water_size_x + water_position_x, 1)  # Adjust water size and position here
        glTexCoord2f(1.0, 1.0); glVertex2f(water_size_x + water_position_x, 1)   # Adjust water size and position here
        glTexCoord2f(1.0, 0.0); glVertex2f(water_size_x + water_position_x, -1.0)  # Adjust water size and position here
        glTexCoord2f(0.0, 0.0); glVertex2f(-water_size_x + water_position_x, -1.0) # Adjust water size and position here
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

        # Draw boat
        glBindTexture(GL_TEXTURE_2D, boat_texture)
        boat_position_y = math.sin(glfw.get_time() * boat_speed) * boat_amplitude
        boat_size_x = 1  # Adjust boat width
        boat_size_y = 1  # Adjust boat height
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex2f(-boat_size_x, boat_size_y + boat_position_y)  # Adjust boat size and position here
        glTexCoord2f(1.0, 1.0); glVertex2f(boat_size_x, boat_size_y + boat_position_y)   # Adjust boat size and position here
        glTexCoord2f(1.0, 0.0); glVertex2f(boat_size_x, -boat_size_y + boat_position_y)  # Adjust boat size and position here
        glTexCoord2f(0.0, 0.0); glVertex2f(-boat_size_x, -boat_size_y + boat_position_y) # Adjust boat size and position here
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

        # Draw black overlay with adjusted opacity
        glBindTexture(GL_TEXTURE_2D, black_overlay_texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex2f(-1.0, 1.0)
        glTexCoord2f(1.0, 1.0); glVertex2f(1.0, 1.0)
        glTexCoord2f(1.0, 0.0); glVertex2f(1.0, -1.0)
        glTexCoord2f(0.0, 0.0); glVertex2f(-1.0, -1.0)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

        glDisable(GL_TEXTURE_2D)

        imgui.render()
        renderer.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    # Stop the sound when the window closes
    wave_sound.stop()
    pygame.mixer.quit()

    glfw.terminate()

if __name__ == "__main__":
    main()
