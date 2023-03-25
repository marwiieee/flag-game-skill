from mycroft import MycroftSkill, intent_file_handler
import random


class FlagGame(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.quiz_questions = [
            {'question': 'Which country is Toronto in?
             'answer': 'Canada',
             'options': ['Canada', 'United States', 'Australia', 'France']},
            {'question': 'Which country is Rome in?',
             'answer': 'Italy',
             'options': ['Italy', 'Mexico', 'Brazil', 'Spain']},
            {'question': 'Which country is Osaka in?',
             'answer': 'Japan',
             'options': ['Japan', 'China', 'South Korea', 'Thailand']},
        ]
        self.score = 0
        self.question_index = 0

    @intent_file_handler('game.flag.intent')
    def handle_game_flag(self, message):
        self.speak_dialog('game.flag')
        self.ask_question()

    @intent_handler('game.flag.answer.intent')
    def handle_game_flag_answer(self, message):
        user_answer = message.data.get('Answer')
        correct_answer = self.quiz_questions[self.question_index]['answer']
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            self.speak_dialog('game.flag.answer.correct')
        else:
            self.speak_dialog('game.flag.answer.incorrect', data={'answer': correct_answer})
        self.question_index += 1
        if self.question_index < len(self.quiz_questions):
            self.ask_question()
        else:
            self.speak_dialog('game.flag.end', data={'score': self.score})

    def ask_question(self):
        question = self.quiz_questions[self.question_index]['question']
        image = self.quiz_questions[self.question_index]['image']
        options = self.quiz_questions[self.question_index]['options']
        random.shuffle(options)
        self.enclosure.display_image(image)
        self.speak(question)
        self.speak("Your options are:")
        for option in options:
            self.speak(option)
        self.ask(f"What is your answer? Choose from {', '.join(options)}")

def create_skill():
    return FlagGame()
