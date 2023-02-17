
# from ast import Or
# from itertools import count
# from tkinter.tix import Tree
# from xmlrpc.client import TRANSPORT_ERROR
import pygame
from random import randint
import math
from sklearn.cluster import KMeans

def distance(p1,p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("Kmeans Visualization")

running = True
clock = pygame.time.Clock()

BACKGROUND = (214,214,214)
BLACK = (0,0,0)
BACKGROUND_PANEL = (249,255,230)
WHITE = (255,255,255)

RED = (255, 0, 0)
GREEN = (0,255,0)
YELLOW = (0,0,255)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRASS = (55,155,65)
GRAPE = (100,25,125)

COLORS = [RED, GREEN, YELLOW, PURPLE, SKY, ORANGE, GRASS, GRAPE]

font = pygame.font.SysFont('sans', 40)
font_small = pygame.font.SysFont('sans', 20)
text_plus = font.render("+", True, WHITE)
text_minus = font.render("-", True, WHITE)
text_run = font.render("Run", True, WHITE)
text_random = font.render("Random", True, WHITE)
text_algorithm = font.render("Algorithm", True, WHITE)
text_reset = font.render("Reset", True, WHITE)

K=0
error = 0 
points = []
clusters = []
labels = []

while running:
    clock.tick(60)
    screen.fill(BACKGROUND)

    # Draw interface
    # Draw panel

    pygame.draw.rect(screen, BLACK, (50,50,700,500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55,55,690,490))

    # K button +, -
    pygame.draw.rect(screen,BLACK, (850,50,50,50))
    screen.blit(text_plus, (865,45))

    pygame.draw.rect(screen,BLACK, (950,50,50,50))
    screen.blit(text_minus, (968, 43))

    # K value
    text_k = font.render("K = " + str(K),True, BLACK )
    screen.blit(text_k, (1050,50))

    # Run button
    pygame.draw.rect(screen, BLACK, (850, 150,150,50))
    screen.blit(text_run, (890, 150))

    # Random button
    pygame.draw.rect(screen, BLACK, (850, 250,150,50))
    screen.blit(text_random, (850, 250))

    # Reset button
    pygame.draw.rect(screen, BLACK, (850, 550,150,50))
    screen.blit(text_reset, (850, 550))

    # algo button
    pygame.draw.rect(screen, BLACK, (850, 450,150,50))
    screen.blit(text_algorithm, (850, 450))

     # End draw interface
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Draw mouse position
    if 50< mouse_x < 750 and 50 < mouse_y < 750:
        text_mouse = font_small.render("(" + str(mouse_x - 50) + "," + str(mouse_y - 50) + ")", True, BLACK)
        screen.blit(text_mouse, (mouse_x + 10, mouse_y))
   

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Create points on panel
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = []
                point = [mouse_x - 50, mouse_y - 50]
                points.append(point)

            # Change K button +
            if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                if K<8:
                    K += 1

            if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                if K > 0:
                    K -= 1
            
            # Run button
            if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
                labels = []

                if clusters == []:
                    continue

                # Assigning points to the closest cluster
                for p in points:
                    distances_to_cluster = []
                    for c in clusters:
                        dis = distance(p,c)
                        distances_to_cluster.append(dis)
                    min_distance = min(distances_to_cluster)
                    label = distances_to_cluster.index(min_distance)
                    labels.append(label)

                # Update clusters 
                for i in range(K):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1

                    if count != 0:
                        new_cluster_x = sum_x/count
                        new_cluster_y = sum_y / count
                        clusters[i] = [new_cluster_x, new_cluster_y]
            
            # Random
            if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
                labels = []
                clusters = []
                for i in range(K):
                    random_point = [randint(0, 700), randint(0, 500)]
                    clusters.append(random_point)

            # Reset
            if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
                K=0
                error = 0 
                points = []
                clusters = []
                labels = []

            
            # Algo
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                if K != 0 :
                    kmeans = KMeans(n_clusters=K).fit(points)
                    labels = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_
                else: 
                    continue


    # Draw points
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (points[i][0] + 50, points[i][1] + 50), 6 )

        if labels == []:
            pygame.draw.circle(screen, WHITE, (points[i][0] + 50, points[i][1] + 50), 5 )
        else:
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 5 )
    
    # Draw cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i] , (int(clusters[i][0]) + 50, int(clusters[i][1]) + 50), 10)

    # Calculate and draw error
    error = 0 
    if clusters != [] and labels != []:
        for i in range(len(points)):
            error += distance(points[i], clusters[labels[i]])
    
    text_error = font.render("Error = " + str(int(error)), True, BLACK)
    screen.blit(text_error, (850,350))
    

    pygame.display.flip()
    
pygame.quit()