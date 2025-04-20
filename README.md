# Catch the Ball

A simple Python game built with Pygame where you control a platform to catch falling balls.

## Game Features

### Simple Version
- Control a platform to catch falling balls
- Score points for each ball caught
- Game over when a ball is missed

### Improved Version
- Ball bounces off platform and walls
- Lives system - you have 3 lives
- Score increases with each bounce
- SVG graphics for improved visuals
- Level progression as you score points

### Advanced Version
- Multiple colorful balls with different sizes and speeds
- Smaller balls are worth more points
- Lives system - miss up to 3 balls before game over
- Level progression - balls fall faster as you level up
- Improved visuals with gradient backgrounds and effects

## Controls
- Left arrow key: Move the platform left
- Right arrow key: Move the platform right
- Space: Restart the game (after game over)
- ESC: Quit the game

## Installation
1. Install the requirements:
```
pip install -r requirements.txt
```

2. Run the game launcher:
```
python launcher.py
```

Or run a specific version directly:
```
python game.py           # Simple version
python game_improved.py  # Improved version with bouncing ball
python enhanced_game.py  # Advanced version with multiple balls
```