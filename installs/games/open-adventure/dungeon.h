/* Generated from adventure.yaml - do not hand-hack! */

#ifndef DUNGEON_H
#define DUNGEON_H

#include <stdio.h>
#include <stdbool.h>

#define SILENT	-1	/* no sound */

/* Symbols for cond bits */
#define COND_LIT	0	/* Light */
#define COND_OILY	1	/* If bit 2 is on: on for oil, off for water */
#define COND_FLUID	2	/* Liquid asset, see bit 1 */
#define COND_NOARRR	3	/* Pirate doesn't go here unless following */
#define COND_NOBACK	4	/* Cannot use "back" to move away */
#define COND_ABOVE	5
#define COND_DEEP	6	/* Deep - e.g where dwarves are active */
#define COND_FOREST	7	/* In the forest */
#define COND_FORCED	8	/* Only one way in or out of here */
/* Bits past 10 indicate areas of interest to "hint" routines */
#define COND_HBASE	10	/* Base for location hint bits */
#define COND_HCAVE	11	/* Trying to get into cave */
#define COND_HBIRD	12	/* Trying to catch bird */
#define COND_HSNAKE	13	/* Trying to deal with snake */
#define COND_HMAZE	14	/* Lost in maze */
#define COND_HDARK	15	/* Pondering dark room */
#define COND_HWITT	16	/* At Witt's End */
#define COND_HCLIFF	17	/* Cliff with urn */
#define COND_HWOODS	18	/* Lost in forest */
#define COND_HOGRE	19	/* Trying to deal with ogre */
#define COND_HJADE	20	/* Found all treasures except jade */

typedef struct {
  const char** strs;
  const int n;
} string_group_t;

typedef struct {
  const string_group_t words;
  const char* inventory;
  int plac, fixd;
  bool is_treasure;
  const char** descriptions;
  const char** sounds;
  const char** texts;
  const char** changes;
} object_t;

typedef struct {
  const char* small;
  const char* big;
} descriptions_t;

typedef struct {
  descriptions_t description;
  const long sound;
  const bool loud;
} location_t;

typedef struct {
  const char* query;
  const char* yes_response;
} obituary_t;

typedef struct {
  const int threshold;
  const int point_loss;
  const char* message;
} turn_threshold_t;

typedef struct {
  const int threshold;
  const char* message;
} class_t;

typedef struct {
  const int number;
  const int turns;
  const int penalty;
  const char* question;
  const char* hint;
} hint_t;

typedef struct {
  const string_group_t words;
} motion_t;

typedef struct {
  const string_group_t words;
  const char* message;
  const bool noaction;
} action_t;

enum condtype_t {cond_goto, cond_pct, cond_carry, cond_with, cond_not};
enum desttype_t {dest_goto, dest_special, dest_speak};

typedef struct {
  const long motion;
  const long condtype;
  const long condarg1;
  const long condarg2;
  const enum desttype_t desttype;
  const long destval;
  const bool nodwarves;
  const bool stop;
} travelop_t;

/* Abstract out the encoding of words in the travel array.  Gives us
 * some hope of getting to a less cryptic representation than we
 * inherited from FORTRAN, someday. To understand these, read the
 * encoding description for travel.
 */
#define T_TERMINATE(entry)	((entry).motion == 1)

extern const location_t locations[];
extern const object_t objects[];
extern const char* arbitrary_messages[];
extern const class_t classes[];
extern const turn_threshold_t turn_thresholds[];
extern const obituary_t obituaries[];
extern const hint_t hints[];
extern long conditions[];
extern const motion_t motions[];
extern const action_t actions[];
extern const travelop_t travel[];
extern const long tkey[];
extern const char *ignore;

#define NLOCATIONS	184
#define NOBJECTS	69
#define NHINTS		10
#define NCLASSES	10
#define NDEATHS		3
#define NTHRESHOLDS	4
#define NMOTIONS    76
#define NACTIONS  	58
#define NTRAVEL		878
#define NKEYS		185

#define BIRD_ENDSTATE 5

enum arbitrary_messages_refs {
    NO_MESSAGE,
    CAVE_NEARBY,
    DWARF_BLOCK,
    DWARF_RAN,
    DWARF_PACK,
    DWARF_SINGLE,
    KNIFE_THROWN,
    SAYS_PLUGH,
    GETS_YOU,
    MISSES_YOU,
    UNSURE_FACING,
    NO_INOUT_HERE,
    CANT_APPLY,
    AM_GAME,
    NO_MORE_DETAIL,
    PITCH_DARK,
    W_IS_WEST,
    REALLY_QUIT,
    PIT_FALL,
    ALREADY_CARRYING,
    YOU_JOKING,
    BIRD_EVADES,
    CANNOT_CARRY,
    NOTHING_LOCKED,
    ARENT_CARRYING,
    BIRD_ATTACKS,
    NO_KEYS,
    NO_LOCK,
    NOT_LOCKABLE,
    ALREADY_LOCKED,
    ALREADY_UNLOCKED,
    BEAR_BLOCKS,
    NOTHING_HAPPENS,
    WHERE_QUERY,
    NO_TARGET,
    BIRD_DEAD,
    SNAKE_WARNING,
    KILLED_DWARF,
    DWARF_DODGES,
    BARE_HANDS_QUERY,
    BAD_DIRECTION,
    TWO_WORDS,
    OK_MAN,
    CANNOT_UNLOCK,
    FUTILE_CRAWL,
    FOLLOW_STREAM,
    NEED_DETAIL,
    NEARBY,
    OGRE_SNARL,
    HUH_MAN,
    WELCOME_YOU,
    REQUIRES_DYNAMITE,
    FEET_WET,
    LOST_APPETITE,
    THANKS_DELICIOUS,
    PECULIAR_NOTHING,
    GROUND_WET,
    CANT_POUR,
    WHICH_WAY,
    FORGOT_PATH,
    CARRY_LIMIT,
    GRATE_NOWAY,
    YOU_HAVEIT,
    DONT_FIT,
    CROSS_BRIDGE,
    NO_CROSS,
    NO_CARRY,
    NOW_HOLDING,
    BIRD_PINING,
    BIRD_DEVOURED,
    NOTHING_EDIBLE,
    REALLY_MAD,
    NO_CONTAINER,
    BOTTLE_FULL,
    NO_LIQUID,
    RIDICULOUS_ATTEMPT,
    RUSTY_DOOR,
    SHAKING_LEAVES,
    DEEP_ROOTS,
    KNIVES_VANISH,
    MUST_DROP,
    CLAM_BLOCKER,
    OYSTER_BLOCKER,
    DROP_OYSTER,
    CLAM_OPENER,
    OYSTER_OPENER,
    PEARL_FALLS,
    OYSTER_OPENS,
    WAY_BLOCKED,
    PIRATE_RUSTLES,
    PIRATE_POUNCES,
    CAVE_CLOSING,
    EXIT_CLOSED,
    DEATH_CLOSING,
    CAVE_CLOSED,
    VICTORY_MESSAGE,
    DEFEAT_MESSAGE,
    SPLATTER_MESSAGE,
    DWARVES_AWAKEN,
    UNHAPPY_BIRD,
    NEEDED_NEARBY,
    NOT_CONNECTED,
    TAME_BEAR,
    WITHOUT_SUSPENDS,
    FILL_INVALID,
    SHATTER_VASE,
    BEYOND_POWER,
    NOT_KNOWHOW,
    TOO_FAR,
    DWARF_SMOKE,
    SHELL_IMPERVIOUS,
    START_OVER,
    WELL_POINTLESS,
    DRAGON_SCALES,
    NASTY_DRAGON,
    BIRD_BURNT,
    BRIEF_CONFIRM,
    ROCKY_TROLL,
    TROLL_RETURNS,
    TROLL_SATISFIED,
    TROLL_BLOCKS,
    BRIDGE_GONE,
    BEAR_HANDS,
    BEAR_CONFUSED,
    ALREADY_DEAD,
    BEAR_CHAINED,
    STILL_LOCKED,
    CHAIN_UNLOCKED,
    CHAIN_LOCKED,
    NO_LOCKSITE,
    WANT_HINT,
    TROLL_VICES,
    LAMP_DIM,
    LAMP_OUT,
    PLEASE_ANSWER,
    PIRATE_SPOTTED,
    GET_BATTERIES,
    REPLACE_BATTERIES,
    MISSING_BATTERIES,
    REMOVE_MESSAGE,
    CLUE_QUERY,
    WAYOUT_CLUE,
    DONT_UNDERSTAND,
    HAND_PASSTHROUGH,
    PROD_DWARF,
    THIS_ACCEPTABLE,
    OGRE_FULL,
    OGRE_DODGE,
    OGRE_PANIC1,
    OGRE_PANIC2,
    FREE_FLY,
    CAGE_FLY,
    NECKLACE_FLY,
    WATER_URN,
    OIL_URN,
    FULL_URN,
    URN_NOPOUR,
    URN_NOBUDGE,
    URN_GENIES,
    DOUGHNUT_HOLES,
    GEM_FITS,
    RUG_RISES,
    RUG_WIGGLES,
    RUG_SETTLES,
    RUG_HOVERS,
    RUG_NOTHING1,
    RUG_NOTHING2,
    FLAP_ARMS,
    RUG_GOES,
    RUG_RETURNS,
    ALL_SILENT,
    STREAM_GURGLES,
    WIND_WHISTLES,
    STREAM_SPLASHES,
    NO_MEANING,
    MURMURING_SNORING,
    SNAKES_HISSING,
    DULL_RUMBLING,
    LOUD_ROAR,
    TOTAL_ROAR,
    BIRD_CRAP,
    FEW_DROPS,
    NOT_BRIGHT,
    TOOK_LONG,
    UPSTREAM_DOWNSTREAM,
    FOREST_QUERY,
    WATERS_CRASHING,
    THROWN_KNIVES,
    MULTIPLE_HITS,
    ONE_HIT,
    NONE_HIT,
    DONT_KNOW,
    WHAT_DO,
    NO_SEE,
    DO_WHAT,
    OKEY_DOKEY,
    GARNERED_POINTS,
    SUSPEND_WARNING,
    HINT_COST,
    TOTAL_SCORE,
    NEXT_HIGHER,
    NO_HIGHER,
    OFF_SCALE,
    RESUME_HELP,
    RESUME_ABANDON,
    VERSION_SKEW,
    TWIST_TURN,
    GO_UNNEEDED,
    NUMERIC_REQUIRED,
};

enum locations_refs {
    LOC_NOWHERE,
    LOC_START,
    LOC_HILL,
    LOC_BUILDING,
    LOC_VALLEY,
    LOC_ROADEND,
    LOC_CLIFF,
    LOC_SLIT,
    LOC_GRATE,
    LOC_BELOWGRATE,
    LOC_COBBLE,
    LOC_DEBRIS,
    LOC_AWKWARD,
    LOC_BIRD,
    LOC_PITTOP,
    LOC_MISTHALL,
    LOC_CRACK,
    LOC_EASTBANK,
    LOC_NUGGET,
    LOC_KINGHALL,
    LOC_NECKBROKE,
    LOC_NOMAKE,
    LOC_DOME,
    LOC_WESTEND,
    LOC_EASTPIT,
    LOC_WESTPIT,
    LOC_CLIMBSTALK,
    LOC_WESTBANK,
    LOC_FLOORHOLE,
    LOC_SOUTHSIDE,
    LOC_WESTSIDE,
    LOC_BUILDING1,
    LOC_SNAKEBLOCK,
    LOC_Y2,
    LOC_JUMBLE,
    LOC_WINDOW1,
    LOC_BROKEN,
    LOC_SMALLPITBRINK,
    LOC_SMALLPIT,
    LOC_DUSTY,
    LOC_PARALLEL1,
    LOC_MISTWEST,
    LOC_ALIKE1,
    LOC_ALIKE2,
    LOC_ALIKE3,
    LOC_ALIKE4,
    LOC_DEADEND1,
    LOC_DEADEND2,
    LOC_DEADEND3,
    LOC_ALIKE5,
    LOC_ALIKE6,
    LOC_ALIKE7,
    LOC_ALIKE8,
    LOC_ALIKE9,
    LOC_DEADEND4,
    LOC_ALIKE10,
    LOC_DEADEND5,
    LOC_PITBRINK,
    LOC_DEADEND6,
    LOC_PARALLEL2,
    LOC_LONGEAST,
    LOC_LONGWEST,
    LOC_CROSSOVER,
    LOC_DEADEND7,
    LOC_COMPLEX,
    LOC_BEDQUILT,
    LOC_SWISSCHEESE,
    LOC_EASTEND,
    LOC_SLAB,
    LOC_SECRET1,
    LOC_SECRET2,
    LOC_THREEJUNCTION,
    LOC_LOWROOM,
    LOC_DEADCRAWL,
    LOC_SECRET3,
    LOC_WIDEPLACE,
    LOC_TIGHTPLACE,
    LOC_TALL,
    LOC_BOULDERS1,
    LOC_SEWER,
    LOC_ALIKE11,
    LOC_DEADEND8,
    LOC_DEADEND9,
    LOC_ALIKE12,
    LOC_ALIKE13,
    LOC_DEADEND10,
    LOC_DEADEND11,
    LOC_ALIKE14,
    LOC_NARROW,
    LOC_NOCLIMB,
    LOC_PLANTTOP,
    LOC_INCLINE,
    LOC_GIANTROOM,
    LOC_CAVEIN,
    LOC_IMMENSE,
    LOC_WATERFALL,
    LOC_SOFTROOM,
    LOC_ORIENTAL,
    LOC_MISTY,
    LOC_ALCOVE,
    LOC_PLOVER,
    LOC_DARKROOM,
    LOC_ARCHED,
    LOC_SHELLROOM,
    LOC_SLOPING1,
    LOC_CULDESAC,
    LOC_ANTEROOM,
    LOC_DIFFERENT1,
    LOC_WITTSEND,
    LOC_MIRRORCANYON,
    LOC_WINDOW2,
    LOC_TOPSTALACTITE,
    LOC_DIFFERENT2,
    LOC_RESERVOIR,
    LOC_DEADEND12,
    LOC_NE,
    LOC_SW,
    LOC_SWCHASM,
    LOC_WINDING,
    LOC_SECRET4,
    LOC_SECRET5,
    LOC_SECRET6,
    LOC_NECHASM,
    LOC_CORRIDOR,
    LOC_FORK,
    LOC_WARMWALLS,
    LOC_BREATHTAKING,
    LOC_BOULDERS2,
    LOC_LIMESTONE,
    LOC_BARRENFRONT,
    LOC_BARRENROOM,
    LOC_DIFFERENT3,
    LOC_DIFFERENT4,
    LOC_DIFFERENT5,
    LOC_DIFFERENT6,
    LOC_DIFFERENT7,
    LOC_DIFFERENT8,
    LOC_DIFFERENT9,
    LOC_DIFFERENT10,
    LOC_DIFFERENT11,
    LOC_DEADEND13,
    LOC_ROUGHHEWN,
    LOC_BADDIRECTION,
    LOC_LARGE,
    LOC_STOREROOM,
    LOC_FOREST1,
    LOC_FOREST2,
    LOC_FOREST3,
    LOC_FOREST4,
    LOC_FOREST5,
    LOC_FOREST6,
    LOC_FOREST7,
    LOC_FOREST8,
    LOC_FOREST9,
    LOC_FOREST10,
    LOC_FOREST11,
    LOC_FOREST12,
    LOC_FOREST13,
    LOC_FOREST14,
    LOC_FOREST15,
    LOC_FOREST16,
    LOC_FOREST17,
    LOC_FOREST18,
    LOC_FOREST19,
    LOC_FOREST20,
    LOC_FOREST21,
    LOC_FOREST22,
    LOC_LEDGE,
    LOC_RESBOTTOM,
    LOC_RESNORTH,
    LOC_TREACHEROUS,
    LOC_STEEP,
    LOC_CLIFFBASE,
    LOC_CLIFFACE,
    LOC_FOOTSLIP,
    LOC_CLIFFTOP,
    LOC_CLIFFLEDGE,
    LOC_REACHDEAD,
    LOC_GRUESOME,
    LOC_FOOF1,
    LOC_FOOF2,
    LOC_FOOF3,
    LOC_FOOF4,
    LOC_FOOF5,
    LOC_FOOF6,
};

enum object_refs {
    NO_OBJECT,
    KEYS,
    LAMP,
    GRATE,
    CAGE,
    ROD,
    ROD2,
    STEPS,
    BIRD,
    DOOR,
    PILLOW,
    SNAKE,
    FISSURE,
    OBJ_13,
    CLAM,
    OYSTER,
    MAGAZINE,
    DWARF,
    KNIFE,
    FOOD,
    BOTTLE,
    WATER,
    OIL,
    MIRROR,
    PLANT,
    PLANT2,
    OBJ_26,
    OBJ_27,
    AXE,
    OBJ_29,
    OBJ_30,
    DRAGON,
    CHASM,
    TROLL,
    TROLL2,
    BEAR,
    MESSAG,
    VOLCANO,
    VEND,
    BATTERY,
    OBJ_40,
    OGRE,
    URN,
    CAVITY,
    BLOOD,
    RESER,
    OBJ_46,
    OBJ_47,
    OBJ_48,
    SIGN,
    NUGGET,
    OBJ_51,
    OBJ_52,
    OBJ_53,
    COINS,
    CHEST,
    EGGS,
    TRIDENT,
    VASE,
    EMERALD,
    PYRAMID,
    PEARL,
    RUG,
    OBJ_63,
    CHAIN,
    RUBY,
    JADE,
    AMBER,
    SAPPH,
    OBJ_69,
};

enum motion_refs {
    MOT_0,
    HERE,
    MOT_2,
    ENTER,
    MOT_4,
    MOT_5,
    MOT_6,
    FORWARD,
    BACK,
    MOT_9,
    MOT_10,
    OUTSIDE,
    MOT_12,
    MOT_13,
    STREAM,
    MOT_15,
    MOT_16,
    CRAWL,
    MOT_18,
    INSIDE,
    MOT_20,
    NUL,
    MOT_22,
    MOT_23,
    MOT_24,
    MOT_25,
    MOT_26,
    MOT_27,
    MOT_28,
    UP,
    DOWN,
    MOT_31,
    MOT_32,
    MOT_33,
    MOT_34,
    MOT_35,
    LEFT,
    RIGHT,
    MOT_38,
    MOT_39,
    MOT_40,
    MOT_41,
    MOT_42,
    EAST,
    WEST,
    NORTH,
    SOUTH,
    NE,
    SE,
    SW,
    NW,
    MOT_51,
    MOT_52,
    MOT_53,
    MOT_54,
    MOT_55,
    MOT_56,
    LOOK,
    MOT_58,
    MOT_59,
    MOT_60,
    MOT_61,
    XYZZY,
    DEPRESSION,
    ENTRANCE,
    PLUGH,
    MOT_66,
    CAVE,
    CROSS,
    BEDQUILT,
    PLOVER,
    ORIENTAL,
    CAVERN,
    SHELLROOM,
    RESERVOIR,
    OFFICE,
};

enum action_refs {
    ACT_NULL,
    CARRY,
    DROP,
    SAY,
    UNLOCK,
    NOTHING,
    LOCK,
    LIGHT,
    EXTINGUISH,
    WAVE,
    TAME,
    GO,
    ATTACK,
    POUR,
    EAT,
    DRINK,
    RUB,
    THROW,
    QUIT,
    FIND,
    INVENTORY,
    FEED,
    FILL,
    BLAST,
    SCORE,
    FEE,
    FIE,
    FOE,
    FOO,
    FUM,
    BRIEF,
    READ,
    BREAK,
    WAKE,
    SAVE,
    RESUME,
    FLY,
    LISTEN,
    PART,
    SEED,
    WASTE,
    ACT_UNKNOWN,
    THANKYOU,
    INVALIDMAGIC,
    HELP,
    False,
    TREE,
    DIG,
    LOST,
    MIST,
    FBOMB,
    STOP,
    INFO,
    SWIM,
    WIZARD,
    YES,
    NEWS,
    ACT_VERSION,
};

/* State definitions */

/* States for LAMP */
#define LAMP_DARK	0
#define LAMP_BRIGHT	1

/* States for GRATE */
#define GRATE_CLOSED	0
#define GRATE_OPEN	1

/* States for STEPS */
#define STEPS_DOWN	0
#define STEPS_UP	1

/* States for BIRD */
#define BIRD_UNCAGED	0
#define BIRD_CAGED	1
#define BIRD_FOREST_UNCAGED	2

/* States for DOOR */
#define DOOR_RUSTED	0
#define DOOR_UNRUSTED	1

/* States for SNAKE */
#define SNAKE_BLOCKS	0
#define SNAKE_CHASED	1

/* States for FISSURE */
#define UNBRIDGED	0
#define BRIDGED	1

/* States for BOTTLE */
#define WATER_BOTTLE	0
#define EMPTY_BOTTLE	1
#define OIL_BOTTLE	2

/* States for MIRROR */
#define MIRROR_UNBROKEN	0
#define MIRROR_BROKEN	1

/* States for PLANT */
#define PLANT_THIRSTY	0
#define PLANT_BELLOWING	1
#define PLANT_GROWN	2

/* States for AXE */
#define AXE_HERE	0
#define AXE_LOST	1

/* States for DRAGON */
#define DRAGON_BARS	0
#define DRAGON_DEAD	1
#define DRAGON_BLOODLESS	2

/* States for CHASM */
#define TROLL_BRIDGE	0
#define BRIDGE_WRECKED	1

/* States for TROLL */
#define TROLL_UNPAID	0
#define TROLL_PAIDONCE	1
#define TROLL_GONE	2

/* States for BEAR */
#define UNTAMED_BEAR	0
#define SITTING_BEAR	1
#define CONTENTED_BEAR	2
#define BEAR_DEAD	3

/* States for VEND */
#define VEND_BLOCKS	0
#define VEND_UNBLOCKS	1

/* States for BATTERY */
#define FRESH_BATTERIES	0
#define DEAD_BATTERIES	1

/* States for URN */
#define URN_EMPTY	0
#define URN_DARK	1
#define URN_LIT	2

/* States for CAVITY */
#define CAVITY_FULL	0
#define CAVITY_EMPTY	1

/* States for RESER */
#define WATERS_UNPARTED	0
#define WATERS_PARTED	1

/* States for SIGN */
#define INGAME_SIGN	0
#define ENDGAME_SIGN	1

/* States for EGGS */
#define EGGS_HERE	0
#define EGGS_VANISHED	1
#define EGGS_DONE	2

/* States for VASE */
#define VASE_WHOLE	0
#define VASE_DROPPED	1
#define VASE_BROKEN	2

/* States for RUG */
#define RUG_FLOOR	0
#define RUG_DRAGON	1
#define RUG_HOVER	2

/* States for CHAIN */
#define CHAIN_HEAP	0
#define CHAINING_BEAR	1
#define CHAIN_FIXED	2

/* States for AMBER */
#define AMBER_IN_URN	0
#define AMBER_IN_ROCK	1



#endif /* end DUNGEON_H */