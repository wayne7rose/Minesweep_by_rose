import pygame as pg
from pygame.locals import *
import minesweep
import sys
import time


#  鼠标的位置pos --> position 
def pos_position(pos):
    left = (pos[0] // 20) * 20 + 2
    top = (pos[1] // 20) * 20 + 2
    return (left, top)

#  格子位置point --> position
def point_position(point, x):
    left = (point % x) * 20 + 2
    top = (point // x) * 20 + 2
    return (left, top)

#  鼠标位置pos --> 格子位置point
def pos_point(pos, x):
    point = pos[0]//20 + x * (pos[1]//20)
    return point


def main():
    # ------------------ 设置三种游戏难度 ---------------------------------------------
    easy_x, easy_y, easy_mines = 10, 10, 10
    normal_x, normal_y, normal_mines = 20, 15, 40
    hard_x, hard_y, hard_mines = 30, 20, 100
    # ---------------------------------------------------------------------------------

    # 一些控制流程变量的初始化，以及创建扫雷实例对象
    pg.init()
    start = True
    init = False
    win = False
    delay = 0
    x0, y0 = 200, 200
    mine_sweep = minesweep.MineSweep(10, 10, 10)
    screen = pg.display.set_mode((x0, y0))
    pg.display.set_caption("Minesweep - by rose")
    clock = pg.time.Clock()   
    
    # 载入图片
    bg0 = pg.image.load("image/bg0.png").convert_alpha()    # 整个背景
    bg1 = pg.image.load("image/bg1.png").convert_alpha()    # 一格，未翻开
    bg2 = pg.image.load("image/bg2.png").convert_alpha()    # 一格，翻开
    boom_mine = pg.image.load("image/boom_mine.png").convert_alpha()    # 炸雷
    mine_image = pg.image.load("image/mine.png").convert_alpha()
    flag_image = pg.image.load("image/flag.png").convert_alpha()
    start_image = start_notpress_image = pg.image.load("image/start_notpress.png").convert_alpha()
    start_press_image = pg.image.load("image/start_press.png").convert_alpha()
    start_image_rect = start_image.get_rect()

    # 载入音效
    win_sound = pg.mixer.Sound("music/win.wav")
    win_sound.set_volume(0.2)
    boom_sound = pg.mixer.Sound("music/boom.wav")
    boom_sound.set_volume(0.2)
        
    # show[]表示每个格子的显示：show[0]表示翻开是空白，[1-8]表示显示1-8, [9]-->mine, [10]-->flag
    font = pg.font.SysFont('TimesNewman', 26)
    font2 = pg.font.SysFont('arial', 16)
    font3 = pg.font.SysFont('colonna', 26)
    GREY = (122, 122, 122)
    show = []
    show.append(font.render('', True, GREY))
    for i in range(8):
        show.append(font.render(' '+str(i+1), True , (80* (i%4), 50, 255- 80* (i%4))))
    show.append(mine_image)
    show.append(flag_image)


    # 难易程度按钮初始化
    mode = []
    choose_mode = []
    mode.append(font2.render("Easy:   "+str(easy_x)+" × "+str(easy_y)+" ,  "+str(easy_mines)+" mines" ,True, (0, 0, 0)))
    choose_mode.append(mode[-1])
    mode.append(font2.render("Normal: "+str(normal_x)+" × "+str(normal_y)+" ,  "+str(normal_mines)+" mines" ,True, (0, 0, 0)))
    choose_mode.append(mode[-1])
    mode.append(font2.render("Hard:   "+str(hard_x)+" × "+str(hard_y)+" , "+str(hard_mines)+" mines" ,True, (0, 0, 0)))
    choose_mode.append(mode[-1])
    mode.append(font2.render("Easy:   "+str(easy_x)+" × "+str(easy_y)+" ,  "+str(easy_mines)+" mines" ,True, (255, 0, 0)))
    mode.append(font2.render("Normal: "+str(normal_x)+" × "+str(normal_y)+" ,  "+str(normal_mines)+" mines" ,True, (255, 0, 0)))
    mode.append(font2.render("Hard:   "+str(hard_x)+" × "+str(hard_y)+" , "+str(hard_mines)+" mines" ,True, (255, 0, 0)))
    choose_mode_rect = []
    for i in range(3):
        choose_mode_rect.append(choose_mode[i].get_rect())       

    
    # ------------------------------------ 主 循 环 -----------------------------------------------------
    while True:
        if start:  # ----------------- 难易程序选择界面 ----------------------------------
            win = False
            is_first = True
            game_over = False
            screen.blit(bg0, (0, 0))
            
            for i in range(3):
                choose_mode_rect[i].left = x0 / 2 - 80
                choose_mode_rect[i].top = y0 / 2 - 40 + i*20
                screen.blit(choose_mode[i], (choose_mode_rect[i].left, choose_mode_rect[i].top))                
                
        if init:  # ------------------ 根据难易程度，画背景和格子，reset 地雷--------------
            start = False
            init = False
            sweep_times = 0
            remaining_mine = mine_num
            bgsize = x0, y0 = 20 * x + 2, 20 * y + 26
            screen = pg.display.set_mode(bgsize)
            screen.blit(bg0, (0, 0))
            start_image_rect.left, start_image_rect.top  = x0/2 - 12, y0 - 24
            
            for i in range(y + 1):
                pg.draw.line(screen, GREY, (0, i * 20), (x * 20, i * 20), 2)
            for i in range(x + 1):
                pg.draw.line(screen, GREY, (i * 20, 0), (i * 20, y * 20), 2)

            mine_sweep.reset(x, y, mine_num)
            mine_sweep.bury_mine()
            start_time = time.time()

            '''
            # 设置扫雷面积 x * y
            global x
            global y
            x = int(input("请输入横格数:"))
            y = int(input("请输入纵格数:"))
            mine_num = int(input("请输入地雷的个数:"))
            '''
        
        if game_over:  # ------------- 显示所有格子信息，是否重新开始选择界面 --------------
            for i in range(x*y):
                screen.blit(bg2, point_position(i, x))
                screen.blit(show[mine_sweep.list_cue[i]], point_position(i, x))
                if mine_sweep.flag[i] == 1:
                    if mine_sweep.list_cue[i] != 9:
                        screen.blit(mine_image, point_position(i, x))
                        pg.draw.line(screen, (255, 0, 0), point_position(i, x), point_position(i+x+1, x), 4)
                        pg.draw.line(screen, (255, 0, 0), point_position(i+1, x), point_position(i+x, x), 4)
                    else:
                        screen.blit(flag_image, point_position(i, x))
            if not win:
                screen.blit(boom_mine, point_position(boom_point, x))
            

        if win:   # ------------------- 通关祝贺五毛特效 ----------------------------------
            win1 = font3.render("Congratulation !" ,True, (255, 0, 0))
            win2 = font3.render("You Win !" ,True, (255, 0, 0))
            remaining_mine = 0
            if is_first:
                win_sound.play()
                is_first = False
            if delay < 7:
                screen.blit(win1, (x0 / 2 - 80, y0 / 4))
                screen.blit(win2, (x0 / 2 - 60, y0 / 4 + 50))

                
        # --------------------------------- 用户鼠标事件 ----------------------------------    
        for event in pg.event.get():  
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            # ----------- start 和 game over 界面选择菜单时 鼠标悬停特效 ------------------
            if event.type == MOUSEMOTION: 
                for i in range(3):
                    if choose_mode_rect[i].collidepoint(event.pos):
                        choose_mode[i] = mode[i+3]
                    else:
                        choose_mode[i] = mode[i]

            if event.type == MOUSEBUTTONUP:
                if event.button == 1 and not start:
                    start_image = start_notpress_image
                    if start_image_rect.collidepoint(event.pos):
                        start = True

            if event.type == MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed() == (True, False, False):
                    if not start:
                        if start_image_rect.collidepoint(event.pos):
                            start_image = start_press_image
                        

                    # --------------------- 游戏时 : 翻格子找雷 ------------------------------
                    if not game_over and not start:
                        point = pos_point(event.pos, x)
                        if point <= x*y and not mine_sweep.sweeped[point] and not mine_sweep.flag[point]:
                            sweep_times += 1
                            
                            # --------------- 翻格子时：点中雷，game over --------------------
                            if mine_sweep.list_cue[point] == 9:
                                if sweep_times != 1:
                                    boom_point = point
                                    game_over = True
                                    boom_sound.play()
                                else:
                                    while mine_sweep.list_cue[point] == 9:
                                        mine_sweep.reset(x, y, mine_num)
                                        mine_sweep.bury_mine()
                                        sweep_times = 0
                                    sweep_times = 1
                                    if mine_sweep.list_cue[point]: 
                                        screen.blit(bg2, pos_position(event.pos))
                                        screen.blit(show[mine_sweep.list_cue[point]], pos_position(event.pos))
                                        mine_sweep.sweeped[point] = 1
                                    else:
                                        screen.blit(bg2, pos_position(event.pos))
                                        mine_sweep.find_neighbor(point)
                                        for each in mine_sweep.neighbor:
                                            mine_sweep.sweeped[each[0]] = 1
                                            screen.blit(bg2, point_position(each[0], x))
                                            screen.blit(show[each[1]], point_position(each[0], x))
                                        mine_sweep.neighbor_reset()

                            # -------------- 翻格子时：点中数字，显示数字 --------------------
                            elif mine_sweep.list_cue[point]: 
                                screen.blit(bg2, pos_position(event.pos))
                                screen.blit(show[mine_sweep.list_cue[point]], pos_position(event.pos))
                                mine_sweep.sweeped[point] = 1
                            
                            # -------------- 翻格子时：点中空白，显示周围所有安全区域 --------
                            else:
                                screen.blit(bg2, pos_position(event.pos))
                                mine_sweep.find_neighbor(point)
                                for each in mine_sweep.neighbor:
                                    if not mine_sweep.flag[each[0]]:
                                        mine_sweep.sweeped[each[0]] = 1
                                        screen.blit(bg2, point_position(each[0], x))
                                        screen.blit(show[each[1]], point_position(each[0], x))
                                mine_sweep.neighbor_reset()

                    # ---------------------- start界面时，选择难易程度 --------------------
                    if start and not game_over:
                        if choose_mode_rect[0].collidepoint(event.pos):
                            x, y = easy_x, easy_y
                            mine_num = easy_mines
                            init = True
                        elif choose_mode_rect[1].collidepoint(event.pos):
                            x, y = normal_x, normal_y
                            mine_num = normal_mines
                            init = True

                        elif choose_mode_rect[2].collidepoint(event.pos):
                            x, y = hard_x, hard_y
                            mine_num = hard_mines
                            init = True
                         
                # --------------- 游戏时，右键插旗子（没有扫过的才能插）---------------------
                if pg.mouse.get_pressed() == (False, False, True) and not game_over and not start:
                    point = pos_point(event.pos, x)
                    if point <= x*y and not mine_sweep.sweeped[point]:
                        if not mine_sweep.flag[point]:
                            screen.blit(flag_image, pos_position(event.pos))
                            mine_sweep.flag[point] = 1
                            remaining_mine -= 1
                        else:
                            screen.blit(bg1, pos_position(event.pos))
                            mine_sweep.flag[point] = 0
                            remaining_mine += 1
                            
                            
                # ------------- 游戏时，中键打开周围所有格子，如果有雷就输了---------------
                if pg.mouse.get_pressed() == (False, True, False) and not game_over and not start:
                    point = pos_point(event.pos, x)
                    if point <= x*y and mine_sweep.sweeped[point]:
                        mine_sweep.find_neighbor_8(point)
                        if mine_sweep.neighbor_flag == mine_sweep.list_cue[point]:
                            for each in mine_sweep.neighbor:
                                if not mine_sweep.flag[each[0]]:
                                    mine_sweep.sweeped[each[0]] = 1
                                    screen.blit(bg2, point_position(each[0], x))
                                    screen.blit(show[each[1]], point_position(each[0], x))
                                    if each[1] == 9:
                                        boom_point = each[0]
                                        game_over = True
                                        boom_sound.play()
                        mine_sweep.neighbor_reset()
        
        if not start and not game_over:
            # --------------- 如果存在一个非雷点没点开（插旗不算），游戏就没有结束 --------------
            all_sweeped = True
            for i in range(x*y):
                if mine_sweep.list_cue[i] != 9 and mine_sweep.sweeped[i] == 0:
                    all_sweeped = False
            if all_sweeped:
                game_over = True
                win = True
                
            # --------------- 显示你认为剩余雷的个数以及时间 ---------------------------------
            screen.blit(bg0, (0,y0 - 24))
            mine_num_text = font2.render("Mines :  %s" % str(remaining_mine) ,True, (0, 0, 0))        
            screen.blit(mine_num_text, (x0/4 - 35, y0 - 22))
            time_used = int(time.time() - start_time)
            time_used_text = font2.render("Time :  %s s" % str(time_used) ,True, (0, 0, 0))
            screen.blit(time_used_text, (x0*3/4 - 35, y0 - 22))
            screen.blit(start_image, (start_image_rect.left, start_image_rect.top))
                        
        pg.display.flip()
        clock.tick(60)
        delay = (delay + 1) % 10


if __name__ == "__main__":
    main()

    
