import os
import sys
import pygame as pg
from random import randint

WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP:(0, -5), 
    pg.K_DOWN:(0, 5), 
    pg.K_LEFT:(-5, 0), 
    pg.K_RIGHT:(5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    #こうかとん描画設定
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0) #rotozoomは拡大している
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    #爆弾の描画設定
    bom = pg.Surface((20, 20))
    pg.draw.circle(bom, (255, 0, 0), (10, 10), 10)
    bom.set_colorkey((0, 0, 0))
    bom_rct = bom.get_rect()
    bom_rct.center = randint(0, WIDTH), randint(0, HEIGHT)
    vx, vy = 5, 5
 
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
    
        bom_rct.move_ip(vx, vy)
        screen.blit(bom, bom_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
