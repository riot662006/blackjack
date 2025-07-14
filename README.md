# 🃏 Blackjack Simulator
A **stylized, terminal-based, object-oriented Blackjack simulator** built with Python. Experience a rich, ASCII-rendered card game that brings the feel of a casino to your command line. Complete with real betting mechanics, dealer logic, face-down cards, and a visual deck—this isn't your average text-based game. It's Blackjack with flair.

## 🎯 Features
- 🎨 Beautiful Card Art: Custom ASCII art for every card, including animations for face-down dealer cards.

- 💸 Betting System: Simulate real stakes with entry fees, double-downs, and pot calculations.

- 🧠 Smart Dealer AI: Dealer hits on soft 17 and reveals cards dynamically.

- 🔁 Multiple Rounds: Keep playing as long as you can afford the bid—or walk away a winner.

- 🧾 User Input Validation: Smooth and safe inputs with friendly error messages and prompts.

## 🧱 Object-Oriented Design
This project is built with **clean OOP principles**:

- `Card` and `Deck` classes encapsulate all logic for card creation, display, and manipulation.
- `Deck` is a subclass of `list`, enabling intuitive iteration and slicing while adding custom methods.
- ASCII rendering is handled in reusable `display()` methods, separated from game logic.
- `main()` manages gameplay flow, with reusable utility functions for input handling and game state.
- The design ensures **modularity**, **reusability**, and **easy extensibility** for future features (e.g. multiplayer or GUI).

## 🚀 How to Run
Make sure you have Python installed, then:

```bash
python blackjack.py
```
No external libraries needed.

## 🔍 About
**Blackjack Simulator** brings the drama and style of a casino table into your terminal. Built for solo players who want more than just logic—this game is wrapped in visual detail, pacing, and personality. Whether you're here to test your strategy or just enjoy a few rounds of well-crafted fun, this simulator deals more than just cards—it delivers an experience.

## 🛠 Tech Stack
- Language: Python 3
- Rendering: Custom ASCII Art

📸 Preview
 ```log 
  _______     _______ 
|A      |   |/// \\\|
|       |   |\\\ ///|
|   ♠   |   |<<<|>>>|
|       |   |/// \\\|
|       |   |\\\ ///|
|______A|   |_______|
```
## 🔮 Planned Features (Optional)
- Multi-player support (hot-seat)
- Save & resume game
- GUI or web-based version with same core logic
- Card counting training mode
- Leaderboards & high scores
