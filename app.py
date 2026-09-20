import streamlit as st
import random

# -----------------------------
# Game settings
# -----------------------------

GRID_SIZE = 7


# -----------------------------
# Start a new game
# -----------------------------

def new_game():
    st.session_state.snake = [(3, 3)]
    st.session_state.food = (1, 5)
    st.session_state.direction = "RIGHT"
    st.session_state.score = 0
    st.session_state.game_over = False


# Create the game for the first time
if "snake" not in st.session_state:
    new_game()


# -----------------------------
# Move the snake
# -----------------------------

def move_snake(direction):

    # Get the snake's current head
    head_row, head_col = st.session_state.snake[0]

    # Work out the new position
    if direction == "UP":
        new_head = (head_row - 1, head_col)

    elif direction == "DOWN":
        new_head = (head_row + 1, head_col)

    elif direction == "LEFT":
        new_head = (head_row, head_col - 1)

    else:
        new_head = (head_row, head_col + 1)

    # Check if the snake hits the wall
    if (
        new_head[0] < 0
        or new_head[0] >= GRID_SIZE
        or new_head[1] < 0
        or new_head[1] >= GRID_SIZE
    ):
        st.session_state.game_over = True
        return

    # Check if the snake hits itself
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return

    # Add the new head
    st.session_state.snake.insert(0, new_head)

    # Check if the snake eats the food
    if new_head == st.session_state.food:

        # Increase score
        st.session_state.score += 1

        # Find a new food position
        empty_spaces = []

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):

                if (row, col) not in st.session_state.snake:
                    empty_spaces.append((row, col))

        st.session_state.food = random.choice(empty_spaces)

    else:
        # Remove the tail
        st.session_state.snake.pop()


# -----------------------------
# Display the game
# -----------------------------

st.title("🐍 Mini Snake Game")

st.write("Use the buttons to move the snake.")
st.write("Eat the 🍎 to increase your score!")

# Score
st.subheader(f"🏆 Score: {st.session_state.score}")


# -----------------------------
# Draw the grid
# -----------------------------

for row in range(GRID_SIZE):

    row_display = ""

    for col in range(GRID_SIZE):

        position = (row, col)

        if position == st.session_state.snake[0]:
            row_display += "🐍 "

        elif position in st.session_state.snake:
            row_display += "🟢 "

        elif position == st.session_state.food:
            row_display += "🍎 "

        else:
            row_display += "⬜  "

    st.write(row_display)


# -----------------------------
# Game over message
# -----------------------------

if st.session_state.game_over:

    st.error("💥 Game Over!")

    if st.button("🔄 Play Again"):
        new_game()
        st.rerun()


# -----------------------------
# Movement buttons
# -----------------------------

else:

    st.write("### 🎮 Controls")

    # Up button
    if st.button("⬆️ UP"):
        move_snake("UP")
        st.rerun()

    # Left, Down and Right buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅️ LEFT"):
            move_snake("LEFT")
            st.rerun()

    with col2:
        if st.button("⬇️ DOWN"):
            move_snake("DOWN")
            st.rerun()

    with col3:
        if st.button("➡️ RIGHT"):
            move_snake("RIGHT")
            st.rerun()
