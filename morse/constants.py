from uuid import UUID

BOTS = {
    "dash": "EB:C9:96:2D:EA:48",
    "dot": "C0:F0:84:3C:51:FA",
}

HANDLES = {
    "command": 0x13,
}
CHARACTERISTICS = {
    "dash_sensor": UUID("af230006-879d-6186-1f49-deca0e85d9c1"),
    "universal_sensor": UUID("af230003-879d-6186-1f49-deca0e85d9c1"),
}
COMMANDS = {
    "neck_color":0x03,
    "eye_brightness":0x08,
    "eye":0x09,
    "left_ear_color":0x0b,
    "right_ear_color":0x0c,
    "head_color":0x0d,
    "head_pitch":0x07,
    "head_yaw":0x06,
    "say":0x18,
    "drive":0x02,
    "move":0x23,
    "reset":0xc8, 
}

NOISES={
    k:v.decode("hex")
    for (k,v) in {
        "elephant":   "53595354454c455048414e545f300e460000",  # SYSTELEPHANT_0.F
        "tiresqueal": "535953545449524553515545414c0e460000",  # SYSTTIRESQUEAL.F
        "hi":         "53595354444153485f48495f564f0b00c900",  # SYSTDASH_HI_VO
        "bragging":   "535953544252414747494e4731410b232300",  # SYSTBRAGGING1A##
        "ohno":       "5359535456375f4f484e4f5f30390b000000",  # SYSTV7_OHNO_09
        "ayayay":     "53595354434f4e46555345445f310b000000",  # SYSTCONFUSED_1
        "confused2":  "53595354434f4e46555345445f320b000000",  # SYSTCONFUSED_2
        "confused3":  "53595354434f4e46555345445f330b000000",  # SYSTCONFUSED_3
        "confused5":  "53595354434f4e46555345445f350b000000",  # SYSTCONFUSED_5
        "confused8":  "53595354434f4e46555345445f380b000000",  # SYSTCONFUSED_8
        "brrp":       "53595354434f4e46555345445f360b000000",  # SYSTCONFUSED_6
        "charge":     "535953544348415247455f3033000b000000",  # SYSTCHARGE_03
    }.items()
}

