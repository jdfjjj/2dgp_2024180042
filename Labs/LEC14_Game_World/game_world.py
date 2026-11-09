# world = [] # 1차원 리스트

world = [[], []]  # 0번, 1번 레이어를 가지는 2차원 리스트


# 게임월드에 객체 추가, layer 를 지정해야 한다.
def add_object(o, depth = 0):
    world[depth].append(o)

# 게임월드에서 객체 제거
def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return      # 더이상 찾을 필요가 없으므로 return 으로 함수 종료, 최적화

# game logic
def update():
    for layer in world:
        for o in layer:
            o.update()

# game rendering
def render():
    for layer in world:
        for o in layer:
            o.draw()
