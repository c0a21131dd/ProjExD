import pygame as pg
import sys
from tkinter import messagebox as tkm
import time
import random
import tkinter as tk

def timer(st): # タイマー関数
    nowtm = time.time() - st
    nowtm//=1
    return int(nowtm)

def check_bound(obj_rct,scr_rct): #衝突チェック関数
    yoko,tate = +1,+1
    if obj_rct.left < scr_rct.left or obj_rct.right > scr_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or obj_rct.bottom > scr_rct.bottom:
        tate = -1
    return yoko, tate

def create_boms(scrn_rct, l): #爆弾作成関数
    new_bomb_sfc = pg.Surface((20,20))
    new_bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(new_bomb_sfc, (255, 0, 0), (10, 10), 10)
    new_bomb_rct = new_bomb_sfc.get_rect()
    new_bomb_rct.center = random.randint(0, scrn_rct.width-10), random.randint(0, scrn_rct.height-10)
    move_x = random.randint(1,3)
    move_y = random.randint(1,3)
    l.append([new_bomb_sfc,new_bomb_rct,move_x,move_y])

def main(st):
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    bakuhatu_sfc = pg.image.load("fig/bakuhatsu.png") #爆発画像ロード
    bakuhatu_sfc = pg.transform.rotozoom(bakuhatu_sfc,0, 0.2)

    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = scrn_rct.width/2 ,scrn_rct.height/2
    scrn_sfc.blit(tori_sfc,tori_rct)

    bomss = [] #爆弾リスト
    create_boms(scrn_rct,bomss)

    clock = pg.time.Clock()
    font = pg.font.Font(None, 50)
    MOUSE_MODE = False #マウス操作モードフラグ

    while True:
        scrn_sfc.blit(bg_sfc,bg_rct)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1: #マウス操作モード判定
                MOUSE_MODE = not MOUSE_MODE
            elif event.type == pg.KEYDOWN:#エスケープキー終了
                if event.key == pg.K_ESCAPE:
                    return

        key_dct = pg.key.get_pressed() #こうかとん移動操作
        key_type = [pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT]
        MOVE_tipe = [[0,-1],[0,1],[-1,0],[1,0]]
        if check_bound(tori_rct, scrn_rct) != (1,1):
            MOVE_tipe = [[0,5],[0,-5],[5,0],[-5,0]]
        if MOUSE_MODE:
            tori_rct.centerx, tori_rct.centery = event.pos
            text = font.render("MOUSEMODE ON", True, (0,0,0))
            scrn_sfc.blit(text, [scrn_rct.width/2,10])
        else:
            for i,KEY in enumerate(key_type):
                if key_dct[KEY]:
                    tori_rct.centerx += MOVE_tipe[i][0]
                    tori_rct.centery += MOVE_tipe[i][1]
        scrn_sfc.blit(tori_sfc,tori_rct)

        for bomb in bomss: #爆弾操作
            if check_bound(bomb[1], scrn_rct) == (-1,1):
                bomb[2] *= -1
            elif check_bound(bomb[1], scrn_rct) == (1,-1):
                bomb[3] *= -1

            bomb[1].move_ip(bomb[2], bomb[3])
            scrn_sfc.blit(bomb[0], bomb[1])

            if bomb[1].colliderect(tori_rct):#衝突判定
                scrn_sfc.blit(bg_sfc,bg_rct)
                scrn_sfc.blit(bakuhatu_sfc,tori_rct)#爆発描写
                pg.display.update()
                return

        if timer(st) > len(bomss)*5: #爆弾作成判定
            create_boms(scrn_rct,bomss)

        text = font.render(f"ScoreTime{timer(st)}", True, (0,0,0)) #スコア表示
        scrn_sfc.blit(text, [10, 10])
        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    st = time.time()
    main(st)
    root = tk.Tk()
    root.withdraw()
    score = timer(st)
    with open('ex04/text.txt',mode = "r", encoding="UTF-8") as file:# ハイスコア読み込み
        for num in file.readline():
            print(type(num))
            HISCORE = int(num)

    if score > HISCORE:#ハイスコア判定と書き込み
        with open('ex04/text.txt',mode = "w", encoding="UTF-8") as file:
            file.write(f"{score}")
        tkm.showinfo("Hit", f"ハイスコア:{HISCORE}秒  生存時間:{score}秒")
        tkm.showinfo("Hit", "ハイスコア更新おめでとう！")
        sys.exit()

    tkm.showinfo("Hit", f"ハイスコア:{HISCORE}秒  生存時間:{score}秒")#最終結果表示
    tkm.showinfo("Hit", "次も頑張ろう！")
    pg.quit()
    sys.exit()
