from GUI import GUI
from Actor import Enemy,Player
from ActorController import ActorController
from field import field
from game import game
from random import randint

def main():
    def generate_map(n):
        maps=[]
        for i in range(n):
            map_=field(name=str(i),x=randint(20,40),y=randint(20,40))
            #map_.create_boarder()
            #map_.create_room(randint(0,map_.width-6),randint(0,map_.height-6),randint(3,6),randint(3,6))
            map_.rise_wall(map_.width*map_.height//10)
            maps.append(map_)
        return maps
    def generate_actor_from_map(maps):
        res=[]
        for map_ in maps:
            act_ctr=ActorController()
            for _ in range(map_.width*map_.height//50):
                act_ctr.add_actor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,\
                "DEF":5,"x":randint(0,map_.width-1),"y":randint(0,map_.height-1),"dist":1,"image":267}),target=None)
            if res:
                prev=res[-1]

                prev_x=randint(0,prev["field"].width-1)
                prev_y=randint(0,prev["field"].height-1)
                cur_x=randint(0,map_.width-1)
                cur_y=randint(0,map_.height-1)

                prev["field"].door[prev_y][prev_x]=[map_,act_ctr,cur_x,cur_y]
                map_.door[cur_y][cur_x]=[prev["field"],prev["ActorController"],prev_x,prev_y]

            res.append({"field":map_,"ActorController":act_ctr})
        p = Player({"name": "Player", "SPD": 20, "HP": 100, "STR": 150, "DEF": 5, "x": 0, "y": 0,"image":282})
        res[0]["ActorController"].add_actor_as_player(p)
        res[0]["ActorController"].update_target(res[0]["ActorController"].player)
        return res

    maps=generate_map(10)

    gm = game(generate_actor_from_map(maps))
    g=GUI(gm)
    g.run()

if __name__ == '__main__':
    import cProfile ,pstats,io
    pr=cProfile.Profile()
    pr.enable()
    main()
    pr.disable()
    s=io.StringIO()
    sortby="cumulative"
    ps=pstats.Stats(pr,stream=s).sort_stats(sortby)
    ps.print_stats()
    #print(s.getvalue())
