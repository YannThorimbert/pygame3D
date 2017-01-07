import thorpy


myobj = Object3D("myobject.stl")
objs = [myobj]

app = thorpy.Application((500,500))

m = thorpy.Menu()
m.play()

app.quit()