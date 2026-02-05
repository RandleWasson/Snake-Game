import pygame, sys, time, random

speed = 15

#windows sizes

frame_size_x = 1380
frame_size_y= 840


check_errors = pygame.init()

if(check_errors[1] > 0):
    print("Error " + check_errors[1])
else:
    print("Game Succesfully initialized")
    
#initialise game window

pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# colors
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)

# Use pygame.font.Font(None, size) to load the bundled font file
SCORE_FONT = pygame.font.Font(None, 20)

fps_controller = pygame.time.Clock()
# one snake square size
square_size = 60

# =========================================================
# === LONG-TERM DATA STORAGE FUNCTIONS (.TXT) =============
# =========================================================

# Function to load scores from the file
def load_leaderboard():
    try:
        # 'r' mode opens the file for reading
        with open("leaderboards.txt", "r") as file:
            # Read all lines, strip whitespace, and convert to integers
            scores = [int(line.strip()) for line in file.readlines()]
            # Sort the scores in descending order
            scores.sort(reverse=True)
            return scores
    except FileNotFoundError:
        # If the file doesn't exist yet, return an empty list
        return []
    except ValueError:
        # Handle case where file content isn't a valid integer
        print("Error: Leaderboards file contains non-numeric data.")
        return []

# Function to update and save the leaderboard
def save_leaderboard(current_score):
    scores = load_leaderboard()
    scores.append(current_score)
    scores.sort(reverse=True)
    
    # Keep only the top 5 scores
    top_scores = scores[:5]

    # 'w' mode opens the file for writing (and overwrites existing content)
    with open("leaderboards.txt", "w") as file:
        for score in top_scores:
            # Write each score followed by a newline character
            file.write(f"{score}\n")

# =========================================================
# === GAME INITIALIZATION =================================
# =========================================================

def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction
    direction = "RIGHT"
    head_pos = [120,60]
    snake_body = [[120,60]]
    food_pos = [random.randrange(1,(frame_size_x // square_size)) * square_size, 
                random.randrange(1,(frame_size_y // square_size)) * square_size]
    food_spawn = True
    score = 0
    
init_vars()

# =========================================================
# === SCORE DISPLAY FUNCTION ==============================
# =========================================================

def show_score(choice, color):
    global SCORE_FONT 
    
    # 1. Display CURRENT Score (Top Left - choice 1)
    if choice == 1:
        score_surface = SCORE_FONT.render("Score: " + str(score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (frame_size_x / 10, 15)
        game_window.blit(score_surface, score_rect)

    # 2. Display FULL Leaderboard (Center - choice 2 - Game Over Screen)
    elif choice == 2:
        leaderboard = load_leaderboard()
        
        # Title
        title_surface = SCORE_FONT.render("HIGH SCORES", True, red)
        title_rect = title_surface.get_rect()
        title_rect.midtop = (frame_size_x/2, frame_size_y/4)
        game_window.blit(title_surface, title_rect)
        
        # List Scores
        y_offset = title_rect.bottom + 10 
        for i, s in enumerate(leaderboard):
            # Highlight the current score if it's in the top 5
            line_color = green if s == score and i < 5 else white
            
            score_line = f"{i+1}. {s}"
            score_surface = SCORE_FONT.render(score_line, True, line_color)
            score_rect = score_surface.get_rect()
            score_rect.midtop = (frame_size_x/2, y_offset)
            game_window.blit(score_surface, score_rect)
            y_offset += 30 # Move down for next score line


# =========================================================
# === GAME LOOP ===========================================
# =========================================================

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if ( event.key == pygame.K_UP or event.key == ord("w") 
                and direction != "DOWN"):
                direction = "UP"
            elif  ( event.key == pygame.K_DOWN or event.key == ord("s") 
                and direction != "UP"):
                direction = "DOWN"
            elif  ( event.key == pygame.K_LEFT or event.key == ord("a") 
                and direction != "RIGHT"):
                direction = "LEFT"
            elif  ( event.key == pygame.K_RIGHT or event.key == ord("d") 
                and direction != "LEFT"):
                direction = "RIGHT"
    
    if direction == "UP":
        head_pos[1] -= square_size
    elif direction == "DOWN":
        head_pos[1] += square_size
    elif direction == "LEFT":
        head_pos[0] -= square_size
    else:
        head_pos[0] += square_size
        
    if head_pos[0] < 0:
        head_pos[0] = frame_size_x - square_size
    elif head_pos[0] > frame_size_x - square_size:
        head_pos[0] = 0
    elif head_pos[1] < 0:
        head_pos[1] = frame_size_y - square_size
    elif head_pos[1] > frame_size_y - square_size:
        head_pos[1] = 0
        
    #eating apple
    snake_body.insert(0, list(head_pos))
    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # spawn food
    if not food_spawn:
        food_pos = [random.randrange(1,(frame_size_x // square_size)) * square_size, 
            random.randrange(1,(frame_size_y // square_size)) * square_size]
        food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
            pos[0] + 2, pos[1] + 2,
            square_size -2, square_size -2 ))
        
    pygame.draw.rect(game_window,red, pygame.Rect(food_pos[0], 
                        food_pos[1], square_size, square_size))
    
    # game over condiditons

    for block in snake_body[1:]:
        if head_pos[0] == block[0] and head_pos[1] == block[1]:
            
            # 1. Save score to external file
            save_leaderboard(score) 
            
            # 2. Display Game Over/Leaderboard Screen (choice 2)
            game_window.fill(black)
            show_score(2, white)
            pygame.display.update()
            
            # 3. Pause and reset
            time.sleep(3) 
            init_vars() 

    # Normal score display during game play
    show_score(1, white)
    pygame.display.update()
    fps_controller.tick(speed)