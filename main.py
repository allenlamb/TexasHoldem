import pygame
import random

pygame.init()
# Width and Height of the Window
DIMENSIONS = [900, 740]


class Card(pygame.sprite.Sprite):
    """
    Represents a typical card
    Contains graphic image to draw card
    Contains rank and suit of card
    """

    def __init__(self, filename: str):
        """
        Constructor method
        :param filename: consists of a number ranking and a letter corresponding to a suit
        :type filename: str
        """
        super(Card, self).__init__()
        self.surf = pygame.image.load(filename)  # Uses the files from GUI folder
        self.rect = self.surf.get_rect()
        self._rank = filename[0]
        # Using te name from the GUI Folder we can initialize the suit and rank of each card
        if filename[1].isdigit():
            # 1-13 Ace to King
            self._rank += filename[1]
            self._suit = filename[2]
        else:

            self._suit = filename[1]

    def getRank(self) -> str:
        """
        returns the rank of a card
        :return: the rank of the card (1-13)
        :rtype: str
        """
        return self._rank

    def getSuit(self) -> str:
        """
        returns the suit of a card
        :return: str with the suit of the card ('c', 'd', 's', 'h')
        :rtype: str
        """
        return self._suit

    # Draws the card
    def displayCard(self, pos: list[int], screen):
        """
        Draws the card onto the screen
        :param pos: position where to draw card
        :type pos: list[int]
        :param screen: where the card will be drawn on to
        """
        screen.blit(self.surf, pos)


class Deck:
    """
    Standard deck of 52 cards in random order
    """

    def __init__(self):
        """
        Constructor method
        """
        self._deck = []  # Deck is basically a list of 52 cards
        # the suits
        second = ['c', 'd', 'h', 's']
        # Using a nested loop to find all the GUI files
        for i in range(1, 14, 1):
            for j in range(4):
                fileCard = str(i) + second[j] + '.gif'
                card = Card(fileCard)
                self._deck.append(card)
        # Shuffle Deck
        random.shuffle(self._deck)

    def draw(self) -> Card:
        """
        Draws a card as if you drew from a deck
        :return: acts as if you drew a card from a deck
        :rtype: Card
        """
        return self._deck.pop()


class CardGroup:
    """A subclass representing a list of cards such as a hand or the river"""

    def __init__(self, deck: Deck):
        """
        Constructor method
        :param deck: deck of cards
        :type deck: Deck
        """
        self._cardGroup = []
        self._cardGroup.append(deck.draw())
        self._cardGroup.append(deck.draw())
        self._yCord = None
        self._starting = DIMENSIONS[0] / 2 - len(self._cardGroup) * 100 / 2

    def display(self, screen):
        """
        Displays the cards on screen in a linear fashion
        :param screen: Screen in which to draw CardGroup on
        :return: For now it is passed as each inherited class will have a different way to display their cards
        """
        pass


class River(CardGroup):
    """
    River or the community pile in Texas Hold' em
    Starts off with 3 cards in the center and eventually goes to 5
    """

    def __init__(self, deck: Deck):
        """
        Constructor method
        :param deck: Deck of cards
        :type deck: Deck
        """
        super().__init__(deck)
        self._cardGroup.append(deck.draw())
        self._yCord = 250

    def display(self, screen):
        """
        Displays river to the center of screen
        :param screen: where river will be drawn
        """
        self._starting = DIMENSIONS[0] / 2 - len(self._cardGroup) * 100 / 2
        for i in range(len(self._cardGroup)):
            self._cardGroup[i].displayCard([self._starting + 100 * i, self._yCord], screen)

    def newTurn(self, deck: Deck, screen):
        """
        Adds a card to the river from the deck and displays it
        :param deck: Deck of cards
        :type deck: Deck
        :param screen: Where the river will be drawn
        """
        if len(self._cardGroup) < 5:
            self._cardGroup.append(deck.draw())
        self.display(screen)

    def length(self):
        """
        :return: How many cards are in the river
        """
        return len(self._cardGroup)


class Player(CardGroup):
    """
    2 cards that the player will use for their game
    """

    def __init__(self, deck: Deck):
        """
        Constructor method
        :param deck: Deck of cards
        :type deck: Deck
        """
        super().__init__(deck)
        self._yCord = 450

    def display(self, screen):
        """
        Displays player hand to the bottom of screen
        :param screen: Where playHand will be drawn to
        """
        for i in range(2):
            self._cardGroup[i].displayCard([self._starting + 100 * i, self._yCord], screen)

    def addRiver(self, river: River):
        """
        This is used in the scoring function where your hand and the rivers are combined in order to score your hand
        :param river: The river should be 5 cards
        :type river: River
        :return: a 2-d list with 7 elements [rank,suit]
        :rtype: list[list]
        """
        hand = []
        self._cardGroup += river._cardGroup
        for i in range(len(self._cardGroup)):
            hand.append([self._cardGroup[i].getRank(), self._cardGroup[i].getSuit()])
        return hand


class Bot(CardGroup):
    """
    A list of two cards, although there is a third element that stores the backfacing cards
    used for display, something exclusive to the Bot hand
    """

    def __init__(self, deck: Deck):
        """
        Constructor method
        :param deck: deck of cards
        :type deck: Deck
        """
        super().__init__(deck)
        self._cardGroup.append(Card('b.gif'))
        self._yCord = 100

    # Displays the back of a card
    def display(self, screen):
        """
        displays 2 cardbacks and hides the front
        :param screen: where the Bot Cards will be drawn to
        """
        for i in range(2):
            self._cardGroup[2].displayCard([self._starting + 100 * i, self._yCord], screen)

    # End of game will need to display the card fronts
    def display1(self, screen):
        """
        now displays the front of the 2 cards when the game is over
        :param screen: where the bot cards will be drawn to
        :return:
        """
        for i in range(2):
            self._cardGroup[i].displayCard([self._starting + 100 * i, self._yCord], screen)

    def addRiver(self, river: River):
        """
        This is used in the scoring function where your hand and the rivers are combined in order to score your hand
        :param river: The river should be 5 cards
        :type river: River
        :return: a 2-d list with 7 elements [rank,suit]
        :rtype: list[list]
        """
        hand = []
        self._cardGroup += river._cardGroup
        for i in range(len(self._cardGroup)):
            if self._cardGroup[i].getRank() != 'b':
                hand.append([self._cardGroup[i].getRank(), self._cardGroup[i].getSuit()])
        return hand


def royalFlush(hand, handSuit, handRank, suitList):
    """
    Checks to see if a hand is a Royal Flush
    A, K, Q, J, 10 all of the same suit
    :param hand: List of  7 cards
    :type hand: list[Cards]
    :param handSuit: list showing the frequency of each suit
    :type handSuit: list
    :param handRank: list showing the frequency of each rank
    :type handRank: list
    :param suitList: list of the suits in standard order by our program [c, d, h, s] makes code lot more convenient
    :type suitList: list
    :returns: Either True or false
    :rtype: list[bool]
    """
    royalRankList = [1, 10, 11, 12, 13]
    testSuit = ''
    testRank = 0
    for i in range(len(handSuit)):
        if handSuit[i] >= 5:
            testSuit = suitList[i]
            break
    if testSuit == '':
        return [False]
    for i in range(5):
        if handRank[royalRankList[i]] == 1:
            testRank = royalRankList[i]
            break
    if testRank == 0:
        return [False]
    for i in range(5):
        if [royalRankList[i], testSuit] not in hand:
            return [False]
    return True


def straightFlush(hand, handSuit, handRank, suitList):
    """
    Checks to see if a hand is a straightFlush
    5 cards in a sequence, all of the same suit
    :param hand: List of  7 cards
    :type hand: list[Cards]
    :param handSuit: list showing the frequency of each suit
    :type handSuit: list
    :param handRank: list showing the frequency of each rank
    :type handRank: list
    :param suitList: list of the suits in standard order by our program [c, d, h, s] makes code lot more convenient
    :type suitList: list
    :returns: Either False or True and the highest ranked card
    :rtype: list
    """
    testSuit = ''
    for i in range(len(handSuit)):
        if handSuit[i] >= 5:
            testSuit = suitList[i]
            break
    if testSuit == '':
        return [False]
    streak = 0
    maxRank = 0
    for j in range(1, 14, 1):
        if handRank[j] >= 1:
            streak += 1
        else:
            streak = 0
        if streak >= 5 and j == 13 and handRank[13] >= 1:
            maxRank = 13
        elif streak >= 5 and handRank[j + 1] == 0:
            maxRank = j
    if maxRank == 0:
        return [False]
    for i in range(5):
        if [maxRank - i, testSuit] not in hand:
            return [False]
    return [True, maxRank]


def fourOfAKind(handRank):
    """
    Checks to see if a hand is a Four of a Kind
    All 4 cards of the same rank
    :param handRank: list showing the frequency of each rank
    :type handRank: list
    :returns: Either False or True and the highest ranked card
    :rtype: list
    """
    for i in range(len(handRank)):
        if handRank[i] == 4:
            maxRank = i
            return [True, maxRank]
    return [False]


def fullHouse(handRank):
    """
    Checks to see if a hand is a Full House
    Three of a kind with a pair
    :param handRank: list showing the frequency of each rank
    :type handRank: list
    :returns: Either False or True, the rank of the triple and the rank of the pair
    :rtype: list
    """
    maxTriple = 0
    maxPair = 0
    for i in range(len(handRank)):
        if handRank[i] == 3:
            if i > maxTriple:
                maxTriple = i
        if handRank[i] == 2:
            if i > maxPair:
                maxPair = i

    if maxTriple == 0 or maxPair == 0:
        return [False]
    else:
        return [True, maxTriple, maxPair]


def flush(hand, handSuit, suitList):
    """
    Checks to see if a hand is a Flush
    5 cards of the same suit, but not in a sequence
    :param hand: List of  7 cards
    :type hand: list[Cards]
    :param handSuit: list showing the frequency of each suit
    :type handSuit: list
    :param suitList: list of the suits in standard order by our program [c, d, h, s] makes code lot more convenient
    :type suitList: list
    :returns: Either False or True and the highest ranked card
    :rtype: list
    """
    testSuit = ''
    maxRank = 0
    for i in range(len(handSuit)):
        if handSuit[i] >= 5:
            testSuit = suitList[i]
            break
    if testSuit == '':
        return [False]
    if [1, testSuit] in hand:
        maxRank = 1
    if maxRank != 1:
        for i in range(13):
            if [13 - i, testSuit] in hand:
                maxRank = 13 - i
                break
    return [True, maxRank]


def straight(handRank):
    """
    Checks to see if a hand is a straight
    5 cards in a sequence, but not of the same suit
    :param handRank: list showing the frequency of each rank
    :type handRank: list
    :returns: Either False or True and the highest ranked card
    :rtype: list
    """
    streak = 0
    maxRank = 0
    for j in range(1, 14, 1):
        if handRank[j] >= 1:
            streak += 1
        else:
            streak = 0
        if streak >= 4 and j == 13 and handRank[1] >= 1:
            maxRank = 1
            break
        if streak >= 5 and j == 13 and handRank[13] >= 1:
            maxRank = 13
        elif streak >= 5 and handRank[j + 1] == 0:
            maxRank = j
    if maxRank == 0:
        return [False]
    return [True, maxRank]


def threeOfAKind(handRank):
    """
    Checks to see if a hand is Three of a Kind
    3 cards of the same rank
    :param handRank: list showing the frequency of each rank
    :type handRank: list
    :returns: Either False or True and the rank of the triple
    :rtype: list
    """

    maxTriple = 0
    for i in range(len(handRank)):
        if handRank[i] == 3:
            if i > maxTriple:
                maxTriple = i
    if maxTriple == 0:
        return [False]
    return [True, maxTriple]


def twoPair(handRank):
    """
    Checks to see if a hand is a Two Pair
    2 different pairs
    :param handRank: list showing the frequency of each rank
    :type handRank: list
    :returns: Either False or True and the rank of both pairs
    :rtype: list
    """
    pair = []
    for i in range(len(handRank)):
        if handRank[i] == 2:
            pair.append(i)
    pair.sort()
    if len(pair) < 2:
        return [False]
    return [True, pair[-1], pair[-2]]


def onePair(handRank):
    """
    Checks to see if contains a Pair
    2 cards of the same rank
    :param handRank: list showing the frequency of each rank
    :type handRank: list
    :returns: Either False or True and the rank of the pair
    :rtype: list
    """
    pair = 0
    for i in range(len(handRank)):
        if handRank[i] == 2:
            pair = i
    if pair == 0:
        return [False]
    return [True, pair]


def highCard(handRank):
    """
    When you haven't made any of the hands above, you play the highest card in your hand
    :param handRank: list showing the frequency of each rank
    :type handRank: list
    :returns: Either The highest ranking cardin your hand
    :rtype: int
    """
    for i in range(len(handRank)):
        if handRank[13 - i] >= 1:
            return 13 - i


def score(hand):
    """
    Scores the hand by checking one by one every possible score
    :param hand: 2-d list containing suit and rank
    :type hand: list
    :return: returns which hand you got, as well as the highest ranking card(s) of that hand to settle tie breakers
    :rtype: list
    """
    suitList = ['c', 'd', 'h', 's']
    ranks = [0] * 14
    suits = [0] * 4
    for i in range(7):
        hand[i][0] = int(hand[i][0])
        ranks[hand[i][0]] += 1
        suits[suitList.index(hand[i][1])] += 1
    txtAndTie = []
    if royalFlush(hand, suits, ranks, suitList)[0]:
        txtAndTie.append("Royal Flush")
        txtAndTie.append(0)
    elif straightFlush(hand, suits, ranks, suitList)[0]:
        txtAndTie.append("Straight Flush")
        txtAndTie.append(1)
        txtAndTie.append(straightFlush(hand, suits, ranks, suitList)[1])
    elif fourOfAKind(ranks)[0]:
        txtAndTie.append("Four of a Kind")
        txtAndTie.append(2)
        txtAndTie.append(fourOfAKind(ranks)[1])
    elif fullHouse(ranks)[0]:
        txtAndTie.append("Full House")
        txtAndTie.append(3)
        txtAndTie.append(fullHouse(ranks)[1])
        txtAndTie.append(fullHouse(ranks)[2])
    elif flush(hand, suits, suitList)[0]:
        txtAndTie.append("Flush")
        txtAndTie.append(4)
        txtAndTie.append(flush(hand, suits, suitList)[1])
    elif straight(ranks)[0]:
        txtAndTie.append("Straight")
        txtAndTie.append(5)
        txtAndTie.append(straight(ranks)[1])
    elif threeOfAKind(ranks)[0]:
        txtAndTie.append("Three of a Kind")
        txtAndTie.append(6)
        txtAndTie.append(threeOfAKind(ranks)[1])
    elif twoPair(ranks)[0]:
        txtAndTie.append("Two Pair")
        txtAndTie.append(7)
        txtAndTie.append(twoPair(ranks)[1])
        txtAndTie.append(twoPair(ranks)[2])
    elif onePair(ranks)[0]:
        txtAndTie.append("One Pair")
        txtAndTie.append(8)
        txtAndTie.append(onePair(ranks)[1])
    else:
        txtAndTie.append("High Card")
        txtAndTie.append(9)
        txtAndTie.append(highCard(ranks))
    return txtAndTie


def endText(bScore, pScore):
    """
    Returns the text for the score including
    what score the bot got
    what score the player got
    who won/tied
    :param bScore: the score of the bot
    :type bScore: list
    :param pScore: the score of the player
    :type pScore: list
    :return: victory, lose or tie text for the game to display
    """
    if pScore[1] == bScore[1]:
        if pScore[2] > bScore[2] or (pScore[2] == 1 and bScore[2] != 1):
            return "YOU WIN"
        if pScore[2] < bScore[2] or (bScore[2] == 1 and pScore[2] != 1):
            return "YOU LOSE"
        if pScore[2] == bScore[2]:
            if pScore[1] == 3 or pScore[1] == 7:
                if pScore[3] == bScore[3]:
                    return "IT IS A TIE"
                if pScore[3] > bScore[3] or (pScore[3] == 1 and bScore[3] != 1):
                    return "YOU WIN"
                if pScore[3] < bScore[3] or (bScore[3] == 1 and pScore[3] != 1):
                    return "YOU LOST"
            return "IT IS A TIE"
    elif pScore[1] < bScore[1]:
        return "YOU WIN"
    elif pScore[1] > bScore[1]:
        return "YOU LOSE"

    # SAMPLE CONDITION FOR A ROYAL FLUSH
    # RoyalFlush = [[2, 'd'], [4, 'c'], [10, 's'], [11, 's'], [12, 's'], [13, 's'], [1, 's']]
    # royalSuit = [1, 1, 0, 5]
    # royalRanks = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    # print(royalFlush(RoyalFlush, royalSuit, royalRanks, suitList))

    # SAMPLE CONDITION FOR STRAIGHT FLUSH
    # StraightFLush = [[1, 's'], [2, 's'], [3, 's'], [4, 's'], [5, 's'], [12, 's'], [13, 's']]
    # sFlushSuit = [0, 0, 0, 7]
    # sFlushRanks = [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1]
    # print(straightFlush(StraightFLush, sFlushSuit, sFlushRanks, suitList))

    # SAMPLE CONDITION FOR 4 OF A KIND
    # fourKindRanks = [0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]
    # print(fourOfAKind(fourKindRanks))

    # SAMPLE CONDITION FOR FULL HOUSE
    # fullHouseRanks = [0, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # print(fullHouse(fullHouseRanks))

    # SAMPLE CONDITION FOR FLUSH
    # ['Flush', 10]
    # flushHand = [[1, 's'], [6, 's'], [3, 's'], [7, 's'], [9, 's'], [12, 'd'], [13, 'd']]
    # flushSuit = [0, 2, 0, 5]
    # print(flush(flushHand, flushSuit, suitList))

    # SAMPLE CONDITION FOR STRAIGHT FLUSH
    # straightRank = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    # print(straight(straightRank))

    # SAMPLE CONDITION FOR THREE OF A KIND
    # threeOfAKindRank = [0, 3, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0]
    # print(threeOfAKind(threeOfAKindRank))

    # SAMPLE CONDITION FOR TWO PAIR
    # twoPairRanks = [0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0]
    # print(twoPair(twoPairRanks))

    # SAMPLE CONDITION FOR ONE PAIR
    # onePairRanks = [0, 0, 0, 2, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]
    # print(onePair(onePairRanks))

    # SAMPLE CONDITION FOR HIGH CARD
    # highCardRank = [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]
    # print(highCard(highCardRank))


def checkHand(player, bot, river):
    """
    Encapsulates all the hand scoring functions into one for the game to display
    :param player: the players hand (2 cards)
    :type player: Player
    :param bot: the Bot's hand (2 cards)
    :type bot: Bot
    :param river: 5 River cards
    :type river: River
    :return: The bot score, player score, and the ending result
    :rtype: list
    """
    pHand = player.addRiver(river).copy()
    bHand = bot.addRiver(river).copy()
    bScore = score(bHand)
    pScore = score(pHand)
    result = (endText(bScore, pScore))
    return ['Player: ' + pScore[0], 'Bot: ' + bScore[0], result]


class Text:
    """
    Used to handle all of the text that you will see on the game
    """

    def __init__(self, screen, MinimumWager: int):
        """
        Constructor method
        :param screen: What the text will be drawn to
        :param MinimumWager: The Minimum wager of the game
        :type MinimumWager: int
        """
        self._minWager = MinimumWager
        self.firstTurn = True
        self._WHITE = [255, 255, 255]
        self._RED = [255, 0, 0]
        self._screen = screen
        self._smallFont = pygame.font.SysFont(None, 25)
        self._medFont = pygame.font.SysFont(None, 50)
        self._largeFont = pygame.font.SysFont(None, 70)
        self._minWTxt = self._smallFont.render('Minimum wager: $' + str(MinimumWager), True, self._WHITE)
        self._potTxt = self._medFont.render('POT: $' + str(MinimumWager + MinimumWager), True, self._WHITE)
        self._checkTxt = self._largeFont.render('CHECK', True, self._WHITE)
        self._raiseTxt = self._largeFont.render('RAISE', True, self._WHITE)
        self._foldTxt = self._largeFont.render('FOLD', True, self._WHITE)
        self._foldScreenTxt = self._largeFont.render('YOU FOLDED', True, self._RED)
        self._playAgainTxt = self._medFont.render("Play again? (Press space)", True, self._WHITE)
        self._checkEventTxt = self._smallFont.render('You check, bot raises min. wager. ($' +
                                                     str(MinimumWager) + ')',
                                                     True, self._WHITE)
        self._raiseAmountTxt = self._largeFont.render('Amount: $', True, self._WHITE)

    def display(self, pot):
        """
        This function is the normal state of the game, meaning you are deciding on what to do
        :param pot: total pot of the game
        :type pot: int
        """

        self._potTxt = self._medFont.render('POT: $' + str(pot), True, self._WHITE)
        self._screen.blit(self._checkTxt, (80, 627))
        self._screen.blit(self._raiseTxt, (362, 627))
        self._screen.blit(self._foldTxt, (640, 627))
        self._screen.blit(self._potTxt, (70, 30))
        self._screen.blit(self._minWTxt, (642, 30))

    def displayMessage(self, pot=0):
        """
        Text that pops up when you raise, also indicates that the bot matched your raise
        :param pot: bad naming, but it's the amount you raised too lazy to change now haha
        :return: displays the amount you raised and that the bot matched your raise
        """
        if pot == 0:
            self._screen.blit(self._checkEventTxt, (70, 67))
        else:
            raiseEventTxt = self._smallFont.render('You raise, bot matches raise. ($' + str(pot) + ')', True,
                                                   self._WHITE)
            self._screen.blit(raiseEventTxt, (70, 67))

    def display1(self, pot, player, bot, river):
        """
        Displays the end game screen showing who won and saying if you want to play again
        :param pot: Total pot
        :type pot: int
        :param player: player hand
        :type player: Player
        :param bot: bot hand
        :type bot: Bot
        :param river: river cards
        :type river: River
        :return:
        """
        if river.length() == 5:
            pScore = checkHand(player, bot, river)[0]
            botScore = checkHand(player, bot, river)[1]
            result = checkHand(player, bot, river)[2]
            playerScore = self._medFont.render(pScore, True, self._WHITE)
            botScore = self._medFont.render(botScore, True, self._WHITE)
            resultText = self._largeFont.render(result, True, self._WHITE)
            self._screen.blit(playerScore, (70, 97))
            self._screen.blit(botScore, (70, 132))
            self._screen.blit(resultText, (270, 620))

        self._potTxt = self._medFont.render('POT: $' + str(pot), True, self._WHITE)
        self._screen.blit(self._potTxt, (70, 30))
        self._screen.blit(self._minWTxt, (642, 30))
        self._screen.blit(self._playAgainTxt, (220, 680))

    def display2(self):
        """
        You get this text when you fold
        """
        self._screen.blit(self._foldScreenTxt, (275, 623))
        self._screen.blit(self._playAgainTxt, (220, 680))

    def display3(self, pot):
        """
        This is used when you check and the bot raises the minimum wager
        :param pot: the pot in the game
        """
        self._potTxt = self._medFont.render('POT: $' + str(pot), True, self._WHITE)
        self._screen.blit(self._potTxt, (70, 30))
        self._screen.blit(self._minWTxt, (642, 30))
        self._screen.blit(self._raiseAmountTxt, (50, 627))

    def raiseAmount(self, text):
        """
        The Raise menu player uses that constantly gets updated
        When you press raise and starting pressing numbers this is what it gets drawn onto
        :param text: the user inputted number
        :type text: string
        """
        potTxt = self._largeFont.render(str(text), True, self._WHITE)
        self._screen.blit(potTxt, (300, 626))


class Square:
    """
    The 3 buttons for check, raise, and call
    """

    def __init__(self, COLOR, POS, SIZE, screen):
        """
        Constructor method
        :param COLOR: The rgb values of a color
        :param POS: position of the square
        :param SIZE: size of the square
        :param screen: what the square will be drawn onto
        """
        pygame.draw.rect(screen, COLOR, pygame.Rect(POS[0], POS[1], SIZE[0], SIZE[1]), 0, 3)


class Background:
    """
    Draws what we tried to make look like a poker table
    Draws a big brown square and a smaller green squre inside
    """

    def __init__(self, screen):
        """
        Constructor method
        :param screen: What the table will be drawn onto
        """
        self._BROWN = [78, 53, 36]
        self._GREEN = [0, 135, 62]
        self._SIZE_BROWN = [790, 580]
        self._SIZE_GREEN = [750, 550]
        self._POS_BROWN = [45, 12]
        self._POS_GREEN = [65, 25]
        self._screen = screen

    def display(self):
        """
        :return: Draws the table onto the screen
        """
        Square(self._BROWN, self._POS_BROWN, self._SIZE_BROWN, self._screen)
        Square(self._GREEN, self._POS_GREEN, self._SIZE_GREEN, self._screen)


class Buttons:
    """
    Gives the squares function of a button such as hovering and click detection
    """

    def __init__(self, screen):
        """
        Constructor method
        :param screen: What the button will be applied to
        """
        self._BLUE = [116, 181, 223]
        self._YELLOW = [235, 175, 0]
        self._SIZE = [255, 100]
        self._POS = 45
        self._screen = screen
        self._mouseOnCheck = False
        self._mouseOnRaise = False
        self._mouseOnFold = False

    def updateMousePos(self, pos):
        """
        Constantly updates to keep track of the mouse position and detects if moues is hovering one of the buttons
        :param pos: Position of the mouse
        :type pos: list
        """
        self._mouseOnCheck = 45 <= pos[0] <= 300 and 600 <= pos[1] <= 700
        self._mouseOnRaise = 313 <= pos[0] <= 568 and 600 <= pos[1] <= 700
        self._mouseOnFold = 580 <= pos[0] <= 835 and 600 <= pos[1] <= 700

    def display(self):
        """
        Will draw blue squares but if mouse is hovering one of the buttons will draw the square yellow
        """
        if self._mouseOnCheck:
            (Square(self._YELLOW, [self._POS, 600], self._SIZE, self._screen))
        else:
            (Square(self._BLUE, [self._POS, 600], self._SIZE, self._screen))
        if self._mouseOnRaise:
            (Square(self._YELLOW, [self._POS + 265, 600], self._SIZE, self._screen))
        else:
            (Square(self._BLUE, [self._POS + 265, 600], self._SIZE, self._screen))
        if self._mouseOnFold:
            (Square(self._YELLOW, [self._POS + 530, 600], self._SIZE, self._screen))
        else:
            (Square(self._BLUE, [self._POS + 530, 600], self._SIZE, self._screen))

    def update(self):
        """
        Detects if a button is clicked
        :return: A letter c r f
        :rtype: str
        """
        if self._mouseOnCheck:
            return 'c'
        if self._mouseOnRaise:
            return 'r'
        if self._mouseOnFold:
            return 'f'


class Game:
    """
    Main hub for all the classes and functions to interact with each other in a nice encapsulated class
    """
    MINIMUM_WAGER = 20

    # MINIMUM_WAGER = -20
    # MINIMUM_WAGER = 'A'
    def __init__(self, screen):
        """
        Default constructor
        :param screen: main drawing screen
        """
        self._pot = Game.MINIMUM_WAGER + Game.MINIMUM_WAGER
        self._screen = screen
        self._BLACK = [0, 0, 0]
        self._state = 0  # 0 is normal 1 is game end 2 is fold end 3 is raising
        self._deck = Deck()
        self._background = Background(screen)
        self._button = Buttons(screen)
        self._player = Player(self._deck)
        self._bot = Bot(self._deck)
        self._river = River(self._deck)
        self._mousePos = [0, 0]
        self._text = Text(screen, Game.MINIMUM_WAGER)
        self._quit = False
        self._mostRecentButton = 0
        self._raising = False
        self._raisePrompt = ''
        self._tempHoldRaise = ''

    def display(self):
        """
        displays everything to the game keeping track of what buttons were pressed
        """
        self._screen.fill(self._BLACK)
        self._mousePos = pygame.mouse.get_pos()
        self._background.display()
        self._button.updateMousePos(self._mousePos)

        if self._mostRecentButton == 1:
            self._text.displayMessage()
        self._player.display(self._screen)
        self._bot.display(self._screen)
        self._river.display(self._screen)

        if self._mostRecentButton == 2:
            self._text.displayMessage(self._tempHoldRaise)
        if self._state == 0:
            self._button.display()
            self._text.display(self._pot)

        if self._state in [1, 2]:
            self._bot.display1(self._screen)
            self._text.display1(self._pot, self._player, self._bot, self._river)
            if self._state == 2:
                self._text.display2()
        if self._state == 3:
            self._text.display3(self._pot)
            self._text.raiseAmount(self._raisePrompt)

    def click(self):
        """
        Detects clicking and how to correctly handle the click event
        """
        if self._state == 0:
            if self._button.update() == 'c':
                self._mostRecentButton = 1
                self._pot += Game.MINIMUM_WAGER
                # self._pot += "a"
                # self._pot += -30

                self._river.newTurn(self._deck, self._screen)
                if self._river.length() == 5:
                    self._quit = True
                    self._state = 1

            elif self._button.update() == 'r':
                self._state = 3
                self._mostRecentButton = 2

            elif self._button.update() == 'f':
                self._mostRecentButton = 0
                self._quit = True
                self._state = 2

    def quit(self):
        """
        User quits by exiting
        """
        return self._quit

    def newGame(self):
        """
        After a game is finished and the user presses space it will start a fresh new game
        """
        self._mostRecentButton = 0
        self._state = 0
        self._pot = Game.MINIMUM_WAGER + Game.MINIMUM_WAGER
        self._quit = False
        self._deck = Deck()
        self._button = Buttons(self._screen)
        self._player = Player(self._deck)
        self._bot = Bot(self._deck)
        self._river = River(self._deck)
        self._raisePrompt = ''
        self._tempHoldRaise = ''

    def raising(self):
        """
        This is when you are currently inputting a raise and are using the numkeys
        """
        return self._state == 3

    def raiseEvent(self, event):
        """
        Opens up the numkeys for use to input your raise amount
        once you are done you press return
        can only raise more or equal the minimum wager and can't raise higher than the current pot
        :param event: The input of the keyboard
        """
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if pygame.key.name(event.key) in nums:
            if len(self._raisePrompt) == 5:
                self._raisePrompt = self._raisePrompt[1:]
            self._raisePrompt += pygame.key.name(event.key)

        if event.key == pygame.K_BACKSPACE:
            self._raisePrompt = self._raisePrompt[:-1]

        if event.key == pygame.K_RETURN:
            if self._raisePrompt != '':
                if Game.MINIMUM_WAGER <= int(self._raisePrompt) <= self._pot:
                    self._pot += int(self._raisePrompt) + int(self._raisePrompt)
                    self._state = 0
                    self._mostRecentButton = 2
                    self._tempHoldRaise = self._raisePrompt
                    self._raisePrompt = ''
                    self._river.newTurn(self._deck, self._screen)
                    if self._river.length() == 5:
                        self._quit = True
                        self._state = 1


if __name__ == "__main__":
    def main():
        """
        Creates the screen and uses the game class to create all the variables needed to play
        :return:
        """
        screen = pygame.display.set_mode(DIMENSIONS)
        running = True
        clock = pygame.time.Clock()
        s = Game(screen)
        while running:
            s.display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    s.click()
                if event.type == pygame.KEYUP:
                    if s.raising():
                        s.raiseEvent(event)

                    if event.key == pygame.K_SPACE and s.quit():
                        s.newGame()

            pygame.display.flip()
            clock.tick(60)


    main()
