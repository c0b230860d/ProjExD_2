import os
import sys
import pygame as pg
import time
from random import randint

WIDTH, HEIGHT = 1600, 900
# WIDTH, HEIGHT = 1280, 720
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {  # 移動量辞書
    pg.K_UP:(0, -5), 
    pg.K_DOWN:(0, 5), 
    pg.K_LEFT:(-5, 0), 
    pg.K_RIGHT:(5, 0),
}

def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectまたは爆弾Rect
    戻り値:タプル(横方向判定結果, 縦方向判定結果)
    画面内ならTrue, 画面外ならFalseを返す
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:  # 横判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 縦判定
        tate = False
    return yoko, tate

def roll_dori() -> dict:
    """
    引数:なし
    戻り値:辞書を返す
    """
    ROTE = {  # 回転量辞書
    (-5, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
    (-5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0),
    (0, -5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 90, 2.0),
    (5, -5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 45, 2.0),
    (5, 0):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 0, 2.0),
    (5, 5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), -45, 2.0),
    (0, 5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), -90, 2.0),
    (-5, 5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0),
    }
    return ROTE

def end_game(screen)->None:
    """
    引数:screen
    戻り値:なし
    ゲームオーバー画面を表示
    """
    # blackアウト
    end_window = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(end_window,(0, 0, 0),(0, 0, WIDTH, HEIGHT))
    end_window.set_alpha(80)
    end_rct = end_window.get_rect()
    end_rct.center = WIDTH/2, HEIGHT/2
    screen.blit(end_window, end_rct)
    # ゲームオーバーを表示
    font = pg.font.Font(None, 80)  # フォント設定   
    txt = font.render("Game Over", True, (255, 255, 255))
    screen.blit(txt, [WIDTH/2-120, HEIGHT/2-40])
    #泣いてるこうかとんの表示
    kk_cly = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    screen.blit(kk_cly,[WIDTH/4+30, HEIGHT/2-60])
    screen.blit(kk_cly,[3*WIDTH/4-30, HEIGHT/2-60])
    pg.display.update()
    time.sleep(5)

def add_speed_size()->tuple:
    """
    引数:なし
    戻り値：タプル(加速度リスト, 拡大リスト)
    """
    accs = [a for a in range(1, 11)]  # 加速度リスト
    bb_imgs = []
    for r in range(1, 11):
        bom = pg.Surface((20*r, 20*r))
        pg.draw.circle(bom, (255, 0, 0), (10*r, 10*r), 10*r)
        bom.set_colorkey((0, 0, 0))
        bb_imgs.append(bom)

    return accs, bb_imgs
        
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
        # 衝突判定    
        if kk_rct.colliderect(bom_rct):
            print("\\\こうかとんは焼き鳥になりました🍗//")
            add_speed_size()
            end_game(screen)  # ゲームオーバー画面を呼び出す
            return

        # 背景を表示
        screen.blit(bg_img, [0, 0])

        #拡大と加速
        bb_accs, bom_imgs = add_speed_size()
        avx = vx * bb_accs[min(tmr//500, 9)]
        bom = bom_imgs[min(tmr//500, 9)]

         
        # こうかとんのキー操作と壁判定
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items(): # 移動量
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        # print(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        if sum_mv != [0, 0]:
            kk_img = roll_dori()[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)

        # 爆弾の描画と壁判定
        bom_rct.move_ip(avx, vy)
        screen.blit(bom, bom_rct)
        yoko, tate = check_bound(bom_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1

        pg.display.update()
        tmr += 1
        clock.tick(50)
    
    


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
