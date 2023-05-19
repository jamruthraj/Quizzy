import rpyc
import time

started = 0
finished = 0
top = -1
winners = []


class QuizService(rpyc.Service):
    # initialize the service
    def __init__(self):
        self.scores = {}
        self.questions = {
            'sports': {
                'Which year did India win its first Hockey World Cup?': '1975',
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
        self.current_category = None
        self.players = []
        self.client_ids = []

    # get the list of categories
    def exposed_getcategories(self):
        return list(self.questions.keys())

    # get the question for the given category
    def exposed_getquestions(self, category):
        currques = self.questions[category]
        self.current_category = category
        return currques

    # validate the answer and add the score
    def exposed_validateanswer(self, answer, name, q, category):
        ans = self.questions[category][q]
        if answer.lower().replace(" ", "") == ans:
            if name in self.scores:
                self.scores[name] += 1
            else:
                self.scores[name] = 1
            return True
        else:
            self.scores[name] = 0
            return False

    # register player and get player name
    def exposed_register(self):
        global started
        if started < 4:
            started += 1
            client_id = started
            self.client_ids.append(started)
            print(f"Client {client_id} connected.")
            return client_id
        else:
            return -1

    # get the winner
    def exposed_getwinner(self, name, score):
        global finished, top, winners
        if score > top:
            winners = []
            winners.append(name)
            top = score
        if score == top:
            winners.append(name)
        finished += 1
        while finished < 4:
            time.sleep(2)

        winners = set(winners)
        winners = list(winners)
        if len(winners) == 1:
            return f"The winner is {winners[0]} with a score of {top}."
        else:
            return f"It's a tie between {', '.join(winners)} with a score of {top} each."


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(QuizService, port=12351,
                       protocol_config={"allow_public_attrs": True})
    t.start()
