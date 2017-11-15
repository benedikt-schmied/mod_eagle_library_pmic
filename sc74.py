#!/usr/bin/python
import math

##################################################################
# parameters that shall be changes according to what is desired
##################################################################

# pad size
pad_length = '0.500mm'
pad_width = '0.55mm'

# pads per side
pads_per_side = 3 

# Abstand der gegenueberliegenden Pad-Reihen (Mitte der Pads)
pad_row_distance = (1.9 + 0.5)

# Abstand zwischen den mitten der aeusseren Pads einer Seite
pads_side_length = (2*0.95)

# Siehe Eagle-Doku zu 'SMD'
pad_roundness = '0'

# for TQFP specify 4, for SO specify 2
sides = 2 

##################################################################
# please do not change this section
##################################################################

# stub percentage
stub_percentage = 20

#finger weg_
_pad_counter = 1
_wire_counter = 1


##################################################################
# start of function which work on the wires and smd pads
##################################################################

def wire(start, end, width, orientation, name):
    return "Layer 21;\n WIRE %fmm ROUND (%fmm %fmm) (%fmm %fmm);"  % (width, start[0], start[1], end[0], end[1])

def smd(pos, orientation, name):
    return "Layer 1;\n SMD %s %s -%s R%f '%s' (%fmm %fmm);" % (pad_length, pad_width, pad_roundness, orientation, name, pos[0], pos[1])


##################################################################
# parameters that shall be changes according to what is desired
##################################################################

def rad2deg(a):
    return 180.0 * a / math.pi

def pad_name(i):
    return '%d' % i

##################################################################
# parameters that shall be changes according to what is desired
##################################################################
def mk_pad_line(start, end, num):
    global _pad_counter
    res = list()
    
    # calculate the x - length
    x_delta = end[0] - start[0]
    
    # calculate the y - length
    y_delta = end[1] - start[1]

    # according to the calculated delta, we can define the angle
    if x_delta == 0:
        if y_delta < 0:
            angle = 0
        elif y_delta > 0:
            angle = 180
        else:
            print "error x_delta in pad line calculation"
            angle = 0
    elif y_delta == 0:
        if x_delta < 0:
            angle = 90
        elif x_delta > 0:
            angle = 270
        else:
            "error y_delta in pad line calculation"
            angle = 0

    # now, start calculating the x and y values
    for i in range(num):
        x = start[0] + (end[0] - start[0]) * float(i) / float(num -1 )
        y = start[1] + (end[1] - start[1]) * float(i) / float(num -1 )
        res.append(smd((x,y), angle, pad_name(_pad_counter)))
        _pad_counter += 1
    return res

def mk_wire(start, end, num):
    global _wire_counter
    wire = list()
    x_delta = end[0] - start[0]
    y_delta = end[1] - start[1]

    if x_delta == 0:
        if y_delta < 0:
            angle = 0
	elif y_delta > 0:
	    angle = 180
	else:
	    print "error x_delta in wire calculation"
	    angle = 0
    elif y_delta == 0:
	if x_delta < 0:
            angle = 90
	elif x_delta > 0:
	    angle = 270
	else:
	    print "error y_delta in wire calculation"
	    angle = 0    

    for i in range(num):
        x = start[0] + (end[0] - start[0]) * float(i) / float(num -1 )
        y = start[1] + (end[1] - start[1]) * float(i) / float(num -1 )
        wire.append(wire_stub((x,y), angle))
        _wire_counter += 1
    return wire

def test_something():
    print("hello")

def wire_stub(pos, orientation):
    if orientation == 0:
        start = ((pos[0] + 1.2 ), (pos[1]))
        end = ((start[0] + 0.4), (start[1]))
        return wire(start, end, 0.2, orientation, "mark")
    if orientation == 90:
	start = ((pos[0], pos[1] - 1.2))
	end  = ((start[0], start[1] - 0.4))
        return wire(start, end, 0.2, orientation, "mark")
    if orientation == 180:
	start = ((pos[0] - 1.2, pos[1]))
	end = ((start[0] - 0.4, start[1]))
	return wire(start, end, 0.2, orientation, "mark")
    if orientation == 270:
	start = ((pos[0], pos[1] + 1.2))
	end = ((start[0], start[1] + 0.4))
	return wire(start, end, 0.2, orientation, "mark")
    return ""


##################################################################
# parameters that shall be changes according to what is desired
##################################################################
def create_footprint():
    res = []
    wire = []
    command = ""
    if sides == 4:
        left = ((-pad_row_distance / 2.0, pads_side_length / 2.0), (-pad_row_distance / 2.0, -pads_side_length / 2.0))
        bot =  ((-pads_side_length / 2.0, -pad_row_distance / 2.0), (+pads_side_length / 2.0, -pad_row_distance / 2.0))
        right =((pad_row_distance / 2.0, -pads_side_length / 2.0), (pad_row_distance / 2.0, pads_side_length / 2.0))
        top =  ((pads_side_length / 2.0, pad_row_distance / 2.0), (-pads_side_length / 2.0, pad_row_distance / 2.0))
        res.extend(mk_pad_line(left[0], left[1], pads_per_side))
        res.extend(mk_pad_line(bot[0], bot[1], pads_per_side))
        res.extend(mk_pad_line(right[0], right[1], pads_per_side))
        res.extend(mk_pad_line(top[0], top[1], pads_per_side))

        wire.extend(mk_wire(left[0], left[1], pads_per_side))
        wire.extend(mk_wire(bot[0], bot[1], pads_per_side))
        wire.extend(mk_wire(right[0], right[1], pads_per_side))
        wire.extend(mk_wire(top[0], top[1], pads_per_side))

    elif sides == 2:
        left = ((-pad_row_distance / 2.0, pads_side_length / 2.0), (-pad_row_distance / 2.0, -pads_side_length / 2.0))
        right =((pad_row_distance / 2.0, -pads_side_length / 2.0), (pad_row_distance / 2.0, pads_side_length / 2.0))
        res.extend(mk_pad_line(left[0], left[1], pads_per_side))
        res.extend(mk_pad_line(right[0], right[1], pads_per_side))
    return '\n'.join(res) + '\n' + '\n'.join(wire)


def create_something_else():
    print("test")


if __name__ == '__main__':
    print create_footprint()

