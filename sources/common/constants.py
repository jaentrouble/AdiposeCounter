
# Engine Constants ############################################################
MEMBRANE = (0,0,0)
CELL = (255,255,255)
COUNT = (255,255,0)
LINE_START = (255,0,0)
CURSOR = (255,0,0)

DEFAULT_MP_RATIO = 0.16259
DEFAULT_MP_PIXEL = 63
DEFAULT_MP_MICRO = 50

NEWIMAGE = 0
NEWMASK = 1

MODE_MASK = 10
MODE_IMAGE = 11
MODE_NONE = 12
MODE_SET_MEM = 13
MODE_SET_CELL = 14
MODE_DRAW_MEM = 15
MODE_DRAW_CELL = 16
MODE_FILL_CELL = 17
MODE_FILL_MP_RATIO = 18

SET_MEM = 100
SET_CELL = 101
SET_RATIO = 102

DRAW_OFF = 201
DRAW_MEM = 202
DRAW_CELL = 203
DRAW_CANCEL = 204

FILL_CELL = 301
FILL_MP_RATIO = 302
FILL_LIST = 303
FILL_DELETE = 304
FILL_SAVE = 305
FILL_MICRO = 306

TERMINATE = -1





# Viewer Constants ############################################################
MOUSEDOWN = 401
MOUSEUP = 402
MOUSEPOS = 403
MOUSEDOWN_RIGHT = 404

MOUSEPOS_ON = 501
MOUSEPOS_OFF = 502
BIG_CURSOR_ON = 503
BIG_CURSOR_OFF = 504

MESSAGE_BOX = 601

# Use same numbers as pygame.K_* + 1000
K_Z = 1122
K_ENTER = 1013

# Console Constants ###########################################################
IMAGE_FORMATS = ('.jpg', '.png', '.jpeg', '.tif', '.tiff')