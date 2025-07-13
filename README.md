# 🎮 Monster Shooter

**Monster Shooter** is a top-down 2D action shooter where the player is trapped in a deadly monster world. The objective is simple: **survive**. Enemies come in waves, each introducing new challenges.

---

## 🧍 Player Character

You control a lone survivor armed with a rifle. The player can:

- 🎮 Move freely using `W`, `A`, `S`, `D` keys.
- 🖱️ Aim and shoot in full 360° using the mouse.
- 💥 Take damage from enemies or projectiles.

---

## 👾 Enemy Types

There are three distinct enemy types, each with unique behaviors:

### 1. 🟢 Little Orc
- Fast-moving swarm attacker.

### 2. 🔥 Big Demon
- Large and slow.
- Periodically launches **fireballs** toward the player.
- Fireballs remain active even after the demon dies.

### 3. 💣 Suicide Bomber
- Sprints toward the player.
- Explodes in close range, dealing **massive** damage.
  
---

## 🌊 Wave System

The game progresses through **three waves**, each featuring a new enemy type and increasing difficulty.

| **Wave** | **Enemy Type**      | **Traits**                            |
|----------|---------------------|----------------------------------------|
| 1        | Little Orcs         | Swarm attackers                        |
| 2        | Big Demons          | Launch fire projectiles                |
| 3        | Suicide Bombers     | Explode near the player                |

---

# ▶️ How to Run the Game

Follow these steps to get the game up and running on your local machine.

---

### 1. Clone the Repository

First, clone the game's repository to your local machine using Git:

```bash
git clone https://github.com/faisal-askani/Top-Down-Shooter.git
cd Top-Down-Shooter
```

### 2. Install uv (if not already installed)
   
```bash
pip install uv
```

### 3. Create and Sync the Environment
  - Navigate into the cloned repository and set up a virtual environment using uv. This ensures all dependencies are isolated from your system's Python installation.
    
```bash
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 4. After activating the virtual environment, install the necessary game dependencies, including Pygame, and sync with requirements.txt.

```bash
uv pip install -r requirements.txt
```

### 4. Run the Game
  - Once all dependencies are installed and your virtual environment is active, you can start the game.

```bash
python main.py
```
