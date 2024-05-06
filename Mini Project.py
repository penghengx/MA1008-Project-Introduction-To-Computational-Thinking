#MA1008 Mini Project

#calculate reaction of point load
def reaction_pl(loadType):
    #magnitude input
    while True:         
        try:
            print("Taking downwards as -ve, upwards as +ve,")
            magnitude = float(input("Input magnitude of Load: "))
            break
        except ValueError:
            print("Value Error, please input a valid number.")
    #position input
    while True:         
        try:
            position = float(input("Input position of Load: "))
            if position<0 or position>beam_length:
                print("Position is out of bounds.")
                continue
            else:
                break
        except ValueError:
            print("Value Error, please input a valid number.")
    #add inputs to list    
    global pointloadlist
    pointloadlist.append([magnitude, position])
    #calculation
    dp = A-position
    moment = magnitude*dp
    dB = B-A
    vB = moment/dB
    vA = -magnitude-vB
    #add reactions to list
    global reaction
    reaction[0] += vA
    reaction[1] += vB
    #print inputs to outfile
    print(loadType, magnitude, position, file= outfile, end = "")
    print(file= outfile, end = "\n")

    
#calculate reaction of distributed load    
def reaction_dl(loadType):
    #start magnitude input
    while True:
        try:
            print("Taking downwards as -ve, upwards as +ve,")
            start_magnitude = float(input("Input magnitude of Load at the start: "))
            break
        except ValueError:
            print("Value Error, please input a valid number.")
    #end magnitude input
    while True:
        try:
            print("Taking downwards as -ve, upwards as +ve,")
            end_magnitude = float(input("Input magnitude of Load at the end: "))
            break
        except ValueError:
            print("Value Error, please input a valid number.")
    #start position input
    while True:
        try:
            start_position = float(input("Input position of Load at the start: "))
            if start_position<0 or start_position>beam_length:
                print("Position is out of bounds.")
                continue
            else:
                break
        except ValueError:
            print("Value Error, please input a valid number.")
    #end position input
    while True:
        try:
            end_position = float(input("Input position of Load at the end: "))
            if end_position<0 or end_position>beam_length:
                print("Position is out of bounds.")
                continue
            else:
                break
        except ValueError:
            print("Value Error, please input a valid number.")
    #calculate the resultant magnitude and resultant position of ditributed load
    if start_magnitude == end_magnitude:
        resultant_magnitude = start_magnitude*(end_position - start_position)
        resultant_position = (end_position + start_position)/2
    elif abs(start_magnitude) >= abs(end_magnitude):
        resultant_magnitude = 0.5*start_magnitude*(end_position - start_position)
        resultant_position = start_position + (1/3)*(end_position - start_position)
    elif abs(start_magnitude) <= abs(end_magnitude):
        resultant_magnitude = 0.5*end_magnitude*(end_position - start_position)
        resultant_position = start_position + (2/3)*(end_position - start_position)
    #add inputs to list 
    global distributedloadlist
    distributedloadlist.append([start_magnitude, end_magnitude, start_position, end_position, resultant_magnitude, resultant_position])
    #calculation
    dp = A-resultant_position
    moment = resultant_magnitude*dp
    dB = B-A
    vB = moment/dB
    vA = -resultant_magnitude-vB
    #add reactions to list
    global reaction
    reaction[0] += vA
    reaction[1] += vB
    #print inputs to outfile
    print(loadType, start_magnitude, end_magnitude, start_position, end_position, file= outfile, end = "")
    print(file= outfile, end = "\n")
    

#calculate reaction of bending moment
def reaction_bm(loadType):
    #magnitude input
    while True:         
        try:
            print("Taking ACW as -ve, CW as +ve,")
            magnitude = float(input("Input magnitude of Load: "))
            break
        except ValueError:
            print("Value Error, please input a valid number.")
    #position input
    while True:         
        try:
            position = float(input("Input position of Load: "))
            if position<0 or position>beam_length:
                print("Position is out of bounds.")
                continue
            else:
                break
        except ValueError:
            print("Value Error, please input a valid number.")
    #add inputs to list        
    global bendingmomentlist
    bendingmomentlist.append([magnitude, position])
    #calculation
    dp = B-A
    vB = magnitude/dp
    vA = -vB
    #add reactions to list
    global reaction
    reaction[0] += vA
    reaction[1] += vB
    #print inputs to outfile
    print(loadType, magnitude, position, file= outfile, end = "")
    print(file= outfile, end = "\n")
    

#calculate shear & moment for point load
def shearmoment_pl(i,x):
    magnitude = i[0]
    position = i[1]
    shear = magnitude
    moment = magnitude*(x-position)
    return shear, moment


#calculate shear & moment for distributed load when x is within the start position and end position    
def shearmoment_dl1(i,x):
    start_magnitude = i[0]
    end_magnitude = i[1]
    start_position = i[2]
    end_position = i[3]
    if abs(start_magnitude)>0:
        x_base = x-start_position
        f_cut = start_magnitude-x_base*(start_magnitude/(end_position-start_position))
        R1 = 0.5*x_base*(start_magnitude-f_cut)
        R2 = x_base*f_cut
        shear = R1+R2
        moment = R1*(2/3)*x_base + R2*(x_base/2)
    else:
        x_base = x-start_position
        f_cut = end_magnitude*(x_base/(end_position-start_position))
        R = 0.5*x_base*f_cut
        shear = R
        moment = R*(x_base/3)
    return shear, moment


#calculate shear & moment for distributed load when x is more than the end position
def shearmoment_dl2(i,x):
    start_magnitude = i[0]
    end_magnitude = i[1]
    start_position = i[2]
    end_position = i[3]
    if abs(start_magnitude)>0:
        R = 0.5*start_magnitude*(end_position-start_position)
        xr = start_position+(1/3)*(end_position-start_position)
        shear = R
        moment = R*(x-xr)
    else:
        R = 0.5*end_magnitude*(end_position-start_position)
        xr = start_position + (2/3)*(end_position-start_position)
        shear = R
        moment = R*(x-xr)
    return shear, moment


#calculate shear & moment for bending moment
def shearmoment_bm(i):
    magnitude = i[0]
    position = i[1]
    shear = 0
    moment = magnitude
    return shear, moment
    
    
import math
pointloadlist = []  #[magnitude, position]
distributedloadlist = []    #[start_magnitude, end_magnitude, start_position, end_position, resultant_magnitude, resultant_position]
bendingmomentlist = []  #[magnitude, position]
reaction = [0,0]    #[reaction at A, reaction at B]
shearforce = [] #[magnitude, position]
bendingmoment = []  #[magnitude, position]
divs = 10000    #number of small lengths
A = 0.0
B = 0.0
cantilever_support = 0

#choose data type
data_type = input("Would you like to input data(Y/N)?: ")
if data_type == "Y":
    data_type = "input data"
elif data_type == "N":
    data_type = input("Would you like to load file(Y/N)?: ")
    if data_type == "Y":
        data_type = "load file"
    else:
        print("See you again next time!")

        
#data file
if data_type == "load file":
    while True:
        filename = input("Enter input filename: ")
        try:
            infile = open(filename, "r")
            break
        except FileNotFoundError:
            print("Can't open file. Try again.")
            
    #retrieve beam information        
    read_beam = infile.readline()
    beam_info = read_beam.split(" ")
    beam_type = int(beam_info[0])
    beam_length = float(beam_info[1])
    #simply supported beam support locations
    if beam_type == 1:   
        A = 0.0
        B = beam_length
    #overhanging beam support locations  
    elif beam_type == 2:
        A = float(beam_info[2])
        B = float(beam_info[3])
    #cantilever beam support location 
    elif beam_type == 3:
        cantilever_support = int(beam_info[2])
        if cantilever_support==1:
            A = 0.0
            B = 0.0
        elif cantilever_support==2:
            cantilever_support = 2
            A = beam_length
            B = 0.0

    #retrieve load information
    read_load = infile.readlines()
    for i in read_load:
        load_info = i.split()        
        loadType = int(load_info[0])
        #reaction calculation for simply supported/overhanging beam
        if beam_type == 1 or beam_type == 2:
            #point load
            if loadType == 1:   
                magnitude = float(load_info[1])
                position = float(load_info[2])      
                #add load into list
                pointloadlist.append([magnitude, position])
                #calculation
                dp = A-position
                moment = magnitude*dp
                dB = B-A
                vB = moment/dB
                vA = -magnitude-vB 
                #add reaction into list
                reaction[0] += vA
                reaction[1] += vB
            #distributed load    
            elif loadType == 2: 
                start_magnitude = float(load_info[1])
                end_magnitude = float(load_info[2])
                start_position = float(load_info[3])
                end_position = float(load_info[4])          
                if start_magnitude == end_magnitude:
                    resultant_magnitude = start_magnitude*(end_position - start_position)
                    resultant_position = (start_position+end_position)/2
                elif abs(start_magnitude) >= abs(end_magnitude):
                    resultant_magnitude = 0.5*start_magnitude*(end_position - start_position)
                    resultant_position = start_position + (1/3)*(end_position - start_position)
                elif abs(start_magnitude) <= abs(end_magnitude):
                    resultant_magnitude = 0.5*end_magnitude*(end_position - start_position)
                    resultant_position = start_position + (2/3)*(end_position - start_position)
                #add load into list
                distributedloadlist.append([start_magnitude, end_magnitude, start_position, end_position, resultant_magnitude, resultant_position])
                #calculation
                dp = A-resultant_position
                moment = resultant_magnitude*dp
                dB = B-A
                vB = moment/dB
                vA = -resultant_magnitude-vB
                #add reaction into list
                reaction[0] += vA
                reaction[1] += vB
            #bending moment    
            elif loadType == 3: 
                magnitude = float(load_info[1])
                position = float(load_info[2])
                #add load into list
                bendingmomentlist.append([magnitude, position])
                #calculation
                dp = B-A
                vB = magnitude/dp
                vA = -vB
                #add reaction into list
                reaction[0] += vA
                reaction[1] += vB
            #end
            elif loadType == 4:
                break

        #reaction calculation for cantilever beam
        elif beam_type == 3:
            #point load
            if loadType == 1:   
                magnitude = float(load_info[1])
                position = float(load_info[2])      
                #add load into list
                pointloadlist.append([magnitude, position])
                #calculation
                vA = -magnitude
                #add reaction into list
                reaction[0] += vA
            #distributed load    
            elif loadType == 2: 
                start_magnitude = float(load_info[1])
                end_magnitude = float(load_info[2])
                start_position = float(load_info[3])
                end_position = float(load_info[4])          
                if start_magnitude == end_magnitude:
                    resultant_magnitude = start_magnitude*(end_position - start_position)
                    resultant_position = 0.5*((start_position+end_position)/2)
                elif abs(start_magnitude) >= abs(end_magnitude):
                    resultant_magnitude = 0.5*start_magnitude*(end_position - start_position)
                    resultant_position = start_position + (1/3)*(end_position - start_position)
                elif abs(start_magnitude) <= abs(end_magnitude):
                    resultant_magnitude = 0.5*end_magnitude*(end_position - start_position)
                    resultant_position = start_position + (2/3)*(end_position - start_position)
                #add load into list
                distributedloadlist.append([start_magnitude, end_magnitude, start_position, end_position, resultant_magnitude, resultant_position])
                #calculation
                vA = -resultant_magnitude*(end_position - start_position)
                #add reaction into list
                reaction[0] += vA
            #bending moment    
            elif loadType == 3: 
                magnitude = float(load_info[1])
                position = float(load_info[2])
                #add load into list
                bendingmomentlist.append([magnitude, position])
                #calculation
                dp = A-position
                if dp == 0:
                    vA = 0
                else:
                    vA = magnitude/dp
                #add reaction into list
                reaction[0] += vA
            #end
            elif loadType == 4:
                break
            
    infile.close()

    
#user input manually
if data_type == "input data":
    
    #output file
    while True:
        filename = input("Enter output filename: ")
        try:
            outfile = open(filename, "w")
            break
        except OSError:
            print("Can't open file. Try again.")
        
    #choose beam type    
    while True:         
        try:
            beam_type = int(input("Input the Beam Type (1.Simply supported / 2.Overhanging / 3.Cantilever): "))
            if beam_type<1 or beam_type>3:
                print("Invalid Beam Type. Please choose a Beam Type between 1-3.")
            else:
                break
        except ValueError:
            print("Value Error, please input a valid number.")
            
    #input beam length
    while True:         
        try:
            beam_length = float(input("Input the length of beam(in metres): "))
            if beam_length<=0:
                print("Invalid Beam Length. Please enter a Beam Length > 0.")
            else:
                break
        except ValueError:
            print("Value Error, please input a valid number.")
            
    
    #simply supported support locations      
    if beam_type == 1:   
        A = 0.0
        B = beam_length
        print(beam_type, beam_length, file=outfile, end = " ") 
        print(A, B, file= outfile, end = " ")
        print(file= outfile, end = "\n")
    #overhanging support locations
    elif beam_type == 2: 
        while True:         
            try:
                A = float(input("Distance to Left Support: "))
                if A<0 or A>beam_length:
                    print("Position is out of bounds.")
                    continue
                else:
                    break
            except ValueError:
                print("Value Error, please input a valid number.")
        while True:
            try:
                B = float(input("Distance to Right Support: "))
                if B<0 or B>beam_length:
                    print("Position is out of bounds.")
                    continue
                else:
                    break
            except ValueError:
                print("Value Error, please input a valid number.")
        print(beam_type, beam_length, file=outfile, end = " ") 
        print(A, B, file= outfile, end = " ")
        print(file= outfile, end = "\n")
    #cantilever support location
    elif beam_type == 3:
        while True:
            try:
                cantilever_support = int(input("Input the location of the support(1.L/2.R): "))
                if cantilever_support<1 or cantilever_support>2:
                    print("Please input 1 or 2.")
                    continue
                else:
                    break
            except ValueError:
                print("Value Error, please input a valid number.")
        if cantilever_support == 1:
            A = 0
        elif cantilever_support == 2:
            A = beam_length
        print(beam_type, beam_length, file=outfile, end = " ") 
        print(cantilever_support, file= outfile, end = " ")
        print(file= outfile, end = "\n")
    
    
    #load inputs for simply supported/overhanging beam
    if beam_type == 1 or beam_type == 2:
        while True:
            while True:
                try:
                    loadType = int(input("Select a Load (1.Point load / 2.Distributed load / 3.Bending moment/ 4.End): "))
                    if loadType>4 or loadType<1:
                        print("Invalid Load. Please choose a Load between 1-4.")
                        continue
                    else:
                        break
                except ValueError:
                    print("Value Error, please input a valid number.")
            #load reaction calclations
            if loadType == 1:    #point load
                reaction_pl(loadType)
            elif loadType == 2:  #distributed load
                reaction_dl(loadType)
            elif loadType == 3:  #bending moment
                reaction_bm(loadType)
            elif loadType == 4: #end
                print(loadType, file=outfile, end = "")
                break
            
    #load inputs for cantilever beam
    if beam_type == 3:
        while True:
            while True:
                try:
                    loadType = int(input("Select a Load (1.Point load / 2.Distributed load / 3.Bending moment/ 4.End): "))
                    break
                except ValueError:
                    print("Value Error, please input a valid number.")
                    
            #load reaction calclations
                    
            #point load
            if loadType == 1:
                #magnitude
                while True:         
                    try:
                        print("Taking downwards as -ve, upwards as +ve,")
                        magnitude = float(input("Input magnitude of Load: "))
                        break
                    except ValueError:
                        print("Value Error, please input a valid number.")
                #position
                while True:         
                    try:
                        position = float(input("Input position of Load: "))
                        if position<0 or position>beam_length:
                            print("Position is out of bounds.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Value Error, please input a valid number.")
                #add load into list
                pointloadlist.append([magnitude, position])
                #calculation        
                vA = -magnitude    
                #add reaction into list
                reaction[0] += vA
                #print inputs to outfile
                print(loadType, magnitude, position, file= outfile, end = "")
                print(file= outfile, end = "\n")
                
            #distributed load    
            elif loadType == 2:
                #start_magnitude
                while True:
                    try:    
                        print("Taking downwards as -ve, upwards as +ve,")
                        start_magnitude = float(input("Input magnitude of Load at the start: "))
                        break
                    except ValueError:
                        print("Value Error, please input a valid number.")
                #end_magnitude
                while True:
                    try:    
                        print("Taking downwards as -ve, upwards as +ve,")
                        end_magnitude = float(input("Input magnitude of Load at the end: "))
                        break
                    except ValueError:
                        print("Value Error, please input a valid number.")
                #start_position
                while True:
                    try:    
                        start_position = float(input("Input position of Load at the start: "))
                        if start_position<0 or start_position>beam_length:
                            print("Position is out of bounds.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Value Error, please input a valid number.")
                #end_position
                while True:
                    try:    
                        end_position = float(input("Input position of Load at the end: "))
                        if end_position<0 or end_position>beam_length:
                            print("Position is out of bounds.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Value Error, please input a valid number.")

                #calculate the resultant magnitude and resultant position of ditributed load        
                if start_magnitude == end_magnitude:
                    resultant_magnitude = start_magnitude*(end_position - start_position)
                elif abs(start_magnitude) >= abs(end_magnitude):
                    resultant_magnitude = 0.5*start_magnitude*(end_position - start_position)
                    resultant_position = start_position + (1/3)*(end_position - start_position)
                elif abs(start_magnitude) <= abs(end_magnitude):
                    resultant_magnitude = 0.5*end_magnitude*(end_position - start_position)
                    resultant_position = start_position + (2/3)*(end_position - start_position)
                #add load into list
                distributedloadlist.append([start_magnitude, end_magnitude, start_position, end_position, resultant_magnitude, resultant_position])
                #calculation
                vA = -resultant_magnitude
                #add reaction into list
                reaction[0] += vA
                #print inputs to outfile
                print(loadType, start_magnitude, end_magnitude, start_position, end_position, file= outfile, end = "")
                print(file= outfile, end = "\n")
                
            #bending moment
            elif loadType == 3:
                #magnitude
                while True:         
                    try:
                        print("Taking ACW as -ve, CW as +ve,")
                        magnitude = float(input("Input magnitude of Load: "))
                        break
                    except ValueError:
                        print("Value Error, please input a valid number.")
                #position
                while True:         
                    try:
                        position = float(input("Input position of Load: "))
                        if position<0 or position>beam_length:
                            print("Position is out of bounds.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Value Error, please input a valid number.")
                #add load into list        
                bendingmomentlist.append([magnitude, position])
                #calculation
                dp = A-position
                if dp == 0:
                    vA = 0
                else:
                    vA = magnitude/dp
                #add reaction into list
                reaction[0] += vA
                #print inputs to outfile
                print(loadType, magnitude, position, file= outfile, end = "")
                print(file= outfile, end = "\n")
                
            #end    
            elif loadType == 4: 
                print(loadType, file= outfile, end = "")
                break
            
    outfile.close()

#print the reaction forces   
if beam_type == 1 or beam_type == 2:
    print(f"Vertical reaction force of the first support is {reaction[0]:.3f} N")
    print(f"Vertical reaction force of the second support is {reaction[1]:.3f} N")
elif beam_type == 3:
    print(f"Vertical reaction force of the support is {reaction[0]:.3f} N")
    
#shear & moment calclations  
delta = beam_length / divs  #small length
x = 0
#create list for each small length
while x <= beam_length: 
    shearforce.append([0,x])
    bendingmoment.append([0,x])
    x += delta
shearforce.append([0,beam_length])
bendingmoment.append([0,beam_length])
#add reaction force
vA = reaction[0]
vB = reaction[1]
x = 0

#add reaction force & bending moement of supports for simply supported/overhanging beam
if beam_type == 1 or beam_type == 2:
    #iterate through each small length
    while x <= beam_length:
        shear = 0
        moment = 0
        if x>A:
            shear = vA
            moment = vA*(x-A)
            for a in shearforce:
                if a[1]==x:
                    a[0]+=shear
            for b in bendingmoment:
                if b[1]==x:
                    b[0]+=moment
        if x>B:
            shear = vB
            moment = vB*(x-B)
            for c in shearforce:
                if c[1]==x:
                    c[0]+=shear
            for d in bendingmoment:
                if d[1]==x:
                    d[0]+=moment
        x += delta  #continue to the next small length
        
#add reaction force & bending moment of support for cantilever beam        
elif beam_type == 3:
    #iterate through each small length
    while x <= beam_length:
        shear = 0
        moment = 0
        if x>A:
            shear = vA
            moment = vA*(x-A)
            for a in shearforce:
                if a[1]==x:
                    a[0]+=shear
            for b in bendingmoment:
                if b[1]==x:
                    b[0]+=moment
        x += delta  #continue to the next small length
        
#add point load reaction force & bending moment    
if len(pointloadlist)>0:
    for i in pointloadlist:
        x=0
        #iterate through each small length
        while x <= beam_length:
            shear, moment = shearmoment_pl(i,x)
            if x > i[1]:
                for a in shearforce:
                    if a[1]==x:
                        a[0]+=shear
                for b in bendingmoment:
                    if b[1]==x:
                        b[0]+=moment
            x+=delta    #continue to the next small length

#add distributed load reaction force & bending moment    
if len(distributedloadlist)>0:
    for i in distributedloadlist:
        start_magnitude = i[0]
        end_magnitude = i[1]
        start_position = i[2]
        end_position = i[3]
        x=0
        #iterate through each small length
        while x <= beam_length:
            if x > start_position and x <= end_position:
                shear, moment = shearmoment_dl1(i,x)
                for a in shearforce:
                    if a[1]==x:
                        a[0]+=shear
                for b in bendingmoment:
                    if b[1]==x:
                        b[0]+=moment
            
            elif x > end_position:
                shear, moment = shearmoment_dl2(i,x)
                for a in shearforce:
                    if a[1]==x:
                        a[0]+=shear
                for b in bendingmoment:
                    if b[1]==x:
                        b[0]+=moment
            x+=delta    #continue to the next small length

#add bending moment reaction force & bending moment      
if len(bendingmomentlist)>0:
    for i in bendingmomentlist:
        x=0
        #iterate through each small length
        while x <= beam_length:
            if x > i[1]:
                shear, moment = shearmoment_bm(i)
                for a in shearforce:
                    if a[1]==x:
                        a[0]+=shear
                for b in bendingmoment:
                    if b[1]==x:
                        b[0]+=moment
            x+=delta    #continue to the next small length

#turtle
import math
import turtle
plot = turtle.Turtle()
plot.speed(0)
plot.hideturtle()
plot.width(2)
turtle.tracer(0,0)
scale_x = 900/beam_length #How many pixel for 1 m

#plot the beam
plot.pu() 
plot.goto(-450,230)
plot.pd()
plot.goto(450,230)
plot.goto(450,210)
plot.goto(-450,210)
plot.goto(-450,230)
plot.pu()

#for simply supported/overhanging beam
if beam_type == 1 or beam_type == 2:
#plot the support 1
    plot.pu() 
    plot.goto(-450+(A*scale_x),210) 
    plot.pd()
    plot.goto(-430+(A*scale_x),190)
    plot.goto(-470+(A*scale_x),190)
    plot.goto(-450+(A*scale_x),210)
    plot.pu()
#plot the support 2
    plot.pu() 
    plot.goto(-450+(B*scale_x),210) 
    plot.pd()
    plot.goto(-430+(B*scale_x),190)
    plot.goto(-470+(B*scale_x),190)
    plot.goto(-450+(B*scale_x),210)
    plot.pu()   
#plot the reaction of support 1
    plot.pu()
    plot.goto(-450+(A*scale_x),210)
    if reaction[0]<0:
        plot.pd()
        plot.goto(-450+(A*scale_x),190)
        plot.right(90)
        plot.stamp()
        plot.left(90)
        plot.pu()
    elif reaction[0]>0:
        plot.left(90)
        plot.stamp()
        plot.pd()
        plot.goto(-450+(A*scale_x),190)
        plot.right(90)
        plot.pu()
    #plot the reaction value
    plot.pu()
    plot.goto(-450+(A*scale_x),170)
    plot.write(round(abs(reaction[0]),2))
    plot.pu()
#plot the reaction of support 2
    plot.pu()
    plot.goto(-450+(B*scale_x),210)
    if reaction[1]<0:
        plot.pd()
        plot.goto(-450+(B*scale_x),190)
        plot.right(90)
        plot.stamp()
        plot.left(90)
        plot.pu()
    elif reaction[1]>0:
        plot.left(90)
        plot.stamp()
        plot.right(90)
        plot.pd()
        plot.goto(-450+(B*scale_x),190)
        plot.pu()
    #plot the reaction value
    plot.pu()
    plot.goto(-450+(B*scale_x),170)
    plot.write(round(abs(reaction[1]),2))
    plot.pu()
#for cantilever beam
if beam_type == 3:
#plot the support
    plot.pu() 
    plot.goto(-450+(A*scale_x),210) 
    plot.pd()
    plot.goto(-430+(A*scale_x),190)
    plot.goto(-470+(A*scale_x),190)
    plot.goto(-450+(A*scale_x),210)
    plot.pu()    
#plot the reaction of support
    plot.pu()
    plot.goto(-450+(A*scale_x),210)
    if reaction[0]<0:
        plot.pd()
        plot.goto(-450+(A*scale_x),190)
        plot.right(90)
        plot.stamp()
        plot.left(90)
        plot.pu()
    elif reaction[0]>0:
        plot.left(90)
        plot.stamp()
        plot.right(90)
        plot.pd()
        plot.goto(-450+(A*scale_x),190)
        plot.pu()
    #plot the reaction value
    plot.pu()
    plot.goto(-450+(A*scale_x),170)
    plot.write(round(abs(reaction[0]),2))
    plot.pu()
#plot all the point load
if len(pointloadlist)>0:
    for i in pointloadlist:
        plot.pu()
        plot.goto(-450+((i[1])*scale_x),230)
        #-ve magnitude
        if i[0]<0:
            plot.right(90)
            plot.stamp()
            plot.left(90)
            plot.pd()
            plot.goto(-450+((i[1])*scale_x),250)
            plot.pu()
        #+ve magntiude
        elif i[0]>0:
            plot.pd()
            plot.goto(-450+((i[1])*scale_x),250)
            plot.left(90)
            plot.stamp()
            plot.right(90)
            plot.pu()
        #plot the magnitude value
        plot.pu()
        plot.goto(-450+(i[1]*scale_x),250)
        plot.write(round(abs(i[0]),2))
        plot.pu()
#plot all the distributed load
if len(distributedloadlist)>0:
    for i in distributedloadlist:
        start_f = i[0]
        end_f = i[1]
        start_x = i[2]
        end_x = i[3]
        if abs(start_f)>0 and abs(end_f)>0:
            #plot the start load
            plot.pu()
            plot.goto(-450+(start_x*scale_x),230)
            #-ve magnitude
            if start_f<0:
                plot.right(90)
                plot.stamp()
                plot.pd()
                plot.goto(-450+(start_x*scale_x),250)
                plot.left(90)
                plot.pu()
            #+ve magntiude
            elif start_f>0:
                plot.pd()
                plot.goto(-450+(start_x*scale_x),250)
                plot.left(90)
                plot.stamp()
                plot.right(90)
                plot.pu()
            #plot the magnitude value
            plot.pu()
            plot.goto(-450+(start_x*scale_x),250)
            plot.write(round(abs(start_f),2))
            plot.pu()
            #plot the end load
            plot.goto(-450+(end_x*scale_x),230)
            #-ve magnitude
            if end_f<0:
                plot.right(90)
                plot.stamp()
                plot.pd()
                plot.goto(-450+(end_x*scale_x),230+(20*end_f/start_f))
                plot.left(90)
                plot.pu()
            #+ve magntiude
            elif end_f>0:
                plot.pd()
                plot.goto(-450+(end_x*scale_x),230+(20*end_f/start_f))
                plot.left(90)
                plot.stamp()
                plot.right(90)
                plot.pu()
            #plot the magnitude value
            plot.pu()
            plot.goto(-450+(end_x*scale_x),230+(20*end_f/start_f))
            plot.write(round(abs(end_f),2))
            plot.pu()
            #plot the distribution line
            plot.goto(-450+(start_x*scale_x),250)
            plot.pd()
            plot.goto(-450+(end_x*scale_x),230+(20*end_f/start_f))
            plot.pu()
            
        else:
            plot.pu()
            plot.goto(-450+(start_x*scale_x),230)
            
            if start_f==0 and end_f<0:
                plot.right(90)
                plot.stamp()
                plot.left(90)
                plot.pu()
                plot.goto(-450+(start_x*scale_x),250)
                plot.write(0.0)
                plot.pu()
                plot.goto(-450+(end_x*scale_x),230)
                plot.right(90)
                plot.stamp()
                plot.left(90)
                plot.pd()
                plot.goto(-450+(end_x*scale_x),250)
                plot.pu()
                plot.goto(-450+(end_x*scale_x),250)
                plot.write(round(abs(end_f),2))
                plot.pu()
                
            elif start_f==0 and end_f>0:
                plot.left(90)
                plot.stamp()
                plot.right(90)
                plot.pu()
                plot.goto(-450+(start_x*scale_x),250)
                plot.write(0.0)
                plot.pu()
                plot.goto(-450+(end_x*scale_x),230)
                plot.pd()
                plot.goto(-450+(end_x*scale_x),250)
                plot.left(90)
                plot.stamp()
                plot.right(90)
                plot.pu()
                plot.goto(-450+(end_x*scale_x),250)
                plot.write(round(abs(end_f),2))
                plot.pu()
            
            elif end_f==0 and start_f<0:
                plot.right(90)
                plot.stamp()
                plot.pd()
                plot.goto(-450+(start_x*scale_x),250)
                plot.left(90)
                plot.pu()
                plot.goto(-450+(start_x*scale_x),250)
                plot.write(round(abs(start_f),2))
                plot.pu()
                plot.goto(-450+(end_x*scale_x),230)
                plot.right(90)
                plot.stamp()
                plot.left(90)
                plot.pu()
                plot.goto(-450+(end_x*scale_x),250)
                plot.write(0.0)
                plot.pu()

            elif end_f==0 and start_f>0:
                plot.pd()
                plot.goto(-450+(start_x*scale_x),250)
                plot.left(90)
                plot.stamp()
                plot.right(90)
                plot.write(round(abs(start_f),2))
                plot.goto(-450+(end_x*scale_x),230)
                plot.left(90)
                plot.stamp()
                plot.right(90)
                plot.goto(-450+(end_x*scale_x),250)
                plot.write(0.0)
                plot.pu()
           
            #plot the distribution line
            if (start_f==0 and end_f<0) or (start_f==0 and end_f>0):
                plot.goto(-450+(start_x*scale_x),232)
                plot.pd()
                plot.goto(-450+(end_x*scale_x),250)
                plot.pu()
            else:
                plot.goto(-450+(start_x*scale_x),250)
                plot.pd()
                plot.goto(-450+(end_x*scale_x),232)
                plot.pu()
#plot all the bending moment
if len(bendingmomentlist)>0:
    for i in bendingmomentlist:
        plot.pu()
        plot.goto(-450+(i[1]*scale_x),190)
        #-ve magnitude
        if i[0]<0:
            plot.pd()
            plot.circle(30)
            plot.pu()
            plot.stamp()
        #+ve magntiude
        elif i[0]>0:
            plot.pd()
            plot.circle(30)
            plot.pu()
            plot.right(180)
            plot.stamp()
            plot.left(180)
            plot.pu()
        #plot the magnitude value
        plot.pu()
        plot.goto(-450+(i[1]*scale_x),170)
        plot.write(round(abs(i[0]),2))
        plot.pu()
        

#Draw the shear force & bending moment graph
j = turtle.Turtle()   
j.speed(0)
j.width(1)

#plot the axis
def plot_axes(x0, y0):
   j.pu()
   j.goto(x0, y0) # put a dot at origin
   j.dot(5) #dot size
   j.pd()  # x-axis
   j.goto(x0+(beam_length*scale_x), y0)
   j.stamp()
   j.pu()   # y-axis
   j.goto(x0, y0-115)
   j.pd()
   j.goto(x0, y0+115)
   j.left(90)
   j.stamp()
   j.right(90)
   j.pu()

#sheer force graph axis
x0, y0 = -450, 40
plot_axes(x0, y0)
j.pu()
j.goto(x0-30,y0+115)
j.write("Shear Force / N")
j.pu()
j.goto(x0+(beam_length*scale_x)+20, y0)
j.write("x / m")
j.pu()

#bending moment graph axis
x0, y0 = -450, -200
plot_axes(x0, y0)
j.pu()
j.goto(x0-30,y0+115)
j.write("Bending Moment / Nm")
j.pu()
j.goto(x0+(beam_length*scale_x)+20, y0)
j.write("x / m")
j.pu()

#shear force scale
shear_magnitude = []
for i in shearforce:
    shear_magnitude.append(abs(i[0]))
    max_sf = max(shear_magnitude)
scale_shear = 110/max_sf
#shear force graph plotting    
x0_sf , y0_sf = -450, 40 #Origin for shear force diagram
j.goto(x0_sf,y0_sf)
j.pd()
for i in shearforce:
    j.goto(x0_sf+(i[1]*scale_x), y0_sf+(i[0]*scale_shear))
j.pu()

#bending moment scale
bm_magnitude = []
for i in bendingmoment:
    bm_magnitude.append(abs(i[0]))
    max_bm = max(bm_magnitude)
scale_bm = 110/max_bm
#bending moment graph plotting    
x0_bm , y0_bm = -450, -200 #Origin for shear force diagram
j.goto(x0_bm,y0_bm)
j.pd()
for i in bendingmoment:
    j.goto(x0_bm+(i[1]*scale_x), y0_bm+(i[0]*scale_bm))
j.pu()
