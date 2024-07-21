# Connect Four Game

## Overview

This is a Connect Four game implemented using Flask for the backend and JavaScript for the frontend. The game allows a player to compete against an AI agent. The AI agent uses a Minimax algorithm with alpha-beta pruning for its moves.

## Game Description

Connect Four is a two-player connection game in which the players take turns dropping colored discs from the top into a vertically suspended grid. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs. The game is simple to learn but can involve complex strategies.

## How to Play

1. **Starting the Game**: When you open the game in your web browser, a new game board will be displayed. You will play as the red player, and the AI will play as the yellow player.
2. **Making a Move**: Click on a column to drop your disc into that column. The disc will occupy the lowest available space within the column.
3. **Winning the Game**: The game will automatically detect if you or the AI has formed a horizontal, vertical, or diagonal line of four discs, and will declare the winner.
4. **Resetting the Game**: You can reset the game at any time by clicking the "Reset" button, which will clear the board and start a new game.

## Agent

The agent for this Connect Four game uses a Minimax algorithm with alpha-beta pruning to determine the best moves. Here’s a brief overview of how the AI works:

- **Minimax Algorithm**: This algorithm is used to choose an optimal move for the AI. It simulates all possible moves, calculates the potential outcomes, and selects the move that maximizes the AI's chances of winning while minimizing the player's chances.
- **Alpha-Beta Pruning**: This technique is used to optimize the Minimax algorithm by eliminating branches in the game tree that do not need to be explored. This significantly reduces the computation time, allowing the AI to make decisions more quickly.
- **Heuristic Evaluation**: The AI uses a heuristic evaluation function to assign scores to board states. This function considers various factors, such as the number of potential winning lines for the AI and the player.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Himanshu-0502/Connect-Four.git
    cd Connect-Four
    ```

2. Install the Dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the Flask App:
    ```sh
    python app.py
    ```

## Acknowledgements

This project was inspired by the classic Connect Four game. Special thanks to all contributors and developers who have worked on similar projects and shared their knowledge online.
