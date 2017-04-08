# SUN

"""
0000 0010 0000 = 0x020
0100 0010 0010 = 0x422
0010 0000 0100 = 0x204
0000 1111 0000 = 0x0F0
0001 1111 1000 = 0x1F8
1101 1111 1000 = 0xDF8
0001 1111 1011 = 0x1FB
0001 1111 1000 = 0x1F8
0000 1111 0000 = 0x0F0
0010 0000 0100 = 0x204
0100 0100 0010 = 0x442
0000 0100 0000 = 0x040
"""

"""
[ ] airplane
[ ] alarm_clock
[ ] anger
[X] angry
[ ] apple
[ ] aquarius
[ ] aries
[ ] arrow_heading_down
[ ] arrow_heading_up
[ ] arrow_lower_left
[ ] arrow_lower_right
[ ] arrow_up_down
[ ] arrow_upper_left
[ ] arrow_upper_right
[ ] art
[ ] athletic_shoe
[ ] atm
[ ] baby_chick
[ ] banana
[ ] bangbang
[ ] bank
[ ] baseball
[ ] basketball
[ ] beer
[ ] bell
[ ] bike
[ ] birthday
[ ] black_nib
[ ] blue_car
[ ] bomb
[ ] book
[ ] boom
[ ] bread
[ ] broken_heart
[ ] bulb
[ ] bullettrain_side
[ ] bus
[ ] bust_in_silhouette
[ ] cake
[ ] calling
[ ] camera
[ ] cancer
[ ] capricorn
[ ] carousel_horse
[X] cat
[ ] cd
[ ] checkered_flag
[ ] cherries
[ ] cherry_blossom
[ ] christmas_tree
[ ] circus_tent
[ ] cl
[ ] clapper
[X] closed_umbrella
[X] cloud
[ ] clubs
[ ] cocktail
[ ] coffee
[ ] computer
[ ] confounded
[ ] convenience_store
[ ] copyright
[ ] crescent_moon
[ ] crown
[ ] cry
[X] curly_loop
[ ] cyclone
[ ] dash
[ ] diamond_shape_with_a_dot_inside
[ ] diamonds
[ ] disappointed
[ ] dizzy_face
[X] dog
[ ] door
[ ] droplet
[ ] ear
[ ] eight
[ ] end
[ ] envelope
[ ] envelope_with_arrow
[ ] exclamation
[ ] eyeglasses
[ ] eyes
[ ] fax
[ ] first_quarter_moon
[ ] fish
[ ] fist
[ ] five
[ ] foggy
[ ] footprints
[ ] fork_and_knife
[ ] four
[ ] four_leaf_clover
[ ] free
[ ] fuelpump
[ ] full_moon
[ ] gemini
[ ] gift
[ ] golf
[X] grin
[ ] hamburger
[ ] handbag
[ ] hash
[ ] headphones
[ ] heart
[ ] heart_eyes
[ ] heartbeat
[ ] hearts
[ ] high_heel
[ ] horse
[ ] hospital
[ ] hotel
[ ] hotsprings
[ ] hourglass_flowing_sand
[ ] house
[ ] id
[ ] interrobang
[ ] iphone
[ ] jeans
[ ] key
[ ] kiss
[X] laughing
[ ] left_right_arrow
[ ] leftwards_arrow_with_hook
[ ] leo
[ ] libra
[ ] lipstick
[ ] love_letter
[ ] m
[ ] mag
[ ] maple_leaf
[ ] microphone
[ ] moneybag
[ ] mount_fuji
[ ] movie_camera
[ ] musical_note
[ ] new
[ ] new_moon
[ ] ng
[ ] night_with_stars
[ ] nine
[ ] no_smoking
[ ] notes
[ ] ocean
[ ] office
[ ] ok
[ ] on
[ ] one
[ ] pager
[ ] paperclip
[ ] parking
[ ] pencil
[ ] pencil2
[ ] penguin
[X] pensive
[X] persevere
[ ] pig
[ ] pisces
[ ] post_office
[ ] pouch
[ ] punch
[ ] purse
[ ] rage
[ ] railway_car
[ ] raised_hand
[ ] ramen
[ ] recycle
[ ] red_car
[ ] registered
[ ] relieved
[ ] restroom
[ ] ribbon
[ ] rice_ball
[ ] ring
[ ] runner
[ ] running_shirt_with_sash
[ ] sagittarius
[ ] sailboat
[ ] sake
[ ] school
[ ] scissors
[ ] scorpius
[ ] scream
[ ] seat
[ ] secret
[ ] seedling
[ ] seven
[ ] ship
[ ] shirt
[ ] six
[ ] ski
[ ] smiley
[ ] smirk
[ ] smoking
[ ] snail
[ ] snowboarder
[X] snowman
[ ] sob
[ ] soccer
[ ] soon
[ ] spades
[ ] sparkles
[ ] stuck_out_tongue_winking_eye
[X] sunny
[ ] sweat
[ ] sweat_drops
[ ] sweat_smile
[ ] taurus
[ ] tea
[ ] telephone
[ ] tennis
[ ] three
[ ] thumbsup
[ ] ticket
[ ] tm
[ ] tophat
[ ] traffic_light
[ ] triangular_flag_on_post
[ ] tulip
[ ] tv
[ ] two
[ ] two_hearts
[ ] u5408
[ ] u6e80
[ ] u7981
[ ] u7a7a
[X] umbrella
[ ] unamused
[ ] v
[ ] video_game
[ ] virgo
[ ] warning
[ ] watch
[ ] wavy_dash
[ ] waxing_gibbous_moon
[ ] wheelchair
[ ] wine_glass
[ ] wink
[ ] wrench
[ ] yen
[ ] yum
[ ] zap
[ ] zero
[ ] zzz
"""

sunny = [0x020, 0x422, 0x204, 0x0F0,
         0x1F8, 0xDF8, 0x1FB, 0x1F8,
         0x0F0, 0x204, 0x442, 0x040]

cloud = [0x000, 0x000, 0x000, 0x018,
         0x1A4, 0x242, 0x402, 0x402,
         0x244, 0x1B8, 0x000, 0x000]

umbrella = [0x040, 0x0E0, 0x3F8, 0x7FC,
            0x7FC, 0xFFE, 0xFFE, 0x952,
            0x040, 0x040, 0x240, 0x180]

snowman = [0x0E0, 0x110, 0x208, 0x2A8,
           0x208, 0x110, 0x208, 0x404,
           0x404, 0x404, 0x208, 0x1F0]

lightning = [0x008, 0x018, 0x030, 0x070,
             0x0E0, 0x1FC, 0x3F8, 0x070,
             0x0E0, 0x0C0, 0x180, 0x100]

rain = [0xC63, 0x000, 0x000, 0x30C,
        0x000, 0x000, 0xC63, 0x000,
        0x000, 0x30C, 0x000, 0xC63]

dog = [0x402, 0x606, 0x50A, 0x4F2,
       0x402, 0x000, 0x090, 0x000,
       0x000, 0x060, 0x060, 0x000]

cat = [0x801, 0xC03, 0xAF5, 0x801,
       0x000, 0x108, 0x000, 0xF0F,
       0x000, 0x264, 0x198, 0x000]

sailboat = [0x040, 0x040, 0x0D0, 0x150,
            0x158, 0x258, 0x25C, 0x7DE,
            0x000, 0x3FC, 0x1F8, 0x000]

tree = [0x040, 0x1F0, 0x0E0, 0x1F0,
        0x378, 0x1F0, 0x3D8, 0xFFE,
        0x040, 0x1F0, 0x110, 0x0E0]

grin = [0x000, 0x000, 0x108, 0x294,
        0x000, 0x000, 0x1F8, 0x108,
        0x1F8, 0x000, 0x000, 0x000]

angry = [0x000, 0x000, 0x204, 0x108,
         0x090, 0x000, 0x000, 0x060,
         0x090, 0x108, 0x000, 0x000]

persevere = [0x000, 0x000, 0x110, 0x208,
             0x404, 0x000, 0x000, 0x1F0,
             0x208, 0x000, 0x000, 0x000]

pensive = [0x000, 0x000, 0x090, 0x108,
           0x204, 0x000, 0x000, 0x168,
           0x294, 0x000, 0x000, 0x000]

laughing = [0x000, 0x000, 0x294, 0x108,
            0x294, 0x000, 0x060, 0x090,
            0x090, 0x060, 0x000, 0x000]

BMP = {}
BMP["sunny"] = [0x020, 0x422, 0x204, 0x0F0,
                0x1F8, 0xDF8, 0x1FB, 0x1F8,
                0x0F0, 0x204, 0x442, 0x040]

BMP["cloud"] = [0x000, 0x000, 0x000, 0x018,
                0x1A4, 0x242, 0x402, 0x402,
                0x244, 0x1B8, 0x000, 0x000]

BMP["lightning"] = [0x008, 0x018, 0x030, 0x070,
                    0x0E0, 0x1FC, 0x3F8, 0x070,
                    0x0E0, 0x0C0, 0x180, 0x100]

BMP["house"] = [0x060, 0x0F0, 0x1F8, 0x3FC,
                0x7FE, 0xFFF, 0xFFF, 0x264,
                0x264, 0x3FC, 0x3FC, 0x3FC]

BMP["clock"] = [0x0F0, 0x30C, 0x402, 0x406,
                0x909, 0x891, 0x861, 0x801,
                0x402, 0x402, 0x30C, 0x0F0]

BMP["end"] = [0x180, 0x3FC, 0x7FC, 0x7FC,
              0x3FC, 0x180, 0x000, 0xEE2,
              0xAA2, 0xEAE, 0x8AA, 0xEAE]

BMP["bulb"] = [0x040, 0x444, 0x208, 0x0E0,
               0x110, 0xD16, 0x110, 0x0E0,
               0x000, 0x0E0, 0x0E0, 0x0E0]

BMP["train"] = [0x1F8, 0x30C, 0x3FC, 0x204,
                0x204, 0x3FC, 0x3FC, 0x36C,
                0x3FC, 0x090, 0x108, 0x204]

BMP["exclamation"] = [0x070, 0x070, 0x070, 0x060,
                      0x060, 0x060, 0x040, 0x040,
                      0x040, 0x000, 0x0C0, 0x0C0]

BMP["curly_loop"] = [0x1F0, 0x60C, 0x802, 0x802,
                     0x0F1, 0x109, 0x269, 0x289,
                     0x292, 0x262, 0x10C, 0x0F0]

BMP["closed_umbrella"] = [0x0C0, 0x120, 0x020, 0x020,
                          0x070, 0x070, 0x070, 0x070,
                          0x070, 0x070, 0x020, 0x020]

from PIL import Image

im = Image.new("1", (12, 12))
pix = im.load()

for x in range(12):
  for y in range(12):
    row = BMP["curly_loop"][y]
    cell = row & (1 << (12 - x - 1))
    pix[x, y] = cell

im.save("curly_loop.bmp")
