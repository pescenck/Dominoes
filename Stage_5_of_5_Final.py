import random


class Domino:

    def __init__(self):
        self.full_domino_set = []
        self.stock_pieces = []
        self.computer_pieces = []
        self.player_pieces = []
        self.domino_snake = []
        self.status = None
        self.player_input = None

    def generate_full_domino_set(self):
        self.full_domino_set = [[x, y] for x in range(7) for y in range(x + 1)]

    def shuffle_domino_set(self):
        random.shuffle(self.full_domino_set)

    def allocate_domino_pieces(self):
        self.player_pieces = self.full_domino_set[:7]
        self.computer_pieces = self.full_domino_set[7:14]
        self.stock_pieces = self.full_domino_set[14:]

    def determine_starting_player(self):
        player_pieces_max = max(self.player_pieces)
        computer_pieces_max = max(self.computer_pieces)

        if computer_pieces_max > player_pieces_max:
            self.status = 'player'

            max_index = self.computer_pieces.index(computer_pieces_max)
            self.domino_snake.append(self.computer_pieces[max_index])
            self.computer_pieces.remove(self.computer_pieces[max_index])
        else:
            self.status = 'computer'

            max_index = self.player_pieces.index(player_pieces_max)
            self.domino_snake.append(self.player_pieces[max_index])
            self.player_pieces.remove(self.player_pieces[max_index])

    def check_player_input(self):
        while True:
            count = self.player_input.count('-')
            if count > 1:
                print("Invalid input. Please try again.")
                self.player_input = input()
            elif self.player_input.lstrip('-').isdigit():
                if abs(int(self.player_input)) > len(self.player_pieces):
                    print("Invalid input. Please try again.")
                    self.player_input = input()
                else:
                    break
            else:
                print("Invalid input. Please try again.")
                self.player_input = input()

    def player_move(self):
        while True:
            self.player_input = input()
            self.check_player_input()
            player_input = int(self.player_input)

            if player_input > 0:
                player_input -= 1

                if self.player_pieces[player_input][0] == self.domino_snake[-1][1]:
                    self.domino_snake.append(self.player_pieces[player_input])
                    self.player_pieces.remove(self.player_pieces[player_input])
                    break
                elif self.player_pieces[player_input][1] == self.domino_snake[-1][1]:
                    flip_piece = self.player_pieces[player_input]
                    flip_piece.reverse()
                    self.domino_snake.append(flip_piece)
                    self.player_pieces.remove(self.player_pieces[player_input])
                    break
                else:
                    print("Illegal move. Please try again.")

            elif player_input < 0:
                player_input = abs(player_input) - 1

                if self.player_pieces[player_input][1] == self.domino_snake[0][0]:
                    self.domino_snake.insert(0, self.player_pieces[player_input])
                    self.player_pieces.remove(self.player_pieces[player_input])
                    break
                elif self.player_pieces[player_input][0] == self.domino_snake[0][0]:
                    flip_piece = self.player_pieces[player_input]
                    flip_piece.reverse()
                    self.domino_snake.insert(0, flip_piece)
                    self.player_pieces.remove(self.player_pieces[player_input])
                    break
                else:
                    print("Illegal move. Please try again.")
            else:
                if len(self.stock_pieces) != 0:
                    new_player_piece = self.stock_pieces.pop()
                    self.player_pieces.append(new_player_piece)
                    break
                else:
                    break

    def computer_ai_algorithm(self):
        computer_ai_list = self.computer_pieces + self.domino_snake

        count_dictionary = {}

        index = 0
        while index != 7:
            count = 0
            for domino in computer_ai_list:
                for number in domino:
                    if number == index:
                        count += 1
            count_dictionary[index] = count
            index += 1

        score_list = []
        for domino in self.computer_pieces:
            x = count_dictionary[domino[0]]
            y = count_dictionary[domino[1]]
            score_list.append(x + y)

        return score_list

    def computer_move(self):
        score_list = self.computer_ai_algorithm()
        while True:
            if len(score_list) != 0:
                highest_score = max(score_list)
                highest_score_index = score_list.index(highest_score)
                computer_input = self.computer_pieces[highest_score_index]
                computer_input_index = self.computer_pieces.index(computer_input)

                if computer_input[0] == self.domino_snake[-1][1]:
                    self.domino_snake.append(computer_input)
                    self.computer_pieces.remove(self.computer_pieces[computer_input_index])
                    break
                elif computer_input[1] == self.domino_snake[-1][1]:
                    flip_piece = computer_input
                    flip_piece.reverse()
                    self.domino_snake.append(flip_piece)
                    self.computer_pieces.remove(self.computer_pieces[computer_input_index])
                    break

                elif computer_input[1] == self.domino_snake[0][0]:
                    self.domino_snake.insert(0, computer_input)
                    self.computer_pieces.remove(self.computer_pieces[computer_input_index])
                    break
                elif computer_input[0] == self.domino_snake[0][0]:
                    flip_piece = computer_input
                    flip_piece.reverse()
                    self.domino_snake.insert(0, flip_piece)
                    self.computer_pieces.remove(self.computer_pieces[computer_input_index])
                    break
                else:
                    score_list.remove(score_list[highest_score_index])
                    continue

            else:
                if len(self.stock_pieces) != 0:
                    new_computer_piece = self.stock_pieces.pop()
                    self.computer_pieces.append(new_computer_piece)
                    break
                else:
                    break

    def check_for_win_condition(self):
        if len(self.player_pieces) == 0:
            self.status = 'player_wins'
            return True
        elif len(self.computer_pieces) == 0:
            self.status = 'computer_wins'
            return True
        elif self.domino_snake[0][0] == self.domino_snake[-1][1]:
            count_number = self.domino_snake[0][0]

            counter = 0
            for _ in self.domino_snake:
                for number in _:
                    if number == count_number:
                        counter += 1
            if counter >= 8:
                self.status = 'game_over_draw'
                return True
            else:
                return False
        else:
            return False

    def display_game_status(self):
        if self.status == 'player':
            print("\n""Status: It's your turn to make a move. Enter your command.")
        elif self.status == 'computer':
            print("\n""Status: Computer is about to make a move. Press Enter to continue...")
        elif self.status == 'player_wins':
            print("\n""Status: The game is over. You won!")
        elif self.status == 'computer_wins':
            print("\n""Status: The game is over. The computer won!")
        elif self.status == 'game_over_draw':
            print("\n""Status: The game is over. It's a draw!")

    def print_domino_snake(self):
        if len(self.domino_snake) > 6:

            snake_first_half_string_list = []
            for _ in self.domino_snake[0:3]:
                snake_first_half_string_list.append(str(_))

            snake_second_half_string_list = []
            for _ in self.domino_snake[(len(self.domino_snake) - 3):]:
                snake_second_half_string_list.append(str(_))

            print(''.join(snake_first_half_string_list) + '...' + ''.join(snake_second_half_string_list))
            print()

        else:
            domino_snake_string_list = []
            for _ in self.domino_snake:
                domino_snake_string_list.append(str(_))

            print(''.join(domino_snake_string_list))
            print()

    def game_interface(self):
        print("=" * 70)
        print(f"Stock size:", len(self.stock_pieces))
        print(f"Computer pieces:", len(self.computer_pieces))
        print()

        self.print_domino_snake()

        print("Your pieces:")
        for i, domino in enumerate(self.player_pieces, 1):
            print(i, domino, sep=':')

        self.display_game_status()

    def main(self):
        self.generate_full_domino_set()
        self.shuffle_domino_set()
        self.allocate_domino_pieces()
        self.determine_starting_player()

        while not self.check_for_win_condition():
            self.game_interface()
            if self.status == 'player':
                self.player_move()
                self.status = 'computer'
            else:
                self.player_input = input()
                self.computer_move()
                self.status = 'player'

        self.game_interface()


Domino().main()
