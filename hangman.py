import curses
import random 
import string

DASH = "-"
alphabets = "abcdefghijklmnopqrstuvwxyz"

positions = {"HEAD_Y" : 4, "HEAD_X" : 36, "NECK_Y" : 5, "NECK_X" : 36, "BODY_Y" : 6, "BODY_X" : 36, "RIG_HAND_Y" : 5, "RIG_HAND_X" : 35, "LEFT_HAND_Y" : 5, "LEFT_HAND_X" : 37, "RIG_LEG_Y" : 7, "RIG_LEG_X" : 35, "LEFT_LEG_Y" : 7, "LEFT_LEG_X" : 37}

while True:
    used = []
    def choose_word():
        lines = [word.strip() for word in open("words.txt")]
        return random.choice(lines)

    def updating_dashes(chosen_letter, dashes, letter_list):
        chosen_letter_count = 0
        for index, character in enumerate(letter_list):
            if chosen_letter == character:
                chosen_letter_count  += 1
                dashes[index] = character
        return(chosen_letter_count, ''.join(dashes))

    stdscr = curses.initscr()

    def draw_hangman(chances_left):
        if chances_left == 6:
            stdscr.addstr(positions["HEAD_Y"], positions["HEAD_X"], "O",curses.A_BOLD)
        elif chances_left == 5:
            stdscr.addstr(positions["NECK_Y"], positions["NECK_X"], "|",curses.A_BOLD)
        elif chances_left == 4:
            stdscr.addstr(positions["RIG_HAND_Y"], positions["RIG_HAND_X"], "/",curses.A_BOLD)
        elif chances_left == 3:
            stdscr.addstr(positions["LEFT_HAND_Y"], positions["LEFT_HAND_X"], "\\",curses.A_BOLD)
        elif chances_left == 2:
            stdscr.addstr(positions["BODY_Y"], positions["BODY_X"], "|",curses.A_BOLD)
        elif chances_left == 1:
            stdscr.addstr(positions["RIG_LEG_Y"], positions["RIG_LEG_X"], "/",curses.A_BOLD)
        else:
            stdscr.addstr(positions["LEFT_LEG_Y"], positions["LEFT_LEG_X"], "\\",curses.A_BOLD)

    def guess_letter(input_position):
        stdscr.addstr(18, 16, "letters typed : ")
        while True:
            key_entered = stdscr.getstr(18, input_position, 1).decode('utf-8').lower()
            #stdscr.addstr(22, 20, "=>>> " + key_entered + " <<<==")
            input_position += 1
            if key_entered not in alphabets:
                stdscr.addstr(20, 16, "Select an Alphabet.                       ")
            elif key_entered in used:
                stdscr.addstr(20, 16, "Letter already used, Please try again!")
            else:
                used.append(key_entered)
                return key_entered

    def game(dashes, letter_list):
        letters_found = 0
        chances_left = 7
        input_position = 32
        game_over =  False

        while not game_over:
            key_entered = guess_letter(input_position)
            input_position += 1

            chosen_letter_count, updated_dashes = updating_dashes(key_entered, dashes, letter_list)
            letters_found  += chosen_letter_count

            if letters_found == len(letter_list):
                stdscr.addstr(22, 16, "'CONGRATULATIONS!,You won the game'     ")
                game_over = True

            if chosen_letter_count != 0:
                stdscr.addstr(16, 23, updated_dashes)
                stdscr.addstr(20, 16, "Correct guess                                ")
            else:
                chances_left -= 1
                stdscr.addstr(20, 16, "letter not in the word, try again          ")
                draw_hangman(chances_left)

                if chances_left == 0:
                    stdscr.addstr(20, 16, "your chances are over,You lost           ")
                    stdscr.addstr(21, 16, "Word : " + ''.join(letter_list))
                    game_over = True

    def display(dashes):
        for x in range(20, 36):
            stdscr.addstr(2, x, '\u2501')
        for x in range(3, 12):
            stdscr.addstr(x, 19, '\u2503')

        for x in range(15, 33):
            stdscr.addstr(11, x, '\u2501')
        for x in range(33,40):
            stdscr.addstr(12,x,'\u2501')
        for x in range(15, 40):
            stdscr.addstr(14, x, '\u2501')

        
        for x in range(12,14):
            stdscr.addstr(x,15, '\u2503')
        
        stdscr.addstr(2,19,'\u250F')
        stdscr.addstr(2,36,'\u2513')
        stdscr.addstr(3,36,'\u2503')
        stdscr.addstr(11,19,'\u253B')
        stdscr.addstr(11,32,'\u2513')
        stdscr.addstr(11,15,'\u250F')
        stdscr.addstr(14,15,'\u2517')
        stdscr.addstr(12,32,'\u2517')
        stdscr.addstr(12,40,'\u2513')
        stdscr.addstr(14, 40, '\u251B')
        stdscr.addstr(13, 40, '\u2503')
        stdscr.addstr(11, 19, '\u253B')
    
        stdscr.addstr(16, 16, "Word : ")    
        stdscr.addstr(16, 23, ''.join(dashes))

    letter_list = list(choose_word())
    dashes = list(DASH * len(letter_list))
    display(dashes)
    game(dashes, letter_list)

    stdscr.addstr(23, 16, "Do you want to play again?? (y / n)")
    play_again_choice = stdscr.getstr(23, 55, 1).decode('utf-8').lower()
    curses.curs_set(0)

    while play_again_choice != 'n' and play_again_choice != 'y':
        stdscr.addstr(23, 16, "Enter either y or n                  ")
        play_again_choice = stdscr.getstr(23, 55, 1).decode('utf-8').lower()

    if play_again_choice == 'n':
        stdscr.clear()
        curses.endwin()
        break

    stdscr.clear()

    curses.endwin()





