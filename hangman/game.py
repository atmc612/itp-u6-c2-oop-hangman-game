from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess, hit = False, miss = False):
        if hit and miss:
            raise InvalidGuessAttempt("Can't be both a hit and a miss")
        self.guess = guess
        self.hit = hit
        self.miss = miss
    
    def is_hit(self):
        return self.hit
    
    def is_miss(self):
        return self.miss

class GuessWord(object):
    def __init__(self, answer_word):
        if not answer_word:
            raise InvalidWordException('Attempt can only be one letter')
        self.answer = answer_word
        self.masked = '*' * len(answer_word)
        
    def perform_attempt(self, attempt_letter):
        if len(attempt_letter) > 1:
            raise InvalidGuessedLetterException
        
        if attempt_letter.lower() not in self.answer.lower():
            return GuessAttempt(attempt_letter, miss = True)
        
        #iterate and uncover word
        else:
            hit_list_index = []
            for index, char in enumerate(list(self.answer.lower())):
                if char.lower() == attempt_letter.lower():
                    hit_list_index.append(index)
            
            result = list(self.masked)
            for index in hit_list_index:
                result[index] = attempt_letter.lower()
            result = "".join(result)
            self.masked = result
        
        return GuessAttempt(attempt_letter, hit = True)
        

class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list = WORD_LIST, number_of_guesses = 5):
        self.word_list = word_list
        self.previous_guesses = []
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(self.select_random_word(word_list))
    
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException("Can not select random word from empty list")
        return random.choice(word_list)
    
    ## define game states 
    
    def is_finished(self):
        if self.word.masked == self.word.answer or self.remaining_misses == 0:
            return True
        return False

    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        return False

    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
    
    ## perform guess
    def guess(self,attempt_letter):
        
        if self.is_finished():
            raise GameFinishedException("Game is already over!")
        self.previous_guesses.append(attempt_letter.lower())        
        attempt = self.word.perform_attempt(attempt_letter)

        if attempt.is_miss() == True:
            self.remaining_misses -= 1

        if self.is_won():
            raise GameWonException("Game Won!") 
        if self.is_lost():
            raise GameLostException("Game Lost!")  
        return attempt
    
    
    
