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

width = 1280
height = 1024

pygame.init() #Initialise pygame
#screen = pygame.display.set_mode((1280,1024),pygame.FULLSCREEN)
screen = pygame.display.set_mode((width,height))
background = pygame.Surface(screen.get_size()) #Create the background object
background = background.convert() #Convert it to a background

#initialise global variables
progname = "HochzeitsCam v1.0 (c) Daniel Wandrei"
detetc_cam_cmd = "gphoto2 --auto-detect"
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
    smallfont = pygame.font.SysFont("freeserif", 25) #Small font for banner message
    bigfont = pygame.font.SysFont("freeserif", 50)  # Small font for banner message
    if (image != ""):
        image = pygame.image.load(image).convert_alpha()
        img_width =  image.get_width()
        img_height = image.get_height()
        aspect = img_width / width
        new_img_height = int(img_height / aspect)
        top_padding = int((height - new_img_height) / 2)

        image = pygame.transform.scale(image, (1280, new_img_height))

        screen.blit(image, (0, top_padding))

    # Render progtext
    hud_progname = smallfont.render(progname,1, (0,0,255))
    screen.blit(hud_progname,(20,980))

    # Render hud_counter
    hud_counter = bigfont.render("Bild " + `counter` + " von " + `image_count`,1, (0,0,255))
    screen.blit(hud_counter,(960,950)) #Write the image counter

    if(Message != ""): #If the big message exits write it
        font = pygame.font.SysFont("freeserif", 180)
        text = font.render(Message, 1, (0,0,255))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        screen.blit(text, textpos)

    pygame.draw.rect(screen,pygame.Color(0,0, 255),(10,10,1260,1004),2) #Draw the red outer box
    pygame.display.flip()

    return

# Los gehts
Message = "Lade..."
UpdateDisplay("")

# Pruefe ob images_dir existiert
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Zaehle Bilder
file_list = glob.glob(images_dir + "/*.jpg")
image_count = len(file_list)

UpdateDisplay("")
time.sleep(2)

# Warte auf Kamera
Message = "Kamera Check..."
UpdateDisplay("")
time.sleep(2)

camcheck = False
while not camcheck:
    detect = sub.check_output(detetc_cam_cmd, shell=True)
    if "PTP" in detect:
        camcheck = True
        Message = "Kamera OK!"
        UpdateDisplay("")
        time.sleep(2)
        Message = "Umount Kamera"
        UpdateDisplay("")
        sub.Popen(cam_umount_cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
        time.sleep(2)
    time.sleep(1)

time.sleep(3)
Message = ""
UpdateDisplay("")

# Ab hier Main-Loop
while(continue_loop):
    file_list = glob.glob(images_dir + "/*.jpg")
    image_count = len(file_list)
    counter = 0
    for file in file_list:
        counter = counter + 1
        UpdateDisplay( file )
        time.sleep(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "quiting..."
                continue_loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    take_pic_command = "gphoto2 --capture-image-and-download --filename ./images/" + str(image_count + 1) + ".jpg --force-overwrite"
                    pic = sub.Popen(take_pic_command, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)