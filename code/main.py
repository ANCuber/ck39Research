import PySimpleGUI as sg
import process as worker
print("ready")
# All the stuff inside your window.
font = ('SimSun', 24, 'bold')
while True:
    # Create the Window
    layout = [ 
            [sg.Text('Please enter a mathematical expression',size=(20,5),font=font), sg.InputText(size=(20,5),font=font)],
            [sg.Button('submit',size=(20,1),font=font)] ]
    window = sg.Window('Text2LaTex', layout,resizable=True)
    # Event Loop to process "events" and get the "values" of the inputs
    s=""
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'submit':
            s = values[0] # if user closes window or clicks cancel
            break

    window.close()

    signs = ["大於等於","小於等於","等於","大於","小於"]
    k = 5
    for i in range(0,5):
        if(s.find(signs[i])>=0):
            k = i
            break
    st = worker.processed(s,k)
    st = worker.retrived(st)
    result = worker.generate(st,k)

    ans = worker.rev(result,s)
    over= 0
    layout2 = [[sg.Text('Generate:',size=(20,5),font=font),sg.Input(ans,size=(10,5), disabled=True, text_color=sg.theme_text_color(), disabled_readonly_background_color=sg.theme_text_element_background_color(),font=font)],[sg.Button('next',size=(20,1),font=font)]]


    window2 = sg.Window('Tex2LaTex', layout2,resizable=True)

    while True:
        event, values = window2.read()
        if event == sg.WIN_CLOSED:
            over=1# if user closes window or clicks cancel
            break
        elif event=='next':
            over=0
            break

    window2.close()
    if over==1:
        print("exiting...")
        break
