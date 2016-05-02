######################################################################
# cyBOOTH                                                            #
######################################################################

#IMPORTS

from __future__ import division
import pygame
import time
import subprocess as sub
import glob
import os
import sys

width = 1280
height = 1024

pygame.init() #Pygame GO
#screen = pygame.display.set_mode((1280,1024),pygame.FULLSCREEN) # Vorerst kein Fullscreen
screen = pygame.display.set_mode((width,height))

background = pygame.Surface(screen.get_size())
background = background.convert()

#Globale Variablen
progname = "HochzeitsCam v1.0 (c) Daniel Wandrei"
detect_cam_cmd = "gphoto2 --auto-detect"
cam_umount_cmd = "gvfs-mount -s gphoto2"
take_pic_cmd = "gphoto2 --capture-image-and-download --folder /images --force-overwrite"
images_dir = "images"
counter = 0
image_count = 0
continue_loop = True
backg_img = "backg.jpg"


def UpdateDisplay( image ):
    #background.fill(pygame.Color("black")) #Black background)
    background = pygame.image.load(backg_img)
    background = pygame.transform.scale(background, (width, height))
    screen.blit(background, (0, 0))
    smallfont = pygame.font.SysFont("Noto Sans", 25)
    bigfont = pygame.font.SysFont("Noto Sans", 50)
    if (image != ""):
        image = pygame.image.load(image).convert_alpha()
        img_width =  image.get_width()
        img_height = image.get_height()
        aspect = img_width / width
        new_img_height = int(img_height / aspect)
        top_padding = int((height - new_img_height) / 2)

        image = pygame.transform.scale(image, (1220, new_img_height))

        screen.blit(image, (30, top_padding))

    # Render progname
    hud_progname = smallfont.render(progname,1, (0,0,255))
    screen.blit(hud_progname,(43,950))

    # Render hud_counter
    hud_counter = bigfont.render("Bild " + `counter` + " von " + `image_count`,1, (0,0,255))
    screen.blit(hud_counter,(960,920))

    if(Message != ""):
        font = pygame.font.SysFont("Noto Sans", 220)
        text = font.render(Message, 1, (0,0,255))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        screen.blit(text, textpos)

    pygame.draw.rect(screen,pygame.Color(0,0, 255),(10,10,1260,1004),2)
    pygame.display.flip()

    return

# Los gehts
pygame.display.set_caption(progname)
Message = "Hallo Welt!"
UpdateDisplay("")

# Pruefe ob images_dir existiert
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Zaehle Bilder
file_list = glob.glob(images_dir + "/*.jpg")
image_count = len(file_list)

UpdateDisplay("")
time.sleep(1)

# Warte auf Kamera
Message = "Kamera..."
UpdateDisplay("")
time.sleep(1)
camcheck = False
while not camcheck:
    detect = sub.check_output(detect_cam_cmd, shell=True)
    if "PTP" in detect:
        camcheck = True
        Message = "OK!"
        UpdateDisplay("")
        time.sleep(1)
        Message = "Umount..."
        UpdateDisplay("")
        time.sleep(1)
        sub.Popen(cam_umount_cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
        Message = "OK!"
        UpdateDisplay("")
    time.sleep(1)
Message = ""
UpdateDisplay("")
time.sleep(3)

# Ab hier Main-Loop
while(continue_loop):
    file_list = glob.glob(images_dir + "/*.jpg")
    image_count = len(file_list)
    counter = 0
    for file in file_list:
        counter = counter + 1
        UpdateDisplay( file )
        for wait_for_input in range(1,3000):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "quiting..."
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or vent.key == pygame.K_ESCAPE:
                        while True:
                            detect = sub.check_output(detect_cam_cmd, shell=True)
                            if "PTP" in detect:
                                break
                            else:
                                Message = "Kamera?"
                                UpdateDisplay("")
                                time.sleep(1)
                                detect = sub.check_output(detect_cam_cmd, shell=True)
                                if "PTP" in detect:
                                        camcheck = True
                                        Message = "OK!"
                                        UpdateDisplay("")
                                        time.sleep(1)
                                        Message = "Umount..."
                                        UpdateDisplay("")
                                        time.sleep(1)
                                        sub.Popen(cam_umount_cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
                                        Message = "OK!"
                                        UpdateDisplay("")
                                        time.sleep(1)
                                        break
                        for timer in range(5, 0, -1):
                            Message = timer
                            UpdateDisplay("")
                            time.sleep(1)
                        Message = "SMILE ;)"
                        UpdateDisplay("")
                        take_pic_command = "gphoto2 --capture-image-and-download --filename ./images/" + str(image_count + 1) + ".jpg --force-overwrite"
                        pic = sub.Popen(take_pic_command, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
                        time.sleep(4)
                        Message = "Lade Bild..."
                        UpdateDisplay("")
                        pic.wait()
                        Message = ""
                        UpdateDisplay("")
                        time.sleep(1)
                        UpdateDisplay("./images/" + str(image_count + 1) + ".jpg")
                        time.sleep(10)
            time.sleep(0.001)