from guizero import App, PushButton, Text

def button_pressed():
    name = app.question("Hello", "What's your name?")
    # If cancel is pressed, None is returned
    # so check a name was entered
    if name is not None:
        hello.value = "Hello " + name

app = App()
button = PushButton(app, command=button_pressed, text="Hello")
hello = Text(app)
app.display()