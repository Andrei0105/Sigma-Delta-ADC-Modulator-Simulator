from tkinter import *
from PIL import Image, ImageTk
import time

currentstep=0
sumout = 0
integratorout = 0
comparatorout = 0
dacout = 0
repetitionlen = 0
x = 0
bitstream = []
afterid = 0
generatedvalues = []
listnofzeros = []
listnofones = []
listofreplen = []
listcurrentgenval = []
lastmodifiedvalue = 0

def reset(textSumator, textIntegrator, textComparator, textDac,
              textBoxVin, textBoxDac, textAdcOut, textRepetare,
              textOnes, textBitStream, sliderInterval):
    global x
    global bitstream
    global currentstep
    global lastmodifiedvalue
    global generatedvalues
    global listnofones
    global listofreplen
    global listnofzeros
    global listcurrentgenval
    x = 0
    currentstep = 0
    lastmodifiedvalue = 0
    listnofones = []
    listofreplen = []
    listnofzeros = []
    bitstream = []
    generatedvalues = []
    listcurrentgenval = []
    textBitStream.delete(1.0, END)
    textSumator['text'] = "0"
    textIntegrator['text'] = "0"
    textComparator['text'] = "0"
    textDac['text'] = "0"
    textOnes['text'] = "No of 1s: - | No of 0s: -"
    textAdcOut['text'] = "Current generated value: -"
    textRepetare['text'] = "Repetition length: -"
    textBoxVin.delete(0, END)
    textBoxVin.insert(0, "")
    textBoxDac.delete(0, END)
    textBoxDac.insert(0, "")
    sliderInterval.set(1000)
    textSumator.config(fg='black')
    textIntegrator.config(fg='black')
    textComparator.config(fg='black')
    textDac.config(fg='black')

def waitforstopinput(tkFrame):
    tkFrame.after_cancel(afterid)

def previousstep(textSumator, textIntegrator, textComparator, textDac,
                    textBitStream, textRepetare, textOnes, textAdcOut):
    global currentstep
    global lastmodifiedvalue
    global x
    global sumout
    global integratorout
    global comparatorout
    global dacout
    global listnofones
    global listofreplen
    global listnofzeros
    global listcurrentgenval
    global repetitionlen
    if currentstep == 0 and x != 0:
        currentstep = 3
        x = x - 1
        dacout = generatedvalues[-1]
        generatedvalues.pop()
        textDac['text'] = "%.2f" % dacout
        textDac.config(fg='red')
        textSumator.config(fg='black')
    elif currentstep == 0:
        pass
    elif currentstep == 1:
        currentstep = 0
        x = x - 1
        sumout = generatedvalues[-1]
        generatedvalues.pop()
        textSumator['text'] = "%.2f" % sumout
        textSumator.config(fg='red')
        textIntegrator.config(fg='black')
    elif currentstep == 2:
        currentstep = 1
        x = x - 1
        integratorout = generatedvalues[-1]
        generatedvalues.pop()
        textIntegrator['text'] = "%.2f" % integratorout
        textIntegrator.config(fg='red')
        textComparator.config(fg='black')
    elif currentstep == 3:
        currentstep = 2
        x = x - 1
        comparatorout = generatedvalues[-1]
        generatedvalues.pop()
        bitstream.pop()
        textBitStream.delete("1." + str(int(x/4)))
        if listofreplen[-1]>int(x/4):
            textBitStream.tag_delete("rep2")
            textBitStream.tag_add("rep2", "1.0", "1."+str(listofreplen[-1]))
            textBitStream.tag_config("rep2", background="white", foreground="black")
            textBitStream.tag_delete("rep1")
            textBitStream.tag_add("rep1", "1.0", "1."+str(listofreplen[-2]))
            textBitStream.tag_config("rep1", background="red", foreground="white")
            textOnes['text'] = "No of 1s: "+ str(listnofones[-2]) + " | No of 0s: "+ str(listnofzeros[-2])
            listnofones.pop()
            listnofzeros.pop()
            textRepetare['text'] = "Repetition length: " +  str(listofreplen[-2])
            listofreplen.pop()
            textAdcOut['text'] = "Current generated value: " + "%.4f" % listcurrentgenval[-2]
            listcurrentgenval.pop()
        textComparator['text'] = comparatorout
        textComparator.config(fg='red')
        textDac.config(fg='black')

def replength(stream):
    repetitionlength = 1
    maxlength = int(len(stream) / 2)
    for x in range(2, maxlength + 1):
        if stream[0:x] == stream[x:2*x] :
            repetitionlength = x
    return repetitionlength

def process(textSumator, textIntegrator, textComparator, textDac,
              textBoxVin, textBoxDac, textAdcOut, textRepetare,
              textOnes, sliderInterval, textBitStream, tkFrame, simtype):
     global bitstream
     global currentstep
     global sumout
     global integratorout
     global comparatorout
     global dacout
     global repetitionlen
     global x
     global afterid
     global lastmodifiedvalue
     global listnofones
     global listofreplen
     global listnofzeros
     global listcurrentgenval
     if x<2048*4: #maximum number of steps
         tkFrame.update()
         tkFrame.update_idletasks()
         vref = float(textBoxDac.get())
         if currentstep == 0:
             generatedvalues.append(sumout)
             lastmodifiedvalue = sumout
             sumout = float(textBoxVin.get()) - float(textDac['text'])
             textSumator['text'] = "%.2f" % sumout
             textSumator.config(fg='red')
             textDac.config(fg='black')
             currentstep += 1
         elif currentstep == 1:
             generatedvalues.append(integratorout)
             lastmodifiedvalue = integratorout
             integratorout = sumout + float(textIntegrator['text'])
             textIntegrator['text'] = "%.2f" % integratorout
             textIntegrator.config(fg='red')
             textSumator.config(fg='black')
             currentstep += 1
         elif currentstep == 2:
             generatedvalues.append(comparatorout)
             lastmodifiedvalue = comparatorout
             comparatorout = 1 if integratorout >= 0 else 0
             textBitStream.insert(END, str(comparatorout))
             textBitStream.see(END)
             textComparator['text'] = comparatorout
             bitstream.append(comparatorout)
             currentrepetitionlen = replength(bitstream)
             if repetitionlen == 0:
                 repetitionlen = currentrepetitionlen
                 listofreplen.append(0)
                 listofreplen.append(1)
                 listnofzeros.append(0)
                 listnofones.append(0)
                 listnofzeros.append(bitstream[0:currentrepetitionlen].count(0))
                 listnofones.append(bitstream[0:currentrepetitionlen].count(1))
                 listcurrentgenval.append(0)
                 listcurrentgenval.append(vref*2*float(sum(bitstream[0:repetitionlen if repetitionlen >= 1 else -1]))/len(bitstream[0:repetitionlen if repetitionlen >= 1 else -1]) - vref)
             else:
                 reptimes = int(currentrepetitionlen/repetitionlen)
                 res = 0
                 if reptimes < 2 or repetitionlen == 1:
                     res=1
                 for y in range(0, reptimes-2):
                     if bitstream[y*repetitionlen:(y+1)*repetitionlen] != bitstream[(y+1)*repetitionlen:(y+2)*repetitionlen]:
                         res = 1 #not repeating

                 if currentrepetitionlen % repetitionlen != 0:
                     res = 1

                 if res == 1:
                     if repetitionlen != currentrepetitionlen:
                         if currentrepetitionlen not in listofreplen: #to avoid having 2 duplicate elements in the lists after a previousstep -> start/nextstep sequence
                            listofreplen.append(currentrepetitionlen)
                            listnofzeros.append(bitstream[0:currentrepetitionlen].count(0))
                            listnofones.append(bitstream[0:currentrepetitionlen].count(1))
                            listcurrentgenval.append(vref*2*float(sum(bitstream[0:currentrepetitionlen if currentrepetitionlen >= 1 else -1]))/len(bitstream[0:currentrepetitionlen if currentrepetitionlen >= 1 else -1]) - vref)
                     repetitionlen = currentrepetitionlen
                     nofzeros = bitstream[0:repetitionlen].count(0)
                     nofones = bitstream[0:repetitionlen].count(1)
                     textOnes['text'] = "No of 1s: "+ str(nofones) + " | No of 0s: "+ str(nofzeros)

             adcOut = vref*2*float(sum(bitstream[0:repetitionlen if repetitionlen >= 1 else -1]))/len(bitstream[0:repetitionlen if repetitionlen >= 1 else -1]) - vref
             textAdcOut['text'] = "Current generated value: " + "%.4f" % adcOut
             textRepetare['text'] = "Repetition length: " +  str(repetitionlen)
             textComparator.config(fg='red')
             textIntegrator.config(fg='black')
             textBitStream.tag_add("rep", "1.0", "1."+str(repetitionlen))
             textBitStream.tag_config("rep", background="red", foreground="white")
             currentstep += 1
         elif currentstep == 3:
             generatedvalues.append(dacout)
             lastmodifiedvalue = dacout
             dacout = vref if comparatorout == 1 else (-vref)
             textDac['text'] = dacout
             textDac.config(fg='red')
             textComparator.config(fg='black')
             currentstep = 0
         if simtype=="continuous":
            afterid = tkFrame.after(sliderInterval.get(), lambda: process(textSumator, textIntegrator, textComparator, textDac,
                            textBoxVin, textBoxDac, textAdcOut, textRepetare, textOnes, sliderInterval, textBitStream, tkFrame, simtype))
         x = x + 1

def sigmadelta():

    sumout=0.0
    integratorout=0.0
    comparatorout=0
    dacout=0.0

    root=Tk()
    root.title("Sigma-Delta ADC/Modulator Simulation")
    tkFrame=Frame(root, width=530, height = 470, bg='white')
    tkFrame.pack()

    tkFrame.imAdc = Image.open("adc.jpg")
    tkFrame.imageAdc = ImageTk.PhotoImage(tkFrame.imAdc)

    tkFrame.labelImageAdc = Label(image = tkFrame.imageAdc)
    tkFrame.labelImageAdc.place(x = 55, y = 30)


    tkFrame.textSumator = Label(text = "0", font=("Helvetica", 16))
    tkFrame.textSumator.place(x = 155, y = 0)

    tkFrame.textIntegrator = Label(text = "0", font=("Helvetica", 16))
    tkFrame.textIntegrator.place(x = 305, y = 0)

    tkFrame.textComparator = Label(text = "0", font=("Helvetica", 16))
    tkFrame.textComparator.place(x = 505, y = 70)

    tkFrame.textDac = Label(text = "0", font=("Helvetica", 16))
    tkFrame.textDac.place(x = 220, y = 270)

    tkFrame.textBoxVin = Entry( font=("Helvetica", 16), width = 3)
    tkFrame.textBoxVin.place(x = 5, y = 30)

    tkFrame.textBoxDac = Entry( font=("Helvetica", 16), width = 3)
    tkFrame.textBoxDac.place(x = 300, y = 270)

    tkFrame.textAdcOut = Label(text = "Current generated value: -", font=("Helvetica", 12))
    tkFrame.textAdcOut.place(x = 20, y = 313)

    tkFrame.textRepetare = Label(text = "Repetition length: -", font=("Helvetica", 12))
    tkFrame.textRepetare.place(x = 20, y = 336)

    tkFrame.textOnes = Label(text = "No of 1s: - | No of 0s: -", font=("Helvetica", 12))
    tkFrame.textOnes.place(x = 20, y = 359)

    tkFrame.sliderInterval = Scale(from_=1000, to=100)
    tkFrame.sliderInterval.set(1000)
    tkFrame.sliderInterval.place(x=5, y=160)

    tkFrame.textBitStream = Text(height = 3, width = 54, font=("Helvetica", 12))
    tkFrame.scroll = Scrollbar()
    tkFrame.textBitStream.place(x=25,y=400)
    tkFrame.scroll.config(command = tkFrame.textBitStream.yview)
    tkFrame.textBitStream.config(yscrollcommand=tkFrame.scroll.set)
    tkFrame.scroll.place(x=5,y=400)
    tkFrame.buttonSimulation = Button( text="Start", command=lambda:process(
                                                             tkFrame.textSumator,
                                                             tkFrame.textIntegrator,
                                                             tkFrame.textComparator,
                                                             tkFrame.textDac,
                                                             tkFrame.textBoxVin,
                                                             tkFrame.textBoxDac,
                                                             tkFrame.textAdcOut,
                                                             tkFrame.textRepetare,
                                                             tkFrame.textOnes,
                                                             tkFrame.sliderInterval,
                                                             tkFrame.textBitStream,
                                                             tkFrame,
                                                             "continuous"
                                                             ))
    tkFrame.buttonSimulation.place(x = 300, y= 310)

    tkFrame.buttonNext = Button( text="Next step", command=lambda:process(
                                                             tkFrame.textSumator,
                                                             tkFrame.textIntegrator,
                                                             tkFrame.textComparator,
                                                             tkFrame.textDac,
                                                             tkFrame.textBoxVin,
                                                             tkFrame.textBoxDac,
                                                             tkFrame.textAdcOut,
                                                             tkFrame.textRepetare,
                                                             tkFrame.textOnes,
                                                             tkFrame.sliderInterval,
                                                             tkFrame.textBitStream,
                                                             tkFrame,
                                                             "manual"
                                                             ))
    tkFrame.buttonNext.place(x = 300, y= 340)

    tkFrame.buttonStop = Button( text="Stop", command=lambda:waitforstopinput(tkFrame))
    tkFrame.buttonStop.place(x = 341, y= 310)

    tkFrame.buttonReset = Button( text="Reset", command=lambda:reset(tkFrame.textSumator,
                                                            tkFrame.textIntegrator,
                                                            tkFrame.textComparator,
                                                            tkFrame.textDac,
                                                            tkFrame.textBoxVin,
                                                            tkFrame.textBoxDac,
                                                            tkFrame.textAdcOut,
                                                            tkFrame.textRepetare,
                                                            tkFrame.textOnes,
                                                            tkFrame.textBitStream,
                                                            tkFrame.sliderInterval))
    tkFrame.buttonReset.place(x = 382, y= 310)

    tkFrame.buttonPrev = Button( text="Previous step", command=lambda:previousstep(tkFrame.textSumator,
                                                            tkFrame.textIntegrator,
                                                            tkFrame.textComparator,
                                                            tkFrame.textDac,
                                                            tkFrame.textBitStream,
                                                            tkFrame.textRepetare,
                                                            tkFrame.textOnes,
                                                            tkFrame.textAdcOut))
    tkFrame.buttonPrev.place(x = 366, y= 340)

    tkFrame.textInterval = Label(text = "Simulation step(ms)", font=("Helvetica", 11))
    tkFrame.textInterval.place(x = 5, y=265)
    root.mainloop()

sigmadelta()
