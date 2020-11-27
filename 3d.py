import turtle

wn = turtle.Screen()
wn.setup(width = 500, height = 500)

vertices = []
lines = []

xrot = 1
yrot = 1

def vert(x, y, z):
    vertname = 'vert' + str(len(vertices) + 1)
    globals()[vertname] = turtle.Turtle()
    globals()[vertname].shapesize(0.5, 0.5)
    globals()[vertname].hideturtle()
    globals()[vertname].shape('circle')
    globals()[vertname].penup()
    if z == 0:
        globals()[vertname].goto(x, y)
    else:
        globals()[vertname].goto((x + (yrot * z)), (y + (xrot * z)))
    globals()[vertname].showturtle()
    vertices.append((x, y, z))

def line(num1, num2):
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(globals()['vert' + str(num1)].pos())
    turtle.pendown()
    turtle.goto(globals()['vert' + str(num2)].pos())  
    lines.append((vertices[num1 - 1], vertices[num2 - 1]))


wn.tracer(0)

vert(0, 0, 0)
vert(0, 0, 120)

line(1, 2)

wn.tracer(1)
