import pygame
import random
import time
import statistics

# game stats
width = 1000
height = 650
blocksize = 30
gameWidth = 10
gameHeight = 20
windowWidth = gameWidth*blocksize
windowHeight = gameHeight*blocksize
topScore = 0

# shapes created by following 4x4 matrix:
# 0  1  2  3
# 4  5  6  7
# 8  9  10 11
# 12 13 14 15
# and their possible rotations
# idea from source 
blocks = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8], [0, 4, 5, 6]],
    [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],
    [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],
    [[1, 2, 5, 6]]
]

# the colours the blocks can be
colours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
        

class Tetronimo:
    # settting up all information about the tetronimo
    def __init__(self, num):
        self.x = 3
        self.y = -4
        self.type = num
        self.colour = colours[num]
        self.rotation = 0
    
    # a function to reuturn the shape type and its rotation
    def image(self):
        return blocks[self.type][self.rotation]

    # functions to rotate the tetrinomo
    def rotate_clockwise(self):
        self.rotation = (self.rotation + 1) % len(blocks[self.type])
    
    def rotate_anticlockwise(self):
        self.rotation = (self.rotation - 1) % len(blocks[self.type])

class Tetris:

    # setting up board, scores and creating an array that represents the board 
    def __init__(self):
        self.width = gameWidth
        self.height = gameHeight
        self.field = []
        self.score = 0
        self.blocksize = blocksize
        self.block = None
        self.nextBlock = None
        self.playing = True
        self.blockNums = 0
        self.level = 1
        self.line_clears = 0
        self.numOfBlocks = 0
        self.bag = []
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)

    def get_bag_shape(self):
        if len(self.bag) == 0:
            self.bag = [0, 1, 2, 3, 4, 5, 6]
            random.shuffle(self.bag)
        return self.bag.pop()

    def current_block(self):
        self.block = self.nextBlock
        self.next_block()
        self.numOfBlocks += 1

    def next_block(self):
        self.nextBlock = Tetronimo(self.get_bag_shape())

    def intersection(self):
        intersect = False
        for i in range(4):
            for j in range(4):
                if i*4 + j in self.block.image():
                    # block at right side of screen, block at left side of screen
                    if (j + self.block.x > self.width - 1) or (j + self.block.x < 0):
                        intersect = True
                    # checks if on board
                    if i + self.block.y >= 0:
                        # checks if on board
                        if (j + self.block.x > self.width - 1) or (j + self.block.x < 0):
                            intersect = True
                        # block hits bottom
                        elif i + self.block.y  > self.height -1:
                            intersect = True
                        # intersects with another block
                        elif self.field[i + self.block.y][j + self.block.x] != 0:
                            intersect = True
        return intersect

    def row_clear(self):
        lines = 0
        for i in range(0, self.height):
            zeros = 0
            newLines = []
            for x in range (self.width):
                newLines.append(0)
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                self.field.pop(i)
                self.field = [newLines] + self.field
        
        # adjusts score and level
        self.line_clears += lines
        if lines == 1:
            self.score += 40*self.level
        if lines == 2:
            self.score += 100*self.level
        if lines == 3:
            self.score += 300*self.level
        if lines == 4:
            self.score += 1200*self.level
        if self.line_clears >= 10:
            self.level += 1
            self.line_clears -= 10

    # freezes a block when it hits the bottom or another block
    def freeze(self):
        if self.block.y < 0:
            self.playing  = False
        else:
            for i in range(4):
                for j in range(4):
                    if i *4 + j in self.block.image():
                        # makes block permanent
                        self.field[i + self.block.y][j + self.block.x] = self.block.colour
                    
            self.row_clear()
            self.current_block()

    # movement controlls        
    def falling(self):
        self.block.y += 1
        if self.intersection() == True:
            self.block.y -= 1
            self.freeze()

    def down(self):
        self.block.y += 1
        if self.intersection() == True:
            self.block.y -= 1
    
    def left(self):
        self.block.x -= 1
        if self.intersection() == True:
            self.block.x += 1
    
    def right(self):
        self.block.x += 1
        if self.intersection() == True:
            self.block.x -= 1

    def drop(self):
        while self.intersection() != True:
            self.block.y +=1
        self.block.y -= 1
        self.freeze()

    def rotate_clockwise(self):
        self.block.rotate_clockwise()
        if self.intersection() == True:
            self.block.rotate_anticlockwise()
    
    def rotate_anticlockwise(self):
        self.block.rotate_anticlockwise()
        if self.intersection() == True:
            self.block.rotate_clockwise()

class TetrisAI(Tetris):

    # setting up board, scores and creating an array that represents the board 
    def new_block(self):
        self.block = Tetronimo(0)

    # freezes a block when it hits the bottom or another block
    def freeze(self):
        if self.block.y < 0:
            self.playing  = False
        else:
            for i in range(4):
                for j in range(4):
                    if i *4 + j in self.block.image():
                        # makes block permanent
                        self.field[i + self.block.y][j + self.block.x] = self.block.colour
                        
    def left(self):
        while self.intersection() != True:
            self.block.x -= 1
        self.block.x += 1
    
    def right(self):
        self.block.x += 1

class AI:

    def __init__(self):
        self.weights = []
        self.gameScores = []
        self.gen = 1
        self.learning = True
        self.num = 0
        self.topWeights = []
        self.topScores = []
        self.meanHeight = 0
        self.holes = 0
        self.standardDeviation = 0
        self.heightRange = 0
        self.maxAdjacent = 0 
        self.maxHeight = 0
        self.weightedHoles = 0
        self.zeros = 0
        self.generations = 100
        self.trial = 1
        self.current_bot_scores = []

    def new_gen(self):
        # initial generation or reset
        if self.gen == 1 or self.zeros == 10:
            self.weights = []
            self.gameScores = []
            for i in range(10):
                tempList = []
                for j in range(8):
                    tempList.append(random.randint(1,100)/100)
                self.weights.append(tempList)
        else:
            # at this point, self.weights ONLY contains the top 2 parents from fitness()
            # we need to fill the list back up to 10 bots.
            
            # save copies of parents for breeding so we don't accidentally modify them
            parent1 = list(self.weights[0])
            parent2 = list(self.weights[1])


            # 2 mutated clones
            # create a copy of the top 2, but tweak their numbers slightly
            # this helps the AI "fine tune" a good strategy
            for i in range(2):
                new_clone = list(self.weights[i])
                for j in range(8):
                    # 20% chance to tweak a weight slightly
                    if random.randint(1, 5) == 1:
                        change = random.choice([-0.05, 0.05])
                        new_clone[j] = round(new_clone[j] + change, 2)
                self.weights.append(new_clone)


            # 4 offspring/crossover
            # randomly mix genes from Parent 1 and Parent 2
            for i in range(4):
                child = []
                for j in range(8):
                    if random.randint(0, 1) == 0:
                        child.append(parent1[j])
                    else:
                        child.append(parent2[j])
                
                # small chance of mutation in children too
                for j in range(8):
                    if random.randint(1, 20) == 1:
                        child[j] = random.randint(1,100)/100
                
                self.weights.append(child)


            # 2 completely random
            # "fresh" DNA to ensure we don't get stuck
            for i in range(2):
                tempList = []
                for j in range(8):
                    tempList.append(random.randint(1,100)/100)
                self.weights.append(tempList)

            self.gameScores = []


    def fitness(self):
        # gets top scores and corresponding weights and removes others
        combined = list(zip(self.gameScores, self.weights))
        # sort by score (descending)
        combined.sort(key=lambda x: x[0], reverse=True)
        
        # keep top 2
        self.topScores = [x[0] for x in combined[:2]]
        self.topWeights = [x[1] for x in combined[:2]]
        
        self.weights = self.topWeights
        # self.gameScores is cleared in new_gen()

    def fieldStats(self, bot):
        self.meanHeight = 0
        self.holes = 0
        self.standardDeviation = 0
        self.heightRange = 0
        self.maxAdjacent = 0
        self.maxHeight = 0
        self.weightedHoles = 0
        
        # gets all required data from board
        heights = []
        total = 0
        for i in range(10):
            filled = 0
            for j in range(20):
                if bot.field[j][i] != 0:
                    heights.append((20-j))
                    filled += 1
                    break
            if filled == 0:
                heights.append(0)
        total = 0
        for i in heights:
            total += i
        self.meanHeight = total/10
        self.maxHeight = max(heights)
        self.heightRange = max(heights) - min(heights)
        diffSquared = 0
        for i in heights:
            diffSquared += (i-self.meanHeight)**2
        self.standardDeviation = (diffSquared/10)**0.5
        self.standardDeviation = round(self.standardDeviation,2)
        for i in range(9):
            diff = abs(heights[i] - heights[i+1])
            if diff > self.maxAdjacent:
                self.maxAdjacent = diff
        
        # checks number of holes and weighted holes
        for i in range(10):
            blocks_above = 0
            checkHoles = False
            for j in range(20):
                if bot.field[j][i] != 0:
                    checkHoles = True
                    blocks_above += 1
                if checkHoles:
                    if bot.field[j][i] == 0:
                        self.holes += 1
                        self.weightedHoles += blocks_above

    def play(self, type, next_type, colour, rotation, grid):
        bot = TetrisAI()
        bot.new_block()
        bot.block.type = type
        bot.block.colour = colour
        bot.field = [row[:] for row in grid]
        
        # first pass: find all possible moves for current block and score them
        outcomes_pass_1 = []
        for rot in range(len(blocks[type])):
            for x in range(-4, 11):
                bot.block.x = x
                bot.block.rotation = rot
                bot.block.y = -4
                if bot.intersection(): continue

                while not bot.intersection():
                    bot.block.y += 1
                bot.block.y -= 1

                placed = []
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in bot.block.image():
                            r, c = i + bot.block.y, j + bot.block.x
                            if 0 <= r < 20 and 0 <= c < 10:
                                bot.field[r][c] = bot.block.colour
                                placed.append((r, c))
                
                lh = 20 - bot.block.y
                self.fieldStats(bot)
                
                pass1Score = (
                        (self.weights[self.num][0])*self.meanHeight + 
                        (self.weights[self.num][1])*self.holes + 
                        (self.weights[self.num][2])*self.standardDeviation + 
                        (self.weights[self.num][3])*self.heightRange + 
                        (self.weights[self.num][4])*self.maxAdjacent + 
                        (self.weights[self.num][5])*self.maxHeight +
                        (self.weights[self.num][6])*self.weightedHoles + 
                        (self.weights[self.num][7])*lh
                    )

                outcomes_pass_1.append({'x': x, 'rot': rot, 'score': pass1Score, 'placed': placed})
                
                for r, c in placed:
                    bot.field[r][c] = 0

        # optimization: sort by score and keep only the top 6 moves
        outcomes_pass_1.sort(key=lambda x: x['score'])
        outcomes_pass_1 = outcomes_pass_1[:6]

        # second pass: lookahead (check next block on the top 6 grids)
        bestScore = float('inf')
        bestMove = [3, 0, 0]
        
        for move1 in outcomes_pass_1:
            for r, c in move1['placed']:
                bot.field[r][c] = colour

            bot2 = TetrisAI()
            bot2.new_block()
            bot2.block.type = next_type 
            bot2.field = bot.field
            
            for rot2 in range(len(blocks[next_type])):
                for x2 in range(-4, 11):
                    bot2.block.x = x2
                    bot2.block.rotation = rot2
                    bot2.block.y = -4
                    if bot2.intersection(): continue
                    
                    while not bot2.intersection():
                        bot2.block.y += 1
                    bot2.block.y -= 1

                    placed2 = []
                    for i in range(4):
                        for j in range(4):
                            if i * 4 + j in bot2.block.image():
                                r, c = i + bot2.block.y, j + bot2.block.x
                                if 0 <= r < 20 and 0 <= c < 10:
                                    bot2.field[r][c] = bot2.block.colour
                                    placed2.append((r, c))
                    
                    lh2 = 20 - bot2.block.y
                    self.fieldStats(bot2)
                    
                    weightedOutcome = (
                        (self.weights[self.num][0])*self.meanHeight + 
                        (self.weights[self.num][1])*self.holes + 
                        (self.weights[self.num][2])*self.standardDeviation + 
                        (self.weights[self.num][3])*self.heightRange + 
                        (self.weights[self.num][4])*self.maxAdjacent + 
                        (self.weights[self.num][5])*self.maxHeight +
                        (self.weights[self.num][6])*self.weightedHoles + 
                        (self.weights[self.num][7])*lh2
                    )
                    
                    if weightedOutcome < bestScore:
                        bestScore = weightedOutcome
                        bestMove = [move1['x'], move1['rot'], bestScore]
                    
                    for r, c in placed2:
                        bot2.field[r][c] = 0

            for r, c in move1['placed']:
                bot.field[r][c] = 0
        
        if bestMove is None:
             return [0, 0, 0]

        return bestMove    
        

# actual game code
def Main(topScore):
    bot = AI()
    while bot.learning:

        clock = pygame.time.Clock()
        game = Tetris()
        counter = 0
        speed = 100 - 5*game.level
        if speed < 5:
            speed = 5
        
        if bot.weights == []:
            bot.new_gen()

        if len(bot.gameScores) == 10:
            bot.gen += 1
            bot.fitness()
            bot.new_gen()
            bot.num = 0

        if bot.gen != bot.generations+1:
            while game.playing:
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()

                if game.block == None:
                    if game.nextBlock == None:
                        game.next_block()
                        game.current_block()

                if counter >= speed:
                    game.falling()
                    counter = 0

                bestMove = AI.play(bot, game.block.type, game.nextBlock.type, game.block.colour, game.block.rotation, game.field)

                while bestMove[1] > game.block.rotation:
                    game.rotate_clockwise()
                while bestMove[1] < game.block.rotation:
                    game.rotate_anticlockwise()
                while bestMove[0] > game.block.x:
                    game.right()
                while bestMove[0] < game.block.x:
                    game.left()
                game.drop()


                # creates surface appearance
                screen.fill((55,198,255))
                pygame.draw.rect(screen, (11,102,35), pygame.Rect(0, height-(height-windowHeight)//2, width, (height-windowHeight)//2))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect((width-windowWidth)//2, (height-windowHeight)//2, windowWidth, windowHeight))
                for i in range(game.width):
                    for j in range(game.height):
                        pygame.draw.rect(screen, (230,230,230), pygame.Rect(i*blocksize + ((width-windowWidth)//2), j*blocksize + ((height-windowHeight)//2) , blocksize, blocksize), 1)

                # fills in falling blocks
                if game.block is not None:
                    for i in range(4):
                        for j in range(4):
                            if i*4 + j in game.block.image():
                                pygame.draw.rect(screen, game.block.colour, pygame.Rect(j*blocksize + game.block.x*blocksize + ((width-windowWidth)//2), i*blocksize + game.block.y*blocksize + ((height-windowHeight)//2), blocksize, blocksize))

                # fills in frozen blocks
                for i in range(game.height):
                    for j in range(game.width):
                        if game.field[i][j] != 0:
                            pygame.draw.rect(screen, game.field[i][j], pygame.Rect(j*blocksize + ((width-windowWidth)//2), i*blocksize + ((height-windowHeight)//2), blocksize, blocksize))

                # creates surface appearance
                pygame.draw.rect(screen, (0,0,0), pygame.Rect((width-windowWidth)//2, (height-windowHeight)//2, windowWidth, windowHeight),2)
                
                # covers top of screen
                pygame.draw.rect(screen, (55,198,255), pygame.Rect( ((width-windowWidth)//2), 0, windowWidth, ((height-windowHeight)//2)) )

                # displays next block
                if game.nextBlock is not None:
                    for i in range(4):
                        for j in range(4):
                            if i*4 + j in game.nextBlock.image():
                                pygame.draw.rect(screen, game.nextBlock.colour, pygame.Rect(770 + j*blocksize, 130 + i*blocksize, blocksize, blocksize))
                                

                # tetris title and score
                font = pygame.font.SysFont('Calibri', 30, True)
                text = font.render("LEVEL: " + str(game.level), True, (0,0,0))
                screen.blit(text, (20, 160))
                text = font.render("SCORE: " + str(game.score), True, (0,0,0))
                screen.blit(text, (20, 200))
                text = font.render("Generation: " + str(bot.gen), True, (0,0,0))
                screen.blit(text, (15, 240))
                text = font.render("Bot number: " + str(bot.num+1), True, (0,0,0))
                screen.blit(text, (15, 280))
                text = font.render("Trial: " + str(bot.trial) + "/5", True, (0,0,0))
                screen.blit(text, (15, 320))
                text = font.render("HIGH SCORE: " + str(topScore), True, (0,0,0))
                screen.blit(text, (15, 360))
                text = font.render("NEXT BLOCK: ", True, (0,0,0))
                screen.blit(text, (750, 100))
                font = pygame.font.SysFont('Calibri', 58, True)
                text = font.render("TETRIS", True, (0,0,0))
                screen.blit(text, (10, 100))
                pygame.display.update()

                counter += 1
                clock.tick(100)
        
            bot.current_bot_scores.append(game.score)
            if len(bot.current_bot_scores) == 5:
                # use median
                score_median = statistics.median(bot.current_bot_scores)
                bot.gameScores.append(score_median)
                bot.current_bot_scores = []
                bot.num += 1
                bot.trial = 1
            else:
                bot.trial += 1
                
            if game.score > topScore:
                topScore = game.score



    # game ending
    time.sleep(2)
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Calibri", 25)
    ending = font.render("Learning Finished!", True, (0,0,0))
    screen.blit(ending, (420, 300))
    font = pygame.font.SysFont("Calibri", 25)
    again = font.render("Top score was: " + str(topScore), True, (0,0,0))
    screen.blit(again, (420, 340))
    end = True
    while end:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
    pygame.quit()
    

# creates intro screen and starts game    
pygame.font.init()
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
font = pygame.font.SysFont("Calibri", 25)
intro = font.render("Press any key to start!", True, (0,0,0))
screen.blit(intro, (387, 300))
run = True
while run:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            Main(topScore)