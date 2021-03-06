# DYNAMICS

def quickDyn(spread=5, num=10, joints=False, bake=False):
    target = []
    g = py.gravity()

    for i in range(0,num):
        c = py.polyCube()
        target.append(c)
        x = rnd(-spread,spread)
        y = rnd(-spread,spread) + 10
        z = rnd(-spread,spread)
        py.move(x,y,z)
        py.rotate(x,y,z)

    s(target)
    py.rigidBody()

    for i in range(0,len(target)):
        py.connectDynamic(target[i],f=g)

    if(joints==False and bake==True):
        bakeAnimation(target)
        
    if(joints==True):
        target2 = []

        for i in range(0,len(target)):
            s(target[i])
            jnt = py.joint()
            target2.append(jnt)
            
        if(bake==True):
            bakeAnimation(target2)

        for i in range(0,len(target2)):
            unparent(target2[i])

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
