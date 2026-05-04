from abc import ABC
from enum import StrEnum
from typing import Iterable
import argparse
from constraint import (
    ExactSumConstraint,
    MaxSumConstraint,
    MinSumConstraint,
    Problem,
    RecursiveBacktrackingSolver,
)

class Color(StrEnum):
    WHITE = "w"
    BLUE = "u"
    BLACK = "b"
    RED = "r"
    GREEN = "g"


class LandType(StrEnum):
    BASIC = "basic"
    DUAL = "dual"
    SURVEIL = "surveil"
    TRIOME = "triome"
    FETCHLAND = "fetchland"


class Land(ABC):
    def __init__(
        self,
        name: str,
        tag: LandType,
        colors: Iterable[Color],
        tapped: bool = False,
    ):
        self.name = name
        self.tag = tag
        self.colors = set(colors)
        self.tapped = tapped

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name

    def __lt__(self, other):
        if other.tag != self.tag:
            return self.tag < other.tag
        if self.name == other.name:
            return False
        return not self.__gt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

    def __str__(self) -> str:
        return self.name


fetchlands = [
    Land("Polluted Delta", LandType.FETCHLAND, [Color.BLUE, Color.BLACK]),
    Land("Flooded Strand", LandType.FETCHLAND, [Color.WHITE, Color.BLUE]),
    Land("Bloodstained Mire", LandType.FETCHLAND, [Color.BLACK, Color.RED]),
    Land("Wooded Foothills", LandType.FETCHLAND, [Color.RED, Color.GREEN]),
    Land("Windswept Heath", LandType.FETCHLAND, [Color.WHITE, Color.GREEN]),
    Land("Scalding Tarn", LandType.FETCHLAND, [Color.BLUE, Color.RED]),
    Land("Verdant Catacombs", LandType.FETCHLAND, [Color.BLACK, Color.GREEN]),
    Land("Marsh Flats", LandType.FETCHLAND, [Color.WHITE, Color.BLACK]),
    Land("Misty Rainforest", LandType.FETCHLAND, [Color.BLUE, Color.GREEN]),
    Land("Arid Mesa", LandType.FETCHLAND, [Color.WHITE, Color.RED]),
]

basics = [
    Land("Island", LandType.BASIC, [Color.BLUE]),
    Land("Swamp", LandType.BASIC, [Color.BLACK]),
    Land("Mountain", LandType.BASIC, [Color.RED]),
    Land("Forest", LandType.BASIC, [Color.GREEN]),
    Land("Plains", LandType.BASIC, [Color.WHITE]),
]

duals = [
    Land("Underground Sea", LandType.DUAL, [Color.BLUE, Color.BLACK]),
    Land("Volcanic Island", LandType.DUAL, [Color.BLUE, Color.RED]),
    Land("Tropical Island", LandType.DUAL, [Color.BLUE, Color.GREEN]),
    Land("Taiga", LandType.DUAL, [Color.RED, Color.GREEN]),
    Land("Savannah", LandType.DUAL, [Color.GREEN, Color.WHITE]),
    Land("Scrubland", LandType.DUAL, [Color.WHITE, Color.BLACK]),
    Land("Bayou", LandType.DUAL, [Color.BLACK, Color.GREEN]),
    Land("Plateau", LandType.DUAL, [Color.WHITE, Color.RED]),
    Land("Badlands", LandType.DUAL, [Color.BLACK, Color.RED]),
    Land("Tundra", LandType.DUAL, [Color.WHITE, Color.BLUE]),
]

surviels = [
    Land(
        "Commercial District", LandType.SURVEIL, [Color.RED, Color.GREEN], tapped=True
    ),
    Land("Elegant Parlor", LandType.SURVEIL, [Color.RED, Color.WHITE], tapped=True),
    Land("Hedge Maze", LandType.SURVEIL, [Color.GREEN, Color.BLUE], tapped=True),
    Land("Lush Portico", LandType.SURVEIL, [Color.GREEN, Color.WHITE], tapped=True),
    Land(
        "Meticulous Archive", LandType.SURVEIL, [Color.BLUE, Color.WHITE], tapped=True
    ),
    Land("Raucous Theater", LandType.SURVEIL, [Color.RED, Color.BLACK], tapped=True),
    Land(
        "Shadowy Backstreet", LandType.SURVEIL, [Color.BLACK, Color.WHITE], tapped=True
    ),
    Land("Thundering Falls", LandType.SURVEIL, [Color.BLUE, Color.RED], tapped=True),
    Land("Undercity Sewers", LandType.SURVEIL, [Color.BLACK, Color.BLUE], tapped=True),
    Land(
        "Underground Mortuary",
        LandType.SURVEIL,
        [Color.BLACK, Color.GREEN],
        tapped=True,
    ),
]

triomes = [
    Land(
        "Ketria Triome",
        LandType.TRIOME,
        [Color.BLUE, Color.GREEN, Color.RED],
        tapped=True,
    ),
    Land(
        "Savai Triome",
        LandType.TRIOME,
        [Color.BLACK, Color.GREEN, Color.RED],
        tapped=True,
    ),
    Land(
        "Raugrin Triome",
        LandType.TRIOME,
        [Color.WHITE, Color.BLUE, Color.RED],
        tapped=True,
    ),
    Land(
        "Indatha Triome",
        LandType.TRIOME,
        [Color.WHITE, Color.BLACK, Color.GREEN],
        tapped=True,
    ),
    Land(
        "Zagoth Triome",
        LandType.TRIOME,
        [Color.BLUE, Color.BLACK, Color.RED],
        tapped=True,
    ),
    Land(
        "Jetmir's Garden",
        LandType.TRIOME,
        [Color.WHITE, Color.GREEN, Color.RED],
        tapped=True,
    ),
    Land(
        "Raffine's Tower",
        LandType.TRIOME,
        [Color.BLACK, Color.BLUE, Color.WHITE],
        tapped=True,
    ),
    Land(
        "Spara's Headquarters",
        LandType.TRIOME,
        [Color.WHITE, Color.BLUE, Color.GREEN],
        tapped=True,
    ),
    Land(
        "Xander's Lounge",
        LandType.TRIOME,
        [Color.BLUE, Color.BLACK, Color.RED],
        tapped=True,
    ),
    Land(
        "Ziatora's Proving Ground",
        LandType.TRIOME,
        [Color.GREEN, Color.BLACK, Color.RED],
        tapped=True,
    ),
]


manabase = Problem(RecursiveBacktrackingSolver())
manabase.addVariables([*basics, *duals, *surviels, *triomes, *fetchlands], [0, 1,2,3,4])


def parse_args():
    parser = argparse.ArgumentParser(allow_abbrev=True)
    parser.add_argument("--max-copies", type=int, default=4, help="Max copies of any land")
    parser.add_argument("--basic", type=int, default=0, help="Number of basic lands")
    parser.add_argument("--dual", type=int, default=0, help="Number of dual lands")
    parser.add_argument(
        "--surveil", type=int, default=0, help="Number of surveil lands"
    )
    parser.add_argument("--triome", type=int, default=0, help="Number of triomes")
    parser.add_argument(
        "--fetches",
        "--fetchlands",
        type=int,
        required=True,
        help="Number of fetch lands",
    )

    parser.add_argument("-u", type=int, default=0, help="Number of blue lands")
    parser.add_argument("-b", type=int, default=0, help="Number of black lands")
    parser.add_argument("-r", type=int, default=0, help="Number of red lands")
    parser.add_argument("-g", type=int, default=0, help="Number of green lands")
    parser.add_argument("-w", type=int, default=0, help="Number of white lands")

    parser.add_argument(
        "-uu", type=int, default=0, help="Min number of untapped blue lands"
    )
    parser.add_argument(
        "-ub", type=int, default=0, help="Min number of untapped black lands"
    )
    parser.add_argument(
        "-ur", type=int, default=0, help="Min number of untapped red lands"
    )
    parser.add_argument(
        "-ug", type=int, default=0, help="Min number of untapped green lands"
    )
    parser.add_argument(
        "-uw", type=int, default=0, help="Min number of untapped white lands"
    )

    parser.add_argument(
        "-tu", type=int, default=0, help="Min number of tapped blue lands"
    )
    parser.add_argument(
        "-tb", type=int, default=0, help="Min number of tapped black lands"
    )
    parser.add_argument(
        "-tr", type=int, default=0, help="Min number of tapped red lands"
    )
    parser.add_argument(
        "-tg", type=int, default=0, help="Min number of tapped green lands"
    )
    parser.add_argument(
        "-tw", type=int, default=0, help="Min number of tapped white lands"
    )

    for land in duals + surviels + triomes + basics:
        parser.add_argument(
            f"--{land.name.lower().replace(' ', '_')}",
            type=int,
            default=None,
            help=f"Max number of {land.name} (default 4)",
        )

    return parser.parse_args()


def filter_solution(solution):
    ret = {}
    for land, count in solution.items():
        if count != 0:
            ret[land.name] = count
    return ret


def evalFetchlands(solution):
    ret = {}
    for fetch in fetchlands:
        for land, count in solution.items():
            if len(fetch.colors.intersection(land.colors)) > 0:
                if fetch not in ret:
                    ret[fetch] = 0
                ret[fetch] += count

    return ret


def score_solution(solution, fetch_count: int):
    ret = {}
    done = False
    min_count = 0
    for fetch, count in sorted(solution.items(), key=lambda i: i[1], reverse=True):
        if done and min_count > count:
            break
        fetch_count -= 4
        ret[fetch] = count
        if fetch_count <= 0:
            min_count = count
            done = True
    return ret


def solve_manabase():
    args = parse_args()
    fetchables = args.basic + args.dual + args.surveil + args.triome

    manabase.addConstraint(ExactSumConstraint(args.basic), basics)
    manabase.addConstraint(ExactSumConstraint(args.dual), duals)
    manabase.addConstraint(ExactSumConstraint(args.surveil), surviels)
    manabase.addConstraint(ExactSumConstraint(args.triome), triomes)

    manabase.addConstraint(
        ExactSumConstraint(args.u),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.BLUE in land.colors
        ],
    )
    manabase.addConstraint(
        ExactSumConstraint(args.b),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.BLACK in land.colors
        ],
    )
    manabase.addConstraint(
        ExactSumConstraint(args.r),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.RED in land.colors
        ],
    )
    manabase.addConstraint(
        ExactSumConstraint(args.g),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.GREEN in land.colors
        ],
    )
    manabase.addConstraint(
        ExactSumConstraint(args.w),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.WHITE in land.colors
        ],
    )

    manabase.addConstraint(
        MinSumConstraint(args.uu),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.BLUE in land.colors and not land.tapped
        ],
    )
    manabase.addConstraint(
        MinSumConstraint(args.ub),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.BLACK in land.colors and not land.tapped
        ],
    )
    manabase.addConstraint(
        MinSumConstraint(args.ur),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.RED in land.colors and not land.tapped
        ],
    )
    manabase.addConstraint(
        MinSumConstraint(args.ug),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.GREEN in land.colors and not land.tapped
        ],
    )
    manabase.addConstraint(
        MinSumConstraint(args.uw),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.WHITE in land.colors and not land.tapped
        ],
    )

    manabase.addConstraint(
        MinSumConstraint(args.tu),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.BLUE in land.colors and land.tapped
        ],
    )
    manabase.addConstraint(
        MinSumConstraint(args.tb),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.BLACK in land.colors and land.tapped
        ],
    )
    manabase.addConstraint(
        MinSumConstraint(args.tr),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.RED in land.colors and land.tapped
        ],
    )
    manabase.addConstraint(
        MinSumConstraint(args.tg),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.GREEN in land.colors and land.tapped
        ],
    )
    manabase.addConstraint(
        MinSumConstraint(args.tw),
        [
            land
            for land in fetchlands + duals + surviels + triomes + basics
            if Color.WHITE in land.colors and land.tapped
        ],
    )

    for land in duals + surviels + triomes + basics:
        val = getattr(args, land.name.lower().replace(" ", "_"))
        manabase.addConstraint(
            MaxSumConstraint(val if val is not None else args.max_copies), [land]
        )

    if args.tw + args.uw > args.w:
        print("White sources do not add up correctly!")
        return -1
    if args.tu + args.uu > args.u:
        print("Blue sources do not add up correctly!")
        return -1
    if args.tb + args.ub > args.b:
        print("Black sources do not add up correctly!")
        return -1
    if args.tr + args.ur > args.r:
        print("Red sources do not add up correctly!")
        return -1
    if args.tg + args.ug > args.g:
        print("Green sources do not add up correctly!")
        return -1
    if (
        args.w + args.u + args.b + args.r + args.g
        != 2 * (args.dual + args.surveil) + args.basic
    ):
        print("Mana sources must add up to 2 * dual lands + the number of basics")
        print(
            "Provided sources sum: "
            + str(args.w + args.u + args.b + args.r + args.g)
        )
        print("Requested pips: " + str(2 * (args.dual + args.surveil) + args.basic))
        return -1

    solutions = manabase.getSolutions()
    if len(solutions) == 0:
        print("No solutions found")
        return 0
    evaled = []
    for s in solutions:
        eval_fetches = score_solution(evalFetchlands(s), args.fetches)
        max_score = len(eval_fetches) * fetchables
        evaled.append((s, eval_fetches, sum(eval_fetches.values())/max_score))

    for e in sorted(evaled, key=lambda i: i[2]):
        s_str = [f"{str(k)}: {v}" for k, v in sorted(e[0].items()) if v > 0]
        print(f"Score: {e[2]:.2%}")
        print(", ".join(s_str))
        for land, count in sorted(e[1].items(), key=lambda i: i[1], reverse=True):
            print(f"\t{land}: {count} fetchable sources")

        print()

if __name__ == "__main__":
    solve_manabase()
