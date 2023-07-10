import subprocess


import pygame
import sys
import os


SCALE = 2
DEVICE = "/dev/input/event7"


def get_absinfo():
    pipe = subprocess.Popen(
        ["libinput", "record", DEVICE],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    absinfo = {}
    section = {}

    with pipe.stdout as stream:
        while not pipe.poll():
            try:
                line = next(stream).decode().rstrip()
                # print(line)
                if line.startswith("devices:"):
                    section["devices"] = True
                    continue
                if section.get("devices"):
                    if line.startswith("  evdev:"):
                        section["devices_evdev"] = True
                        continue
                    elif line.startswith("  hid:"):
                        section["devices_evdev"] = False
                        continue

                    if section.get("devices_evdev"):
                        if line.startswith("    absinfo:"):
                            section["devices_evdev_absinfo"] = True
                            continue
                        elif line.startswith("    properties:"):
                            section["devices_evdev_absinfo"] = False
                            break

                        if section.get("devices_evdev_absinfo"):
                            key, value = line.strip().split(": ")
                            absinfo.update({int(key): eval(value)})

            except KeyboardInterrupt:
                print("Exiting due to interrupt")
                break
    # print(absinfo)
    pipe.kill()
    return absinfo


absinfo = get_absinfo()

MAX_X = absinfo[0][1]
MAX_Y = absinfo[1][1]
print(MAX_X, MAX_Y)
x = 0
y = 0

if os.environ["XDG_SESSION_TYPE"] == "wayland":
    os.environ["SDL_VIDEODRIVER"] = "wayland"


class Square(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Square, self).__init__()

        self.surf = pygame.Surface((10,10))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()

SCREEN_WIDTH = int(MAX_X/SCALE)
SCREEN_HEIGHT = int(MAX_Y/SCALE)

pygame.init()
root_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()


pointer = Square()
pointer.rect.move_ip(40,40)
root_surf.blit(pointer.surf, pointer.rect)
pygame.display.update()




pipe = subprocess.Popen(
    ["libinput", "record", DEVICE],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
)

section = {}
event = []
with pipe.stdout as stream:
    while not pipe.poll():
        try:
            line = next(stream).decode().rstrip()
            # print(line)
            if line.startswith("devices:"):
                section["devices"] = True
                continue
            if section.get("devices"):
                if line.startswith("  events:"):
                    section["devices_events"] = True
                    continue

                if section.get("devices_events"):
                    # remove comments and
                    for i, v in enumerate(line):
                        if v == "#":
                            line = line[:i]
                    line = line.strip(" -")
                    if not line:
                        continue

                    if line == "evdev:":
                        # if section.get("
                        # section["devices_events_evdev"] = True
                        # event = []
                        continue

                    e = eval(line)
                    if e[2] == 3:
                        if e[3] == 0:
                            x = int(e[4]/SCALE)
                        elif e[3] == 1:
                            y = int(e[4]/SCALE)
                    # print(x,y)
                    # event.append(eval(line))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    raise KeyboardInterrupt
                
                elif e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_ESCAPE, pygame.K_q):
                        raise KeyboardInterrupt
            
            root_surf.fill((0,0,0))
            pointer.rect.update((x, y), pointer.rect.size)
            root_surf.blit(pointer.surf, pointer.rect)
            # clock.tick(60)
            pygame.display.update()
            # clock.tick(30)
        except KeyboardInterrupt:
            print("Exiting due to interrupt")
            break


pipe.kill()
pygame.quit()
