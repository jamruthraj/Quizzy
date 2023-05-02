import rpyc


class QuizGame(rpyc.Service):
    sports = {
        'Which year did India win its first Hockey World Cup?': 1975,
        'First Indian Bowler to take Hatrick in an International Test Match?': 'harbhajansingh',
        'Oldest Tennis Tournament?': 'wimbledon',
        'Which sport does LeBron James play?': 'basketball',
        'Who captained the Indian Team that won the U19 World Cup in 2000?': 'muhammadkaif'
    }

    history = {
        'Who wrote Vande Mataram': 'bankimchandrachatterjee',
        'In which city did the formation of Azad Hind Fauj happen?': 'singapore',
        'Who presided over the first Indian National Congress meeting': 'lalalajpatrai',
        'Who used the word \'Swarajya\' first?': 'balgangadhartilak',
        'Who wrote \'Akbarnama\'?': 'abulfazl'
    }

    gk = {
        'Entomology is the study of?': 'insects',
        'Which element is used for galvanizing Iron': 'zinc',
        'UN Headquaters?': 'newyork',
        'Headquarters of Assam Rifles is present in which city?': 'shillong',
        'Who discovered Electron': 'jjthompson'
    }

    def exposed_get_question(self):

        return 0

    def exposed_check_answer(self, question, answer):
        print("Hi")
        return 0


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(QuizGame, port=18861)
    t.start()
