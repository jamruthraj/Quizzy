import rpyc

score = 0


class QuizClient:
    # initialize the client
    def __init__(self):
        self.conn = rpyc.connect("localhost", 12351)
        self.category = None

    # start the quiz and get the player name
    def start_quiz(self):
        name = input("Enter your name: ")
        player_id = self.conn.root.register()
        if player_id != -1:
            print(f"{name}, you are registered as player {player_id}")
            return (name, player_id)
        else:
            print("Sorry, the quiz is full.")
            return None

    # select the category
    def select_category(self):
        categories = self.conn.root.getcategories()
        print("Available categories:")
        for i, category in enumerate(categories):
            print(f"{i + 1}. {category}")
        choice = input("Enter the number of the category you want to select: ")
        try:
            choice = int(choice)
            if choice < 1 or choice > len(categories):
                raise ValueError
        except ValueError:
            print("Invalid choice.")
            return self.select_category()
        self.category = categories[choice - 1]
        return self.category

    # get the question and validate the answer
    def play_game(self, name, player_id):
        global score
        if not self.category:
            print("No category selected.")
            return

        print(f"{name}, the category is {self.category}")
        questions = self.conn.root.getquestions(self.category)
        for i, (q, a) in enumerate(questions.items()):
            print(f"\nQuestion {i+1}: {q}")
            answer = input("Answer: ")
            if self.conn.root.validateanswer(answer, name, q, self.category):
                print("Correct answer!")
                score += 1
            else:
                print("Wrong answer.")

    # print the winner
    def get_winner(self):
        global score
        print("Your Score: ", score)
        print(self.conn.root.getwinner(name, score))


if __name__ == '__main__':
    client = QuizClient()
    name, player_id = client.start_quiz()
    if name:
        client.select_category()
        client.play_game(name, player_id)
        client.get_winner()
