import tkinter as tk
from tkinter import messagebox
import random
import time

player_can_move = True
bot_can_move = True

def menu(root, var):
    label = tk.Label(root, text="Pilih Mode Permainan")
    label.pack()

    def on_select():
        if var.get() == 1:
            start_game(root, True)
        elif var.get() == 2:
            start_game(root, False)
        elif var.get() == 3:
            root.quit()

    rb1 = tk.Radiobutton(root, text="Brute Force", variable=var, value=1)
    rb1.pack(anchor=tk.W)
    rb2 = tk.Radiobutton(root, text="Greedy", variable=var, value=2)
    rb2.pack(anchor=tk.W)
    rb3 = tk.Radiobutton(root, text="Exit", variable=var, value=3)
    rb3.pack(anchor=tk.W)

    button = tk.Button(root, text="Pilih", command=on_select)
    button.pack()

def insert_first(LK, kartu):
    LK.insert(0, kartu)

def insert_last(LK, kartu):
    LK.append(kartu)

def delete_first(LK, kartu):
    LK.pop(0)

def delete_last(LK, kartu):
    LK.pop(-1)

def delete_after(LK, n):
    LK.pop(n)

def insert_kartu_pertama_meja(k_meja, kartu):
    insert_first(k_meja, kartu)

def insert_kartu_meja(k_meja, kartu, posisi):
    if posisi == "kiri":
        if k_meja[0][1:2] != kartu[5:6]:
            kartu = "[" + kartu[5] + " | " + kartu[1] + "]"
        k_meja.insert(0, kartu)
    elif posisi == "kanan":
        if k_meja[-1][5:6] != kartu[1:2]:
            kartu = "[" + kartu[5] + " | " + kartu[1] + "]"
        k_meja.append(kartu)

def insert_kartu_player(LK, shuffle):
    for i in range(0, 14, 2):
        kartu_str = shuffle[i]
        insert_first(LK, kartu_str)

def insert_kartu_bot_bf(LK, shuffle):
    for i in range(1, 14, 2):
        kartu_str = shuffle[i]
        insert_first(LK, kartu_str)

def insert_kartu_bot_g(LK, shuffle):
    arr_temp = [shuffle[i] for i in range(1, 14, 2)]
    sort_kartu_bot(arr_temp)
    for kartu_str in arr_temp:
        if kartu_str == "[0 | 0]":
            insert_first(LK, kartu_str)
        else:
            insert_last(LK, kartu_str)

def sort_kartu_bot(arrKartu):
    n = len(arrKartu)
    for i in range(n - 1):
        idx = i
        for j in range(i + 1, n):
            new_s = arrKartu[idx]
            s = arrKartu[j]
            if int(s[1:2]) + int(s[5:6]) > int(new_s[1:2]) + int(new_s[5:6]):
                idx = j
        if idx != i:
            arrKartu[idx], arrKartu[i] = arrKartu[i], arrKartu[idx]

def shuffle_kartu(kartu, shuffle):
    random.seed(time.time())
    i = 0
    while i < 15:
        temp = random.choice(kartu)
        while temp in shuffle[:i]:
            temp = random.choice(kartu)
        shuffle[i] = temp
        i += 1

def cek_duplikat(x, shuffle, banyak_kartu):
    duplikat = False
    i = 0
    while i < banyak_kartu and not duplikat:
        if x == shuffle[i]:
            duplikat = True
        i += 1
    return duplikat

def print_kartu_meja(k_meja, root):
    frame = tk.Frame(root)
    frame.pack()
    label = tk.Label(frame, text="Kartu di Meja:")
    label.pack(side=tk.LEFT)
    for kartu in k_meja:
        label = tk.Label(frame, text=kartu)
        label.pack(side=tk.LEFT)

def print_kartu_player(k_player, root):
    frame = tk.Frame(root)
    frame.pack()
    label = tk.Label(frame, text="Kartu di Tangan:")
    label.grid(row=0, column=0, columnspan=2)  # Center the header
    for i, kartu in enumerate(k_player, start=1):
        number_label = tk.Label(frame, text=f"{i}.")
        number_label.grid(row=i, column=0, sticky='w')  # Align number to the left
        card_label = tk.Label(frame, text=kartu)
        card_label.grid(row=i, column=1, sticky='w')  # Align card to the left


def print_kartu_bot(k_bot, root):
    frame = tk.Frame(root)
    frame.pack()
    label = tk.Label(frame, text="Kartu di Bot:")
    label.pack(side=tk.LEFT)
    for kartu in k_bot:
        label = tk.Label(frame, text=kartu)
        label.pack(side=tk.LEFT)

def gameplay(k_meja, k_player, k_bot, is_brute_force, root):
    def refresh_ui():
        for widget in root.winfo_children():
            widget.destroy()
        print_kartu_meja(k_meja, root)
        print_kartu_player(k_player, root)
        print_kartu_bot(k_bot, root)

    def bot_turn():
        cek1 = k_meja[0] if k_meja else None
        cek2 = k_meja[-1] if k_meja else None

        if is_brute_force:
            bot_move_brute_force(k_bot, k_meja)
        else:
            bot_move_greedy(k_bot, k_meja)

        cek3 = k_meja[0] if k_meja else None
        cek4 = k_meja[-1] if k_meja else None
        
        global player_can_move
        global bot_can_move
        if cek1 == cek3 and cek2 == cek4:
            messagebox.showinfo("Info", "Bot skip turn")
            bot_can_move = False
            if ((not k_bot) or (not bot_can_move and not player_can_move)):
                end_game(k_player, k_bot, k_meja, root)
            else:
                player_turn()
        else:
            bot_can_move = True
            player_can_move = True
            refresh_ui()
            player_turn()
            #if not k_bot:
            #    end_game(k_player, k_bot, k_meja, root)
            #else:
            #    player_turn()

    def player_turn():
        refresh_ui()

        def on_select():
            global player_can_move
            global bot_can_move
            pilihan = int(entry.get()) - 1
            if pilihan == -1:
                messagebox.showinfo("Info", "Player skip turn")
                player_can_move = False
                if ((not k_player) or (not bot_can_move and not player_can_move)):
                    end_game(k_player, k_bot, k_meja, root)
                else:
                    bot_turn()
            else:
                kartu = k_player[pilihan]
                if is_valid_move(kartu, k_meja):
                    
                    posisi = pos_var.get()
                    insert_kartu_meja(k_meja, kartu, posisi)
                    k_player.pop(pilihan)
                    
                    player_can_move = True
                    bot_can_move = True
                    
                    refresh_ui()
                    bot_turn()
                    #if not k_player:
                    #    end_game(k_player, k_bot, k_meja, root)
                    #else:
                    #    bot_turn()
                else:
                    messagebox.showinfo("Error", "Kartu tidak dapat diletakkan di meja. Pilih kartu lain.")

        label = tk.Label(root, text="Masukkan pilihan nomor kartu yang dikeluarkan (0 untuk skip):")
        label.pack()
        entry = tk.Entry(root)
        entry.pack()
        pos_var = tk.StringVar(value="kiri")
        rb1 = tk.Radiobutton(root, text="Kiri", variable=pos_var, value="kiri")
        rb1.pack(anchor=tk.W)
        rb2 = tk.Radiobutton(root, text="Kanan", variable=pos_var, value="kanan")
        rb2.pack(anchor=tk.W)
        button = tk.Button(root, text="Pilih", command=on_select)
        button.pack()
    
    
    refresh_ui()
    bot_turn()
    
def is_valid_move(kartu, k_meja):
    if not k_meja:
        return True

    kiri_kartu_meja = k_meja[0]
    if (kartu[1:2] == kiri_kartu_meja[1:2] or kartu[5:6] == kiri_kartu_meja[1:2]):
        return True

    kanan_kartu_meja = k_meja[-1]
    if (kartu[1:2] == kanan_kartu_meja[5:6] or kartu[5:6] == kanan_kartu_meja[5:6]):
        return True

    return False

def bot_move_brute_force(k_bot, k_meja):
    done = False
    for i, kartu in enumerate(k_bot):
        if is_valid_move(kartu, k_meja):
            print(f"\nBot telah mengeluarkan kartu: {kartu}")
            if (kartu[5:6] == k_meja[0][1:2] or kartu[1:2] == k_meja[0][1:2]):
                insert_kartu_meja(k_meja, kartu, "kiri")
            elif (kartu[5:6] == k_meja[-1][5:6] or kartu[1:2] == k_meja[-1][5:6]):
                insert_kartu_meja(k_meja, kartu, "kanan")
            k_bot.pop(i)
            done = True
            break

def bot_move_greedy(k_bot, k_meja):
    max_card = None
    max_card_index = -1
    
    for i, kartu in enumerate(k_bot):
        if is_valid_move(kartu, k_meja):
            card_sum = int(kartu[1:2]) + int(kartu[5:6])
            if max_card is None or card_sum > max_card:
                max_card = card_sum
                max_card_index = i

    if max_card_index != -1:
        kartu = k_bot[max_card_index]
        print(f"\nBot telah mengeluarkan kartu: {kartu}")
        if (kartu[5:6] == k_meja[0][1:2] or kartu[1:2] == k_meja[0][1:2]):
            insert_kartu_meja(k_meja, kartu, "kiri")
        elif (kartu[5:6] == k_meja[-1][5:6] or kartu[1:2] == k_meja[-1][5:6]):
            insert_kartu_meja(k_meja, kartu, "kanan")
        k_bot.pop(max_card_index)

def count_points(kartu_list):  #return int
    points = 0
    for kartu in kartu_list:
        if kartu == "[0 | 0]":
            points += 25
        else:
            kiri, kanan = int(kartu[1]), int(kartu[5])
            points += kiri + kanan
    return points

def end_game(k_player, k_bot, k_meja, root):
    bot_point = count_points(k_bot)
    player_point = count_points(k_player)
    
    print("point bot:\t", bot_point)
    print("point player:\t",  player_point)
    if player_point < bot_point:
        messagebox.showinfo("Game Over", "Player menang!")
        
    elif bot_point < player_point:
        messagebox.showinfo("Game Over", "Bot menang!")
    else:
        messagebox.showinfo("Game Over", "Permainan berakhir dengan seri!")
    root.quit()

def start_game(root, is_brute_force):
    kartu = [
        "[0 | 0]", "[0 | 1]", "[0 | 2]", "[0 | 3]", "[0 | 4]", "[0 | 5]", "[0 | 6]",
        "[1 | 1]", "[1 | 2]", "[1 | 3]", "[1 | 4]", "[1 | 5]", "[1 | 6]",
        "[2 | 2]", "[2 | 3]", "[2 | 4]", "[2 | 5]", "[2 | 6]",
        "[3 | 3]", "[3 | 4]", "[3 | 5]", "[3 | 6]",
        "[4 | 4]", "[4 | 5]", "[4 | 6]",
        "[5 | 5]", "[5 | 6]",
        "[6 | 6]"
    ]

    shuffle = [""] * 15
    shuffle_kartu(kartu, shuffle)

    k_meja = []
    k_player = []
    k_bot = []

    insert_kartu_pertama_meja(k_meja, shuffle[14])
    insert_kartu_player(k_player, shuffle)

    if is_brute_force:
        insert_kartu_bot_bf(k_bot, shuffle)
    else:
        insert_kartu_bot_g(k_bot, shuffle)

    gameplay(k_meja, k_player, k_bot, is_brute_force, root)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Domino Game")

    var = tk.IntVar()
    menu(root, var)

    root.mainloop()

