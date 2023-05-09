import rpyc


class QuizClient:

    def __init__(self, name):
        self.name = name
        self.score = 0

    def start(self):
        conn = rpyc.connect("SERVER_IP_ADDRESS", 18862)
        quiz_service = conn.root.QuizService()

        print(f"Welcome {self.name} to the Quiz Game!")
        print("Select a category to start:")
        print("1. Sports")
        print("2. History")
        print("3. General Knowledge")

        category = input("Enter your choice: ")
        while category not in ['1', '2', '3']:
            print("Invalid choice. Please try again.")
            category = input("Enter your choice: ")

        category_map = {'1': 'sports', '2': 'history', '3': 'gk'}
        questions = quiz_service.get_questions(category_map[category])

        for q in questions:
            print(q)
            answer = input("Your answer: ")
            answer = answer.strip().lower()
            result = quiz_service.validate_answer(q, answer)
            if result:
                print("Correct!")
                self.score += 1
            else:
                print("Incorrect.")

        winner = quiz_service.get_winner(self.name, self.score)
        print(f"The winner is: {winner}")


if __name__ == "__main__":
    name = input("Enter your name: ")
    client = QuizClient(name)
    client.start()
