from GUI import GUI
from Actor import Enemy,Player
from ActorController import ActorController
from field import field
from game import game

def main():
    room1_act=ActorController()
    room1_act.add_actor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":8,"y":1,"dist":1,"image":258}),target=room1_act.player)
    room1_act.add_actor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":3,"y":4,"dist":1,"image":267}),target=room1_act.player)

    room1_map=field(name="room1",x=10,y=10)
    room1_map.door[1][1]=["room2",8,8]

    room2_act = ActorController()
    p = Player({"name": "Player", "SPD": 20, "HP": 100, "STR": 150, "DEF": 5, "x": 5, "y": 5,"image":282})
    room2_act.add_actor_as_player(p)
    room2_act.add_actor(Enemy({"name": "bat", "SPD": 10, "HP": 5, "STR": 10, "DEF": 8, "x": 1, "y": 1, "dist": 1,"image":258}),
                        target=room2_act.player)
    room2_act.add_actor(Enemy({"name": "bat", "SPD": 10, "HP": 5, "STR": 10, "DEF": 8, "x": 8, "y": 1, "dist": 1,"image":267}),
                        target=room2_act.player)
    room2_map = field(name="room2",x=30,y=30)
    room2_map.create_boarder()
    room2_map.rise_wall()
    room2_map.door[8][8] = ["room1", 1, 1]
    gm = game([{"field": room1_map, "ActorController": room1_act}, {"field": room2_map, "ActorController": room2_act}], 1)
    g=GUI(gm)
    g.run()

if __name__ == '__main__':
    main()
