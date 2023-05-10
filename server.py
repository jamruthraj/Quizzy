import rpyc
import random


class QuizService(rpyc.Service):
    # initialize the service
    def __init__(self):
        self.scores = {}
        self.questions = {
            'sports': {
                'Which year did India win its first Hockey World Cup?': 1975,
                'First Indian Bowler to take Hatrick in an International Test Match?': 'harbhajansingh',
                'Oldest Tennis Tournament?': 'wimbledon',
                'Which sport does LeBron James play?': 'basketball',
                'Who captained the Indian Team that won the U19 World Cup in 2000?': 'muhammadkaif'
            },
            'history': {
                'Who wrote Vande Mataram': 'bankimchandrachatterjee',
                'In which city did the formation of Azad Hind Fauj happen?': 'singapore',
                'Who presided over the first Indian National Congress meeting': 'lalalajpatrai',
                'Who used the word \'Swarajya\' first?': 'balgangadhartilak',
                'Who wrote \'Akbarnama\'?': 'abulfazl'
            },
            'gk': {
                'Entomology is the study of?': 'insects',
                'Which element is used for galvanizing Iron': 'zinc',
                'UN Headquaters?': 'newyork',
                'Headquarters of Assam Rifles is present in which city?': 'shillong',
                'Who discovered Electron': 'jjthompson'
            }
        }
        self.current_question = None
        self.current_category = None
        self.answer = None

    # get the question for the given category
    def exposed_get_question(self, category):
        questions = self.questions[category]
        question = random.choice(list(questions.keys()))
        answer = questions[question]
        self.current_question = question
        self.current_category = category
        self.answer = answer
        return self.current_question

    # validate the answer and add the score
    def exposed_validate_answer(self, answer, name):
        if answer.lower().replace(" ", "") == str(self.answer).lower().replace(" ", ""):
            if name in self.scores:
                self.scores[name] += 1
            else:
                self.scores[name] = 1
            return True
        else:
            return False

    # get the winner
    def exposed_get_winner(self):
        if len(self.scores) == 0:
            return "No winner yet. All players have quit."
        max_score = max(self.scores.values())
        winners = [name for name, score in self.scores.items()
                   if score == max_score]
        if len(winners) == 1:
            return f"The winner is {winners[0]} with a score of {max_score}."
        else:
            return f"It's a tie between {', '.join(winners)} with a score of {max_score} each."


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(QuizService, port=12347,
                       protocol_config={"allow_public_attrs": True})
    t.start()
