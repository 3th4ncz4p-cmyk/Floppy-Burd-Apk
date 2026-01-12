# main.py
"""
Floppy Burd - Caveman Studios
"""

import pygame, random, sys, math, json, time, os

# --- Gestion des chemins pour compatibilité EXE et Sauvegarde ---
def get_save_path():
    # Détection si l'application tourne sur Android
# --- On simplifie au maximum pour Android ---
try:
    if 'ANDROID_ARGUMENT' not in os.environ and not getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass

pygame.init()
pygame.mixer.init()
#icon_surface = pygame.image.load("icon_burd.png") 
#pygame.display.set_icon(icon_surface)

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w if 'ANDROID_ARGUMENT' in os.environ else 500
SCREEN_HEIGHT = info.current_h if 'ANDROID_ARGUMENT' in os.environ else 700
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# --- Chargement et configuration du Logo Studio ---
LOGO_STUDIO = pygame.image.load("Caveman_Studios.png")
# On le redimensionne pour qu'il ne prenne pas trop de place (80x80 pixels)
LOGO_STUDIO = pygame.transform.scale(LOGO_STUDIO, (200, 200))

volume_on = True
SAVE_FILE = get_save_path()

# --------------Settings------------
WIDTH, HEIGHT = 500, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floppy Burd")
FPS = 60
clock = pygame.time.Clock()

# Colors
YELLOW = (255, 230, 0)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
LIGHT_GREEN = (0, 220, 0)
BLUE_LIGHT = (135, 206, 250)
BLUE_DARK = (10, 10, 50)
RED = (200, 0, 0)
BUTTON_HOVER = (60, 240, 80)
CONFETTI_COLORS = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

# Physics
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_SPEED = 3
PIPE_GAP = 180

# Fonts
TITLE_FONT = pygame.font.SysFont("comicsansms", 80, bold=True)
FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont("comicsansms", 20, bold=True)
BUTTON_FONT = pygame.font.SysFont("comicsansms", 34, bold=True)
STUDIO_FONT = pygame.font.SysFont("comicsansms", 18, bold=True)

# Easter eggs
EASTER_TEXTS = [
    "Can't pass 10 ? too bad",
    "Try TREXMAND-V",
    "The burd was trained by the shadow government",
    "Do not smash your keyboard",
    "99,999% of the players ragequit after 3 games",
    "How does it feel to be dressed as a maid ?",
    "druB yppolF",
    "Error 404 skill not found",
    "Da Burd is a Burd",
    "KYS : Keep Yourself Safe",
    "Drink some cofee, I suggest a latte macchiato",
    "43.883011°N ; -0.517631°E",
    "amazing chest ahead",
    "I Always Come Back",
    "Flap and plap the bird , wait...",
    "Hey ! Listen...",
    "https://youtu.be/7Wq9U3ypcDY"
]

# Skins definitions
SKINS = [
    ("Yellow", (255,230,0), 0),
    ("Red", (220,50,50), 10),
    ("Blue", (80,150,255), 25),
    ("Green", (80,255,120), 50),
    ("Black", (30,30,30), 100),
    ("Rainbow", None, 200),
]
GOLD_SKIN = ("Gold", (255,220,40), 500)

# -------------------- Sounds & Music --------------------
def safe_load_sound(fname):
    if not os.path.exists(fname): return None
    try:
        return pygame.mixer.Sound(fname)
    except: return None

def safe_music_load(fname):
    if not os.path.exists(fname): return False
    try:
        pygame.mixer.music.load(fname)
        return True
    except: return False

SOUND_JUMP = safe_load_sound("jump.wav")
SOUND_HIT = safe_load_sound("hit.wav")
SOUND_GAMEOVER = safe_load_sound("game_over.wav")
MENU_MUSIC = "menu_song.wav"
GAME_MUSIC = "game_song.wav"

def stop_music():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

# -------------------- Utility drawing --------------------
def draw_text_outline(surface, text, font_obj, color, outline_color, pos, angle=0):
    txt = font_obj.render(text, True, color)
    outline = font_obj.render(text, True, outline_color)
    surf = pygame.Surface((txt.get_width()+12, txt.get_height()+12), pygame.SRCALPHA)
    for dx in (-3,0,3):
        for dy in (-3,0,3):
            if dx!=0 or dy!=0: surf.blit(outline, (dx+6, dy+6))
    surf.blit(txt, (6,6))
    if angle != 0: surf = pygame.transform.rotate(surf, angle)
    rect = surf.get_rect(center=pos)
    surface.blit(surf, rect.topleft)

def draw_button(surface, rect, text, hover=False, color=LIGHT_GREEN):
    shadow = rect.move(3,4)
    pygame.draw.rect(surface, (0,0,0), shadow, border_radius=8)
    col = BUTTON_HOVER if hover else color
    pygame.draw.rect(surface, col, rect, border_radius=8)
    pygame.draw.rect(surface, BLACK, rect, 4, border_radius=8)
    draw_text_outline(surface, text, BUTTON_FONT, WHITE, BLACK, rect.center)

def get_easter_font(text):
    max_w, size = WIDTH - 40, 24
    f = pygame.font.SysFont("comicsansms", size, bold=True)
    while f.size(text)[0] > max_w and size > 12:
        size -= 1
        f = pygame.font.SysFont("comicsansms", size, bold=True)
    return f

def draw_volume_icon(win, rect):
    # Fond du bouton
    vol_color = (0, 200, 0) if volume_on else (200, 0, 0)
    pygame.draw.rect(win, vol_color, rect, border_radius=10)
    
    # Dessin du haut-parleur
    ic = WHITE
    spk_w, spk_h = 8, 12
    sx = rect.x + 8
    sy = rect.centery - spk_h // 2
    # Base du haut-parleur
    pygame.draw.rect(win, ic, (sx, sy, spk_w, spk_h))
    # Cône
    pygame.draw.polygon(win, ic, [(sx+spk_w, sy), (sx+spk_w+10, sy-6), (sx+spk_w+10, sy+spk_h+6), (sx+spk_w, sy+spk_h)])
    
    if volume_on:
        # Ondes sonores
        pygame.draw.arc(win, ic, (sx+12, sy-4, 15, 20), -math.pi/3, math.pi/3, 3)
        pygame.draw.arc(win, ic, (sx+18, sy-8, 20, 28), -math.pi/3, math.pi/3, 3)
    else:
        # Croix pour "muet"
        xx = sx + 22
        pygame.draw.line(win, ic, (xx, sy), (xx+8, sy+spk_h), 2)
        pygame.draw.line(win, ic, (xx+8, sy), (xx, sy+spk_h), 2)

def draw_trash_icon(win, rect, hover=False):
    # Couleur de la poubelle (rouge si survolé, gris sinon)
    color = (255, 50, 50) if hover else (180, 180, 180)
    pygame.draw.rect(win, (40, 40, 40), rect, border_radius=10) # Fond du bouton
    
    # Dessin de la poubelle
    padding = 12
    tx, ty, tw, th = rect.x + padding, rect.y + padding + 5, rect.width - padding*2, rect.height - padding*2 - 5
    
    # Corps
    pygame.draw.polygon(win, color, [(tx, ty), (tx + tw, ty), (tx + tw - 5, ty + th), (tx + 5, ty + th)])
    # Couvercle
    pygame.draw.rect(win, color, (tx - 3, ty - 6, tw + 6, 4), border_radius=2)
    pygame.draw.rect(win, color, (tx + tw//2 - 5, ty - 10, 10, 4), border_radius=1)
    # Lignes verticales sur le corps
    for i in [-4, 0, 4]:
        pygame.draw.line(win, (30, 30, 30), (rect.centerx + i, ty + 4), (rect.centerx + i, ty + th - 4), 2)

def draw_confirm_icons(win, check_rect, cross_rect, mx, my):
    # Dessin du bouton OUI (Checkmark)
    h_ok = check_rect.collidepoint(mx, my)
    pygame.draw.rect(win, (40, 180, 40) if h_ok else (20, 100, 20), check_rect, border_radius=8)
    # Dessin de la coche
    cx, cy = check_rect.center
    pygame.draw.lines(win, WHITE, False, [(cx-10, cy), (cx-3, cy+8), (cx+12, cy-10)], 4)

    # Dessin du bouton NON (Croix)
    h_no = cross_rect.collidepoint(mx, my)
    pygame.draw.rect(win, (220, 40, 40) if h_no else (120, 20, 20), cross_rect, border_radius=8)
    # Dessin de la croix
    cx, cy = cross_rect.center
    pygame.draw.line(win, WHITE, (cx-10, cy-10), (cx+10, cy+10), 4)
    pygame.draw.line(win, WHITE, (cx+10, cy-10), (cx-10, cy+10), 4)

def show_confirm_dialog(save_data):
    # Une mini boucle pour la boîte de dialogue
    while True:
        mx, my = pygame.mouse.get_pos()
        # Overlay sombre
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        WINDOW.blit(overlay, (0,0))
        
        dialog_rect = pygame.Rect(WIDTH//2-150, HEIGHT//2-80, 300, 160)
        pygame.draw.rect(WINDOW, (50, 50, 50), dialog_rect, border_radius=15)
        pygame.draw.rect(WINDOW, WHITE, dialog_rect, 3, border_radius=15)
        
        draw_text_outline(WINDOW, "Wipe Save ?", FONT, WHITE, BLACK, (WIDTH//2, HEIGHT//2-40))
        draw_text_outline(WINDOW, "Are you sure?", SMALL_FONT, YELLOW, BLACK, (WIDTH//2, HEIGHT//2-10))
        
        ok_rect = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 20, 60, 45)
        no_rect = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 20, 60, 45)
        draw_confirm_icons(WINDOW, ok_rect, no_rect, mx, my)
        
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if ok_rect.collidepoint(mx, my): return True
                if no_rect.collidepoint(mx, my): return False

# -------------------- Particles / Confetti --------------------
class Particle:
    def __init__(self,x,y):
        self.x=x; self.y=y; self.r=random.randint(2,5)
        self.color=random.choice([(255,255,255),(255,200,50),(255,150,50)])
        self.vx=random.uniform(-3,3); self.vy=random.uniform(-3,3); self.life=random.randint(20,40)
    def move(self):
        self.x+=self.vx; self.y+=self.vy; self.life-=1; self.r=max(0,self.r-0.1)
    def draw(self,surf):
        if self.life>0 and self.r>0:
            pygame.draw.circle(surf,self.color,(int(self.x),int(self.y)),int(self.r))

class Confetti:
    def __init__(self,x,y):
        self.x=x; self.y=y; self.size=random.randint(4,8); self.color=random.choice(CONFETTI_COLORS)
        self.vx=random.uniform(-2,2); self.vy=random.uniform(-5,-1); self.g=0.2; self.life=random.randint(40,80)
        self.angle=random.uniform(0,360); self.aspeed=random.uniform(-5,5)
    def move(self):
        self.vy+=self.g; self.x+=self.vx; self.y+=self.vy; self.angle+=self.aspeed; self.life-=1
    def draw(self, surf):
        if self.life > 0:
            # Petite traînée
            pygame.draw.line(surf, self.color, (self.x, self.y), (self.x - self.vx*2, self.y - self.vy*2), 2)
            # Confetti rotatif
            s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            s.fill(self.color)
            r = pygame.transform.rotate(s, self.angle)
            surf.blit(r, (int(self.x), int(self.y)))

# -------------------- Environment --------------------
class Pipe:
    def __init__(self,x):
        self.x=x; self.height=random.randint(150, HEIGHT-150-PIPE_GAP)
        self.top=self.height; self.bottom=self.height+PIPE_GAP; self.width=70
        self.offset = random.uniform(-20,20); self.ospeed = random.uniform(0.5,1.0); self.scored=False
    def move(self):
        self.x-=PIPE_SPEED; self.offset+=self.ospeed
        if self.offset>20 or self.offset<-20: self.ospeed*=-1
    def draw(self, win):
        ty, by = self.top + int(self.offset), self.bottom + int(self.offset)
        
        def draw_fancy_pipe(x, y, w, h, is_top):
            # Corps du tuyau avec dégradé de vert
            pygame.draw.rect(win, (0, 100, 0), (x, y, w, h)) # Bord sombre
            pygame.draw.rect(win, GREEN, (x + 5, y, w - 15, h)) # Couleur base
            pygame.draw.rect(win, (144, 238, 144), (x + 10, y, 5, h)) # Reflet lumière
            
            # Chapeau du tuyau
            cap_h = 30
            cap_y = ty - cap_h if is_top else by
            pygame.draw.rect(win, (0, 80, 0), (x - 5, cap_y, w + 10, cap_h), border_radius=3)
            pygame.draw.rect(win, GREEN, (x - 3, cap_y + 2, w + 6, cap_h - 4), border_radius=3)
            pygame.draw.rect(win, (144, 238, 144), (x + 5, cap_y + 2, 5, cap_h - 4)) # Reflet chapeau

        draw_fancy_pipe(self.x, 0, self.width, ty, True)
        draw_fancy_pipe(self.x, by, self.width, HEIGHT - by, False)

    def collide(self,bird):
        ty, by = self.top + int(self.offset), self.bottom + int(self.offset)
        if bird.y - bird.h/2 < ty or bird.y + bird.h/2 > by:
            if bird.x + bird.w/2 > self.x and bird.x - bird.w/2 < self.x + self.width: return True
        return False

class Cloud:
    def __init__(self):
        self.x=random.randint(0,WIDTH); self.y=random.randint(50,200)
        self.size=random.randint(20,40); self.speed=random.uniform(0.2,0.5); self.depth=random.uniform(0.5,1.0)
    def move(self):
        self.x -= self.speed*self.depth
        if self.x<-self.size*3: self.x = WIDTH + self.size*3; self.y = random.randint(50,200)
    def draw(self, win):
        # Ombre portée (gris clair décalé)
        for ox, oy, col in [(4, 4, (200, 200, 200)), (0, 0, WHITE)]:
            pygame.draw.circle(win, col, (int(self.x), int(self.y + oy)), self.size)
            pygame.draw.circle(win, col, (int(self.x + self.size), int(self.y + self.size // 3 + oy)), self.size - 5)
            pygame.draw.circle(win, col, (int(self.x - self.size), int(self.y + self.size // 3 + oy)), self.size - 5)

class Star:
    def __init__(self):
        self.x=random.randint(0,WIDTH); self.y=random.randint(0,HEIGHT//2); self.size=random.randint(2,5)
    def draw(self,win,alpha=255):
        s = self.size; color = (255,255,255, alpha); surf = pygame.Surface((s*4,s*4), pygame.SRCALPHA)
        pygame.draw.polygon(surf, color, [(s,0),(0,s*2),(s*2,s*2)])
        pygame.draw.polygon(surf, color, [(s,s*2),(0,0),(s*2,0)])
        win.blit(surf, (self.x-s, self.y-s))

class Mountain:
    def __init__(self):
        # Paramètres de taille globale
        self.width = random.randint(700, 1000)
        self.height = random.randint(450, 600)
        self.x = WIDTH + random.randint(0, 500)
        self.speed = 0.4
        
        # Génération de la silhouette (plusieurs sommets)
        self.points = []
        num_pts = random.randint(6, 10)
        for i in range(num_pts):
            rel_x = i / (num_pts - 1)
            # Forme de base en cloche (plus haut au centre)
            dist_center = 1.0 - abs(rel_x - 0.5) * 2 
            # Ajout de pics aléatoires escarpés
            h_var = random.uniform(0.7, 1.0) if 0.2 < rel_x < 0.8 else random.uniform(0.2, 0.5)
            self.points.append((rel_x, dist_center * h_var))

    def move(self):
        self.x -= self.speed

    def draw(self, win, t):
        # Couleurs inspirées de ton image
        rock_col = (100, 120, 150)
        shadow_col = (70, 85, 110)
        snow_col = (255, 255, 255)
        night_col = (10, 15, 30)

        def get_c(col):
            # Interpolation pour le cycle jour/nuit
            return (int(col[0]*(1-t) + night_col[0]*t), 
                    int(col[1]*(1-t) + night_col[1]*t), 
                    int(col[2]*(1-t) + night_col[2]*t))

        # Conversion des points relatifs en coordonnées écran
        pts = [(self.x + p[0]*self.width, HEIGHT - p[1]*self.height) for p in self.points]
        
        # 1. DESSIN DU CORPS (Face éclairée)
        full_poly = [(self.x, HEIGHT)] + pts + [(self.x + self.width, HEIGHT)]
        pygame.draw.polygon(win, get_c(rock_col), full_poly)

        # 2. DESSIN DES OMBRES (Relief 3D)
        # On assombrit les versants qui descendent vers la droite
        for i in range(len(pts)-1):
            p1, p2 = pts[i], pts[i+1]
            if p2[1] > p1[1]: # La pente descend
                pygame.draw.polygon(win, get_c(shadow_col), [p1, p2, (p2[0], HEIGHT), (p1[0], HEIGHT)])

        # 3. DESSIN DE LA NEIGE (Sur chaque sommet)
        for i in range(len(pts)):
            px, py = pts[i]
            # Si le pic est assez haut, on met une coiffe de neige
            if self.points[i][1] > 0.35:
                s_w = 40 * self.points[i][1] # Largeur neige
                s_h = 70 * self.points[i][1] # Hauteur neige
                # Triangle de neige qui épouse le sommet
                s_poly = [(px, py), (px + s_w, py + s_h), (px - s_w, py + s_h)]
                pygame.draw.polygon(win, get_c(snow_col), s_poly)

        # 4. NEIGE ÉPARPILLÉE (Petites plaques losanges)
        # On en place quelques-unes aléatoirement sur les versants
        for i in range(3):
            # Utilise un index de point existant pour être "sur" la montagne
            idx = random.randint(1, len(pts)-2)
            tx, ty = pts[idx][0], pts[idx][1] + 80
            if ty < HEIGHT - 20:
                pygame.draw.polygon(win, get_c(snow_col), [(tx, ty-12), (tx+8, ty), (tx, ty+12), (tx-8, ty)])

mountains = [Mountain() for _ in range(3)]

class TreeGroup:
    def __init__(self, x, speed, hill_height):
        self.x = x
        self.speed = speed
        self.y_base = HEIGHT - hill_height + 10
        # On crée 3 à 5 arbres par groupe
        self.trees = []
        for _ in range(random.randint(3, 5)):
            off_x = random.randint(0, 80)
            off_y = random.randint(0, 15)
            self.trees.append({'ox': off_x, 'oy': off_y, 'h': random.randint(20, 40)})

    def move(self):
        self.x -= self.speed
        if self.x < -150: self.x = WIDTH + random.randint(100, 400)

    def draw(self, win, t):
        trunk_col = (80, 50, 30)
        leaf_col = (34, 139, 34)
        for tr in self.trees:
            tx, ty = self.x + tr['ox'], self.y_base + tr['oy']
            pygame.draw.rect(win, trunk_col, (tx, ty, 6, tr['h'])) # Tronc
            pygame.draw.circle(win, leaf_col, (tx + 3, ty), tr['h'] // 2 + 5) # Feuilles

# -------------------- Bird --------------------
class Bird:
    def __init__(self):
        self.x=100; self.y=HEIGHT//2; self.v=0; self.w=48; self.h=36
        self.angle=0; self.wing_angle=0; self.wing_dir=1
    def jump(self):
        self.v = BIRD_JUMP
        if volume_on and SOUND_JUMP: SOUND_JUMP.play()
    def move(self):
        self.v += GRAVITY; self.y += self.v
        self.angle = max(-45, min(45, -self.v*3))
        self.wing_angle += self.wing_dir * 3
        if abs(self.wing_angle) > 18: self.wing_dir *= -1
    def get_skin_colors(self, selected_skin, unlocked_map, best_score, t_anim):
        if unlocked_map.get(GOLD_SKIN[0], False) and best_score >= GOLD_SKIN[2]:
            c = GOLD_SKIN[1]; return c, tuple(max(0,int(cc*0.8)) for cc in c), (240,200,60), "gold"
        if selected_skin == "Rainbow" and unlocked_map.get("Rainbow", False): return None, None, BLACK, "rainbow"
        for name,col,thr in SKINS:
            if name == selected_skin and unlocked_map.get(name, False):
                wing = tuple(max(0,int(cc*0.8)) for cc in col); out = BLACK if name != "Black" else (80,80,80)
                return col, wing, out, None
        return SKINS[0][1], (200,180,0), BLACK, None

    def draw(self, win, score, best_score, unlocked_map, selected_skin, t_anim=0.0, death_mode=False):
        body_col, wing_col, outline_col, special = self.get_skin_colors(selected_skin, unlocked_map, best_score, t_anim)
        surf = pygame.Surface((self.w*2+40, self.h*2+40), pygame.SRCALPHA)
        cx, cy = self.w+20, self.h+20
        
        # --- NOUVELLE QUEUE DYNAMIQUE (3 Plumes) ---
        for i, angle_off in enumerate([-15, 0, 15]):
            tail_angle = math.sin(t_anim * 8 + i) * 10 + angle_off
            tail_surf = pygame.Surface((35, 20), pygame.SRCALPHA)
            pygame.draw.ellipse(tail_surf, outline_col, (0, 5, 30, 10)) # Contour plume
            pygame.draw.ellipse(tail_surf, body_col, (2, 7, 26, 6))    # Couleur plume
            t_rot = pygame.transform.rotate(tail_surf, tail_angle)
            surf.blit(t_rot, (cx - 48, cy - 10 + (i*5)))

        # Corps principal
        pygame.draw.ellipse(surf, outline_col, (cx-26, cy-18, 54, 38))
        if special == "rainbow":
            colors = [(255,0,0),(255,127,0),(255,255,0),(0,255,0),(0,0,255),(148,0,211)]
            shift = int((t_anim*40) % 100)
            for i,col in enumerate(colors):
                dx = -40 + i*14 + (shift % 14)
                pygame.draw.ellipse(surf, col, (cx-26+dx, cy-16, 52, 34))
        else:
            pygame.draw.ellipse(surf, body_col, (cx-24, cy-16, 50, 34))
            pygame.draw.ellipse(surf, (min(255, body_col[0]+40), min(255, body_col[1]+40), min(255, body_col[2]+40)), (cx-18, cy-14, 30, 10))

        # Aile
        w_offset = int(math.sin(t_anim*10)*5)
        pygame.draw.ellipse(surf, outline_col, (cx-14, cy-4 + w_offset, 32, 22))
        pygame.draw.ellipse(surf, wing_col if wing_col else (200,120,0), (cx-12, cy-4 + w_offset, 28, 18))
        
        # Bec
        pygame.draw.polygon(surf, BLACK, [(cx+18, cy), (cx+36, cy+8), (cx+18, cy+14)])
        pygame.draw.polygon(surf, ORANGE, [(cx+16, cy+2), (cx+32, cy+8), (cx+16, cy+12)])
        pygame.draw.line(surf, BLACK, (cx+18, cy+8), (cx+28, cy+8), 2)

        # Œil
        pygame.draw.circle(surf, WHITE, (cx+10, cy-8), 10)
        pygame.draw.circle(surf, BLACK, (cx+13, cy-8), 5)
        pygame.draw.circle(surf, WHITE, (cx+14, cy-10), 2)
        
        # --- AJOUT DU SOURCIL ---
        if not death_mode:
            # Sourcil "déterminé"
            pygame.draw.ellipse(surf, BLACK, (cx + 5, cy - 20, 18, 7))
        else:
            pygame.draw.line(surf, RED, (cx+4, cy-12), (cx+16, cy-4), 3)
            pygame.draw.line(surf, RED, (cx+16, cy-12), (cx+4, cy-4), 3)

        rotated = pygame.transform.rotate(surf, self.angle)
        win.blit(rotated, rotated.get_rect(center=(self.x, self.y)).topleft)

# -------------------- Environment --------------------
class Hill:
    def __init__(self, color, height, speed, depth_factor):
        self.x = 0
        self.color = color
        self.height = height
        self.speed = speed
        self.depth_factor = depth_factor
        # Détails d'herbe aléatoires
        self.grass = [(random.randint(0, WIDTH), random.randint(0, 40)) for _ in range(15)]

    def move(self):
        self.x -= self.speed
        if self.x <= -WIDTH: self.x = 0

    def draw(self, win, t):
        night_col = (int(self.color[0]*0.1), int(self.color[1]*0.1), int(self.color[2]*0.2))
        current_col = [int(self.color[i]*(1-t) + night_col[i]*t) for i in range(3)]

        for offset in [0, WIDTH]:
            # Dessin de la colline
            rect = (self.x + offset - 50, HEIGHT - self.height, WIDTH + 100, self.height * self.depth_factor)
            pygame.draw.ellipse(win, current_col, rect)
            
# Listes de décor
hills = [
    Hill((45, 120, 45), 180, 0.5, 2.5), 
    Hill((60, 160, 60), 120, 1.2, 2.0),
    Hill((80, 200, 80), 70, 2.0, 1.5)
]
mountains = [Mountain() for _ in range(3)]
tree_groups = [
    TreeGroup(random.randint(0, WIDTH), 1.2, 120),
    TreeGroup(random.randint(WIDTH, WIDTH*2), 2.0, 70)
]

def draw_background(win, clouds, stars, t=0.0):
    # 1. Ciel
    r = int(BLUE_LIGHT[0]*(1-t) + BLUE_DARK[0]*t)
    g = int(BLUE_LIGHT[1]*(1-t) + BLUE_DARK[1]*t)
    b = int(BLUE_LIGHT[2]*(1-t) + BLUE_DARK[2]*t)
    win.fill((r,g,b))

    # 2. Étoiles & Nuages
    if t > 0.1:
        for s in stars: s.draw(win, int(255*t))
    if t < 0.9:
        for c in clouds: c.move(); c.draw(win)

    # 3. Montagnes (Lointain)
    for m in mountains:
        m.move()
        if m.x + m.width < 0: # Réapparition aléatoire
            m.__init__() 
        m.draw(win, t)

    # 4. Collines & Arbres
    # On alterne pour que les arbres soient sur les bonnes collines
    hills[0].move(); hills[0].draw(win, t) # Colline arrière
    
    hills[1].move(); hills[1].draw(win, t) # Colline milieu
    tree_groups[0].move(); tree_groups[0].draw(win, t) # Arbres milieu
    
    hills[2].move(); hills[2].draw(win, t) # Colline avant
    tree_groups[1].move(); tree_groups[1].draw(win, t) # Arbres devant

# -------------------- Save handling --------------------
def load_save():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if all(k in data for k in ["best_score", "unlocked_map", "selected_skin"]): return data
        except: pass
    unlocked = {s[0]: False for s in SKINS}; unlocked[SKINS[0][0]] = True
    unlocked[GOLD_SKIN[0]] = False; unlocked["secret"] = False
    return {"best_score": 0, "unlocked_map": unlocked, "selected_skin": SKINS[0][0]}

def save_game(data):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=2)
    except: pass

# -------------------- Menus --------------------
def play_music(m_file):
    if volume_on and safe_music_load(m_file):
        pygame.mixer.music.set_volume(0.5); pygame.mixer.music.play(-1)

def menu_loop(save_data, current_easter):
    global volume_on
    best_score, unlocked_map, selected_skin = save_data["best_score"], save_data["unlocked_map"], save_data["selected_skin"]
    clouds, stars, pipes = [Cloud() for _ in range(5)], [Star() for _ in range(30)], [Pipe(WIDTH//2), Pipe(WIDTH//2+250)]
    bird = Bird(); bird.x, bird.y, pulse = WIDTH//2, 150, 0.0
    stop_music(); play_music(MENU_MUSIC)
    while True:
        clock.tick(FPS); pulse += 0.1; mx, my = pygame.mouse.get_pos()
        t = 1.0 if unlocked_map.get("secret", False) or best_score >= 50 else 0.0
        draw_background(WINDOW, clouds, stars, t)
        for p in pipes: p.move(); p.draw(WINDOW)
        draw_text_outline(WINDOW, "Floppy Burd", TITLE_FONT, YELLOW, BLACK, (WIDTH//2, 100))
        draw_text_outline(WINDOW, current_easter, get_easter_font(current_easter), WHITE, BLACK, (WIDTH//2, 180), -10)
        bird.draw(WINDOW, 0, best_score, unlocked_map, selected_skin, time.time())
        play_rect = pygame.Rect(WIDTH//2 - int(110*(1+0.05*math.sin(pulse))), 340, int(220*(1+0.05*math.sin(pulse))), 64)
        quit_rect = pygame.Rect(WIDTH//2 - 80, play_rect.bottom + 12, 160, 50)
        draw_button(WINDOW, play_rect, "Play", play_rect.collidepoint(mx,my))
        draw_button(WINDOW, quit_rect, "QUIT", quit_rect.collidepoint(mx,my), (230,80,80))
        any_cust = any(unlocked_map.get(n, False) for n,_,_ in SKINS[1:]) or unlocked_map.get(GOLD_SKIN[0], False)
        cust_rect = pygame.Rect(WIDTH//2-130, quit_rect.bottom+12, 260, 56) if any_cust else None
        if cust_rect: draw_button(WINDOW, cust_rect, "Customize", cust_rect.collidepoint(mx,my))

        # (Lignes existantes pour le score)
        y_low = (cust_rect.bottom if cust_rect else quit_rect.bottom) + 12
        WINDOW.blit(FONT.render(f"Best: {best_score}", True, WHITE), (WIDTH//2-50, y_low))
        
        # --- AJOUT DES CRÉDITS ET DU LOGO ---
        # Musique en bas à gauche
        music_credits = STUDIO_FONT.render("Musics by 3th4ncz4p", True, WHITE)
        WINDOW.blit(music_credits, (10, HEIGHT - 30))
        
        # Logo en bas à droite (avec 10px de marge)
        logo_rect = LOGO_STUDIO.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
        WINDOW.blit(LOGO_STUDIO, logo_rect)
    
        # BOUTON WIPE SAVE (Haut à gauche)
        wipe_rect = pygame.Rect(10, 10, 55, 55)
        draw_trash_icon(WINDOW, wipe_rect, wipe_rect.collidepoint(mx, my))
        
        # BOUTON VOLUME AVEC HAUT-PARLEUR
        vol_rect = pygame.Rect(WIDTH - 60, 10, 50, 50)
        draw_volume_icon(WINDOW, vol_rect)
        
        y_low = (cust_rect.bottom if cust_rect else quit_rect.bottom) + 12
        WINDOW.blit(FONT.render(f"Best: {best_score}", True, WHITE), (WIDTH//2-50, y_low))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: save_game(save_data); pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if play_rect.collidepoint(mx,my): return "play"
                if quit_rect.collidepoint(mx,my): save_game(save_data); pygame.quit(); sys.exit()
                if cust_rect and cust_rect.collidepoint(mx,my): return "customize"
                if vol_rect.collidepoint(mx,my):
                    volume_on = not volume_on
                    if volume_on: play_music(MENU_MUSIC)
                    else: pygame.mixer.music.stop()
                if wipe_rect.collidepoint(mx, my):
                    # Appel de la boîte de confirmation
                    if show_confirm_dialog(save_data):
                        # Réinitialisation si l'utilisateur a cliqué sur le vert
                        unlocked = {s[0]: False for s in SKINS}
                        unlocked[SKINS[0][0]] = True
                        unlocked[GOLD_SKIN[0]] = False
                        unlocked["secret"] = False
                        save_data.update({"best_score": 0, "unlocked_map": unlocked, "selected_skin": SKINS[0][0]})
                        save_game(save_data)
                        if volume_on and SOUND_HIT: SOUND_HIT.play()
                        return "menu"
                    # Si "Non", on ne fait rien et on continue la boucle du menu
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE: return "play"

def customization_menu(save_data):
    unlocked_map, selected_skin = save_data["unlocked_map"], save_data["selected_skin"]
    clouds, stars, bird = [Cloud() for _ in range(4)], [Star() for _ in range(20)], Bird()
    bird.x, bird.y, chosen = WIDTH//2, 170, selected_skin
    unlocked_list = [s for s in SKINS if unlocked_map.get(s[0], False)]
    if unlocked_map.get(GOLD_SKIN[0], False): unlocked_list.append(GOLD_SKIN)
    skin_buttons = []
    for idx, sk in enumerate(unlocked_list):
        r = pygame.Rect(WIDTH//2-165 + (idx%3)*118, 220 + (idx//3)*110, 100, 92)
        skin_buttons.append((r, sk))
    apply_r = pygame.Rect(WIDTH//2-130, 550, 120, 50); back_r = pygame.Rect(WIDTH//2+10, 550, 120, 50)
    while True:
        clock.tick(FPS); mx, my = pygame.mouse.get_pos()
        draw_background(WINDOW, clouds, stars, 1.0 if unlocked_map.get("secret", False) else 0.0)
        draw_text_outline(WINDOW, "Skins", TITLE_FONT, YELLOW, BLACK, (WIDTH//2, 90))
        for r, sk in skin_buttons:
            pygame.draw.rect(WINDOW, BLACK, r.inflate(8,8), border_radius=6)
            if sk[0] == "Rainbow": 
                for i,c in enumerate([(255,0,0),(255,127,0),(255,255,0),(0,255,0),(0,0,255),(148,0,211)]):
                    pygame.draw.rect(WINDOW, c, (r.x, r.y+i*15, r.width, 16))
            else: pygame.draw.rect(WINDOW, sk[1] if sk[1] else (255,255,255), r, border_radius=6)
            if chosen == sk[0]: pygame.draw.rect(WINDOW, (255,215,0), r, 4, border_radius=6)
        bird.draw(WINDOW, 0, 999, {chosen:True}, chosen, time.time())
        draw_button(WINDOW, apply_r, "Select", apply_r.collidepoint(mx,my))
        draw_button(WINDOW, back_r, "Back", back_r.collidepoint(mx,my))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: save_game(save_data); pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if apply_r.collidepoint(mx,my): save_data["selected_skin"] = chosen; save_game(save_data); return
                if back_r.collidepoint(mx,my): return
                for r, sk in skin_buttons:
                    if r.collidepoint(mx,my): chosen = sk[0]

def game_over_menu(score, save_data, current_easter):
    bird = Bird(); bird.x, bird.y = WIDTH//2, 150
    stop_music()
    while True:
        clock.tick(FPS); mx, my = pygame.mouse.get_pos()
        draw_background(WINDOW, [], [], 1.0 if save_data["best_score"] >= 50 else 0.0)
        draw_text_outline(WINDOW, "Game Over", TITLE_FONT, YELLOW, BLACK, (WIDTH//2, 100))
        draw_text_outline(WINDOW, current_easter, get_easter_font(current_easter), WHITE, BLACK, (WIDTH//2, 170), -10)
        bird.draw(WINDOW, 0, 0, save_data["unlocked_map"], save_data["selected_skin"], time.time(), True)
        p_r, b_r = pygame.Rect(WIDTH//2-110, 300, 220, 60), pygame.Rect(WIDTH//2-110, 380, 220, 60)
        draw_button(WINDOW, p_r, "Restart", p_r.collidepoint(mx,my))
        draw_button(WINDOW, b_r, "Menu", b_r.collidepoint(mx,my))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: save_game(save_data); pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if p_r.collidepoint(mx,my): return "play_again"
                if b_r.collidepoint(mx,my): return "menu"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE: return "play_again"

# -------------------- Game Round --------------------
def play_round(save_data):
    bird, pipes = Bird(), [Pipe(WIDTH+200)]
    clouds, stars = [Cloud() for _ in range(5)], [Star() for _ in range(30)]
    score, particles, confettis = 0, [], []
    current_t = 1.0 if save_data["unlocked_map"].get("secret", False) else 0.0
    stop_music(); play_music(GAME_MUSIC)
    while True:
        clock.tick(FPS)
        
        # --- REMPLACEZ L'ANCIEN BLOC DE TRANSITION PAR CELUI-CI ---
        # On définit la cible (où on veut arriver)
        target_t = 1.0 if save_data["unlocked_map"].get("secret", False) else min(score/50, 1.0)
        
        # On approche doucement de la cible (interpolation)
        current_t += (target_t - current_t) * 0.05 
        
        # On dessine avec la valeur lissée
        draw_background(WINDOW, clouds, stars, current_t)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: save_game(save_data); pygame.quit(); sys.exit()
            if (e.type==pygame.KEYDOWN and e.key==pygame.K_SPACE) or (e.type==pygame.MOUSEBUTTONDOWN and e.button==1): bird.jump()
        bird.move(); bird.draw(WINDOW, score, save_data["best_score"], save_data["unlocked_map"], save_data["selected_skin"], time.time())
        add_p, rem, dead = False, [], False
        for p in pipes:
            p.move(); p.draw(WINDOW)
            if p.collide(bird): dead = True
            if p.x + p.width < 0: rem.append(p)
            if p.x + p.width < bird.x and not p.scored:
                score += 1; p.scored = True
                if score > save_data["best_score"]:
                    for _ in range(15): confettis.append(Confetti(bird.x, bird.y))
            if p.x == WIDTH//2: add_p = True
        if add_p: pipes.append(Pipe(WIDTH+50))
        for r in rem: pipes.remove(r)
        if bird.y < 0 or bird.y > HEIGHT or dead:
            if volume_on and SOUND_HIT: SOUND_HIT.play()
            if volume_on and SOUND_GAMEOVER: SOUND_GAMEOVER.play()
            pygame.time.delay(400); return score
        for pr in particles[:]:
            pr.move(); pr.draw(WINDOW)
            if pr.life <= 0: particles.remove(pr)
        for cf in confettis[:]:
            cf.move(); cf.draw(WINDOW)
            if cf.life <= 0: confettis.remove(cf)
        WINDOW.blit(FONT.render(f"Score: {score}", True, WHITE), (10,10)); pygame.display.update()

# -------------------- Main --------------------
def main():
    save_data = load_save()
    while True:
        action = menu_loop(save_data, random.choice(EASTER_TEXTS))
        if action == "play":
            score = play_round(save_data)
            if score > save_data["best_score"]: save_data["best_score"] = score
            for name,_,thr in SKINS:
                if save_data["best_score"] >= thr: save_data["unlocked_map"][name] = True
            if save_data["best_score"] >= 500: save_data["unlocked_map"]["Gold"] = True
            if save_data["best_score"] >= 50: save_data["unlocked_map"]["secret"] = True
            save_game(save_data)
            if game_over_menu(score, save_data, random.choice(EASTER_TEXTS)) == "menu": continue
        elif action == "customize": customization_menu(save_data)

if __name__ == "__main__":
    try: main()
    except: pygame.quit(); sys.exit()




