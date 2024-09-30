from math import sqrt


class Circle:

    def __init__(self, x, y, radius, weight=None, vx=0, vy=0, ax=0, ay=0):

        self.center_x = x
        self.center_y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.radius = radius

    def get_distance(self, other):

        return sqrt((self.center_y - other.center_y) ** 2 + (self.center_x - other.center_x) ** 2)

    def get_direction_vector(self, other):

        return self.center_x - other.center_x, self.center_y - other.center_y

    def collides_with(self, other):

        return self.get_distance(other) < self.radius + other.radius

    def collides_with_mouse(self, mouse_coords):

        return sqrt((self.center_y - mouse_coords[1]) ** 2 + (self.center_x - mouse_coords[0]) ** 2) < self.radius

    def collides_with_screen_boundaries(self, width, height):

        if self.center_x - self.radius < 0:
            self.center_x = self.radius
            self.vx *= -1
        if self.center_x + self.radius > width:
            self.center_x = width - self.radius
            self.vx *= -1
        if self.center_y - self.radius < 0:
            self.center_y = self.radius
            self.vy *= -1
        if self.center_y + self.radius > height:
            self.center_y = height - self.radius
            self.vy *= -1

    def correct_overlapping(self, other, width, height):

        distance_between_circles = self.get_distance(other)
        direction_x, direction_y = self.get_direction_vector(other)
        correction = .5 * (distance_between_circles - self.radius - other.radius)

        self.center_x -= correction * direction_x / distance_between_circles
        self.collides_with_screen_boundaries(width, height)
        self.center_y -= correction * direction_y / distance_between_circles
        self.collides_with_screen_boundaries(width, height)

        other.center_x += correction * direction_x / distance_between_circles
        other.collides_with_screen_boundaries(width, height)
        other.center_y += correction * direction_y / distance_between_circles
        other.collides_with_screen_boundaries(width, height)
