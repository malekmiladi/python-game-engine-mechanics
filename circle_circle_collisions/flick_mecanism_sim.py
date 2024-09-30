if __name__ == "__main__":
    from circle_circle_collision import *
    import pygame as pg
    import time
    from pygame.locals import *
    from random import randint
    from os import environ

    environ["SDL_VIDEO_CENTERED"] = "1"

    pg.init()
    clock = pg.time.Clock()
    width, height = 1024, 600
    window = pg.display.set_mode((width, height))

    right_click = False
    left_click = False

    circles_list = [Circle(randint(1, 1000) % width, randint(1, 1000) % height, randint(20, 101)) for i in range(10)]
    circles_list_length = len(circles_list)
    running = True
    selected_circle = None
    move_circle = False
    moving_circles = []
    fps = 60
    done_moving = []
    last_time = time.time()

    while running:
        dt = (time.time() - last_time) * fps
        last_time = time.time()
        mouse_coords = pg.mouse.get_pos()
        window.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    left_click = True
                elif pg.mouse.get_pressed()[2]:
                    right_click = True
            if event.type == MOUSEBUTTONUP:
                if not pg.mouse.get_pressed()[0]:
                    left_click = False
                if not pg.mouse.get_pressed()[2]:
                    right_click = False
                    if selected_circle:
                        selected_circle.vx = .09 * (selected_circle.center_x - mouse_coords[0])
                        selected_circle.vy = .09 * (selected_circle.center_y - mouse_coords[1])
                        moving_circles.append(selected_circle)
                    selected_circle = None

        for circle in moving_circles:
            circle.ax = -.08 * circle.vx
            circle.ay = -.08 * circle.vy
            circle.vx += circle.ax
            circle.vy += circle.ay
            circle.center_x += circle.vx * dt
            circle.center_y += circle.vy * dt
            circle.collides_with_screen_boundaries(width, height)
        for i in range(len(moving_circles)):
            if abs(moving_circles[i].vx) < 0.01:
                moving_circles[i].vx = 0
                moving_circles[i].ax = 0
            if abs(moving_circles[i].vy) < 0.01:
                moving_circles[i].vy = 0
                moving_circles[i].ay = 0
            if moving_circles[i].vx == moving_circles[i].vy == 0:
                done_moving.append(i)
        if done_moving:
            for ind in done_moving:
                moving_circles[ind] = None
            done_moving = []
        while None in moving_circles:
            moving_circles.pop(moving_circles.index(None))

        for circle in circles_list:
            if circle.collides_with_mouse(mouse_coords):
                if left_click:
                    circle.center_x, circle.center_y = mouse_coords
                elif right_click:
                    if not selected_circle:
                        selected_circle = circle

        for i, circle in enumerate(circles_list):
            for j in range(i + 1, circles_list_length):
                if circle.collides_with(circles_list[j]):
                    circle.correct_overlapping(circles_list[j], width, height)

        for circle in circles_list:
            pg.draw.circle(window, (255, 255, 255), (int(circle.center_x), int(circle.center_y)), circle.radius, 1)
        if selected_circle:
            pg.draw.line(window, (0, 0, 200), mouse_coords, (selected_circle.center_x, selected_circle.center_y), 5)

        pg.display.update()
        clock.tick(fps)