import argparse
from lunges import Lunges
from dumbbell import DumbbellCurls
from pullup import PullUps
from legpress import LegPress

# from src.exercies.Pushup import Pushup
# from src.exercies.Plank import Plank
# from src.exercies.ShoulderTap import ShoulderTap
# from src.exercies.Squat import Squat


class GymLytics:
    def __init__(self):
        # self.pushup = Pushup()
        # self.plank = Plank()
        # self.squat = S
        # self.shoulderTap = ShoulderTap()
        self.pullup=PullUps()
        self.lunges = Lunges()
        self.dumbbell=DumbbellCurls()
        self.legpress=LegPress()
    def rep(self, type, source):
        # if type.lower() == str("pushup"):
            # self.pushup.exercise(source)
        # elif type.lower() == str("squat"):
            # self.squat.exercise(source)
        # elif type.lower() == str("plank"):
            # self.plank.exercise(source)
        if type.lower() == str("legpress"):
            self.legpress.exercise(source)
        if type.lower()==str("pullup"):
            self.pullup.exercise(source)
        if type.lower() == str("lunges"):
            self.lunges.exercise(source)
        if type.lower()==str("dumbbell"):
            self.dumbbell.exercise(source)
        else:
            raise ValueError(f"Input {type} and/or {source} is not correct. \n Kindly refer to the documentation")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-type', "--type", required=True, help="Type of exercise",
                        type=str)
    parser.add_argument('-source', "--source", required=True, help="Path to video source", type=str)
    args = parser.parse_args()
    type = args.type
    source = args.source
    gym = GymLytics()
    gym.rep(type, source)