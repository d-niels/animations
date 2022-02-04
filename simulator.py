import pygame
import numpy as np


# Common colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Window to display the simulation
class Frame(object):
    def __init__(self, width=800, height=600, title='Simulation'):
        pygame.init()

        # Size of the frame
        self.width = width
        self.height = height

        # Pygame parameters
        self.win = pygame.display
        self.win.set_caption(title)
        self.surface = self.win.set_mode([width, height])
        self.clock = pygame.time.Clock()

    # Pause the frame
    def wait(self, time):
        pygame.time.delay(int(time * 1000))

    # Create a new frame by drawing all the scene data
    def new_frame(self, scene, time):
        font = pygame.font.SysFont('timesnewroman', 20)
        text = font.render(str(time), False, BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.surface.fill(WHITE)
        self.surface.blit(text, (self.width - 50, 0))

        # Corner coordinates
        UL = np.array([-self.width/2, self.height/2])
        UR = np.array([self.width/2, self.height/2])
        BR = np.array([self.width/2, -self.height/2])
        BL = np.array([-self.width/2, -self.height/2])

        # Draw particles
        i = 0
        while i < len(scene.q):
            pygame.draw.circle(
                self.surface,
                scene.color[i // 2],
                (scene.q[i] + self.width / 2, -scene.q[i + 1] + self.height / 2),
                scene.r[i // 2]
            )
            i += 2

        # Draw Planes
        i = 0
        while i < len(scene.plane_q):
            # Container to hold all the points for the polygon shape
            pts = []

            # Convert the vertex of the plane to the frame's coordinate system
            # (0, 0) in top left corner, (width, height) in bottom right corner
            qx = scene.plane_q[i][0] + self.width / 2
            qy = - scene.plane_q[i][1] + self.height / 2
            nx = scene.plane_n[i][0]
            ny = - scene.plane_n[i][1]

            # Calculate the slope of the plane surface
            m = 0
            if nx != 0:
                m = -ny / nx

            # Find which corners are contained within the plane
            if np.dot(scene.plane_n[i], UL - scene.plane_q[i]) <= 0:
                pts.append([0, 0])
            if np.dot(scene.plane_n[i], UR - scene.plane_q[i]) <= 0:
                pts.append([self.width, 0])
            if np.dot(scene.plane_n[i], BR - scene.plane_q[i]) <= 0:
                pts.append([self.width, self.height])
            if np.dot(scene.plane_n[i], BL - scene.plane_q[i]) <= 0:
                pts.append([0, self.height])

            # Find where the plane surface intercepts the frame's edges
            top_int = 0
            bottom_int = 0
            if m != 0:
                top_int = int(-qy / m + qx)
                bottom_int = int((self.height - qy) / m + qy)
            left_int = int(-qx * m + qy)
            right_int = int(m * (self.width - qx) + qy)

            if 0 < top_int < self.width:
                pts.append([top_int, 0])
            if 0 < bottom_int < self.width:
                pts.append([bottom_int, self.height])
            if 0 < left_int < self.height:
                pts.append([0, left_int])
            if 0 < right_int < self.height:
                pts.append([self.width, right_int])

            # Sort pts so that they can be drawn properly
            length = len(pts)
            pts_sorted = [pts.pop()]
            while len(pts_sorted) < length:
                start = len(pts)
                j = 0
                while j < len(pts):
                    if pts[j][0] == pts_sorted[-1][0]:
                        pts_sorted.append(pts.pop(j))
                    elif pts[j][1] == pts_sorted[-1][1]:
                        pts_sorted.append(pts.pop(j))
                    j += 1
                if start == len(pts):
                    pts_sorted.append(pts[0])

            # Handle if nx = 0
            if nx == 0 and ny > 0:
                pts_sorted = [[0, qy], [0, 0], [self.width, 0], [self.width, qy]]
            elif nx == 0 and ny < 0:
                pts_sorted = [[0, qy], [0, self.height], [self.width, self.height], [self.width, qy]]

            # Handle if ny = 0
            if ny == 0 and nx > 0:
                pts.sorted = [[0, 0], [qx, 0], [qx, self.height], [0, self.height]]
            elif ny == 0 and nx < 0:
                pts.sorted = [[self.width, 0], [qx, 0], [qx, self.height], [self.width, self.height]]

            # Draw the polygon that represents the plane
            pygame.draw.polygon(
                self.surface,
                scene.plane_color[i],
                pts_sorted
            )
            i += 1

        self.win.update()
