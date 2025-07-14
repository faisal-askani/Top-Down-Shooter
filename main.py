import os


from game_manager import GameManager

if __name__ == "__main__":
    # os.environ['SDL_VIDEO_CENTERED'] = '1'
    manager = GameManager(num_orc=10, num_big_demons=7, num_suicide_bombers=6)

    manager.run()
