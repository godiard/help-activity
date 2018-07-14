:orphan:

.. _logo-code-for-turing-machine:

=======================================
Logo code for Turtle Art Turing Machine
=======================================

Logo code saved from Turtle Art Turing Machine session

::

    window

    comment: functions that implement Turtle Art blocks

    to tasetpalette :i :r :g :b :myshade 
    make "s ((:myshade - 50) / 50) 
    ifelse lessp :s 0 [ 
    make "s (1 + (:s *0.8)) 
    make "r (:r * :s) 
    make "g (:g * :s) 
    make "b (:b * :s) 
    ] [ make "s (:s * 0.9) 
    make "r (:r + ((99-:r) * :s)) 
    make "g (:g + ((99-:g) * :s)) 
    make "b (:b + ((99-:b) * :s)) 
    ] setpalette :i (list :r :g :b) 
    end 


    to rgb :myi :mycolors :myshade 
    make "myr first :mycolors 
    make "mycolors butfirst :mycolors 
    make "myg first :mycolors 
    make "mycolors butfirst :mycolors 
    make "myb first :mycolors 
    make "mycolors butfirst :mycolors 
    tasetpalette :myi :myr :myg :myb :myshade 
    output :mycolors 
    end 


    to processcolor :mycolors :myshade 
    if emptyp :mycolors [stop] 
    make "i :i + 1 
    processcolor (rgb :i :mycolors :myshade) :myshade 
    end 


    to tasetshade :shade 
    make "myshade modulo :shade 200 
    if greaterp :myshade 99 [make "myshade (199-:myshade)] 
    make "i 7 
    make "mycolors :colors 
    processcolor :mycolors :myshade 
    end 


    to tasetpencolor :c 
    make "color (modulo (round :c) 100) 
    setpencolor :color + 8 
    end 


    make "colors [
     99  0  0
     99  5  0
     99 10  0
     99 15  0
     99 20  0
     99 25  0
     99 30  0
     99 35  0
     99 40  0
     99 45  0
     99 50  0
     99 55  0
     99 60  0
     99 65  0
     99 70  0
     99 75  0
     99 80  0
     99 85  0
     99 90  0
     99 95  0
     99 99  0
     90 99  0
     80 99  0
     70 99  0
     60 99  0
     50 99  0
     40 99  0
     30 99  0
     20 99  0
     10 99  0
      0 99  0
      0 99  5
      0 99 10
      0 99 15
      0 99 20
      0 99 25
      0 99 30
      0 99 35
      0 99 40
      0 99 45
      0 99 50
      0 99 55
      0 99 60
      0 99 65
      0 99 70
      0 99 75
      0 99 80
      0 99 85 
      0 99 90
      0 99 95
      0 99 99
      0 95 99
      0 90 99
      0 85 99
      0 80 99
      0 75 99
      0 70 99
      0 65 99
      0 60 99
      0 55 99 
      0 50 99
      0 45 99
      0 40 99
      0 35 99
      0 30 99
      0 25 99
      0 20 99
      0 15 99
      0 10 99
      0  5 99
      0  0 99
      5  0 99
     10  0 99
     15  0 99
     20  0 99
     25  0 99
     30  0 99
     35  0 99
     40  0 99
     45  0 99
     50  0 99
     55  0 99
     60  0 99
     65  0 99
     70  0 99
     75  0 99
     80  0 99
     85  0 99
     90  0 99
     95  0 99
     99  0 99
     99  0 90
     99  0 80
     99  0 70
     99  0 60
     99  0 50
     99  0 40
     99  0 30
     99  0 20
     99  0 10] 
    make "shade  50 
    tasetshade :shade 


    to tapop
    if emptyp :taheap [stop]
    make "tmp first :taheap
    make "taheap butfirst :taheap
    output :tmp
    end


    to taminus :y :x
    output sum :x minus :y
    end


    to tasetxy :x :y
    setxy :x :y
    end


    comment: Turing Machine procedures


    to turtleblocks_0
    comment: Comment
     #sTuring_Machine 
    end


    to start
    comment: main program
    comment: Creates and initializes necessary variables, writes program block, writes tape, runs program
     clean #sSetup #sProgram #sTape #sExecute 
    end


    to #sSetup
    comment: Create variables, set initial values
     right 90.0
     setpensize 25.0
     tasetpencolor 0.0
     tasetshade 50.0 penup
     make "#scell 0.0
     make "#ssymbol 0.0
     make "#smove 0.0
     make "#sstate 1.0
     make "#sleftedge -390.0
     make "#stapey 290.0
     make "#sprogramy 200.0
     make "#scellwidth 25.0
     make "#sright 1.0
     make "#shalt 4.0 
     make "#sA 3.0
     make "#sB 2.0
    end


    to #sTape
    comment: Write initial tape. User can change values in repeat statements to change arguments.
     #sToTape
     pendown
     tasetpencolor 20.0
     repeat #sA [ #sWriteCell ] 
     tasetpencolor 0.0
     #sWriteCell
     tasetpencolor 20.0
     repeat #sB [ #sWriteCell ] 
     tasetpencolor 0.0
     #sWriteCell #sToTape penup 
    end


    to #sProgram
    comment: Write program table
     tasetxy :#sleftedge :#sprogramy
     tasetpencolor 20.0
     #sWriteCell
     tasetpencolor 20.0
     #sWriteCell
     tasetpencolor 40.0
     #sWriteCell
     tasetxy :#sleftedge taminus ycor :#scellwidth 
     tasetpencolor 20.0
     #sWriteCell
     tasetpencolor 20.0
     #sWriteCell
     tasetpencolor 20.0
     #sWriteCell
     tasetxy :#sleftedge taminus ycor :#scellwidth 
     tasetpencolor 0.0
     #sWriteCell
     tasetpencolor 0.0
     #sWriteCell
     tasetpencolor 60.0
     #sWriteCell
     stack1 
    end

    to stack1
    comment: Continuation of Program so that the segments fit on the Turtle Art screen
     tasetxy :#sleftedge taminus ycor :#scellwidth 
     tasetpencolor 20.0
     #sWriteCell
     tasetpencolor 20.0
     #sWriteCell
     tasetpencolor 40.0
     #sWriteCell
     tasetxy :#sleftedge taminus ycor :#scellwidth 
     tasetpencolor 0.0
     #sWriteCell
     tasetpencolor 20.0
     #sWriteCell
     tasetpencolor 80.0
     #sWriteCell
     tasetxy
      :#sleftedge taminus ycor
      :#scellwidth
     tasetpencolor 0.0
     #sWriteCell
     tasetpencolor 20.0
     #sWriteCell
     tasetpencolor 80.0
     #sWriteCell
     penup 
    end


    to #sExecute

    comment: Test for halt or next program step
     make "#sstep 0.0
     forever 
      [ ifelse ( equal? :#sstate :#shalt )
      [  stop ]
      [ #sReadPixel
        #sSetValue
        make "#ssymbol :#sValue
        #sToProgram
        wait 1.0
        #sSetSymbol
        forward :#scellwidth
        #sSetMove
        forward :#scellwidth
        #sSetState
        #sLog
        #sToTape
        #sWriteSymbol
        #sNewCell
        wait 1.0
        make "#sstep sum :#sstep 1.0 ] ] 
    end


    to #sToTape
    comment: Move turtle to current cell on tape
     tasetxy
      sum :#sleftedge product :#scellwidth :#scell
      :#stapey 
    end


    to #sToProgram
    comment: Move Turtle to beginning of current program row to execute
     tasetxy
      taminus :#sleftedge 3.0 
      taminus :#sprogramy product :#scellwidth sum :#ssymbol product 2.0 taminus :#sstate 1.0 
    end


    to #sWriteCell

    comment: Write current color to current cell, and move to next cell
     pendown
     forward 0.0
     penup
     forward :#scellwidth 
    end


    to #sWriteSymbol
    comment: Write current color in cell without moving
     pendown
     forward 0.0
     penup 
    end


    to #sReadPixel

    comment: Read RGB values of pixel to stack, pop to variables
     keyboard
     make "#sR tapop
     make "#sG tapop
     make "#sB tapop 
    end


    to #sSetValue
    comment: Find value of cell symbol from RGB numbers
      ifelse not ( equal? :#sB 128.0 ) 
       [  ifelse not ( equal? :#sR 128.0 ) 
        [  ifelse not ( equal? :#sG 128.0 ) 
         [  ifelse ( equal? :#sG 0.0 )
         [  make "#sValue 0.0 ]
        [ make "#sValue 1.0 ] ]
       [ make "#sValue 3.0 ] ]
      [ make "#sValue 4.0 ] ]
     [ make "#sValue 2.0 ] 
    end


    to #sSetMove
    comment: Read next Move direction from program table
     #sReadPixel
     #sSetValue
     make "#smove :#sValue 
    end


    to #sSetSymbol
    comment: Read next Symbol to write from program table
     #sReadPixel
     #sSetValue
     make "#ssymbol :#sValue 
     ifelse ( equal? :#ssymbol 0.0 )
      [  tasetpencolor 0 ]
      [ tasetpencolor 20.0 ] 
    end


    to #sSetState
    comment: Read next State from program table
     #sReadPixel
     #sSetValue
     make "#sstate :#sValue 
    end


    to #sNewCell
    comment: Move left or right and set cell number of new location
      ifelse ( equal? :#smove :#sright )
       [ forward :#scellwidth
         make "#scell sum :#scell 1.0 ]
       [ back :#scellwidth
         make "#scell taminus :#scell 1.0 ] 
    end


    to #sLog
    comment: Write Step number, Symbol, Move, State, Cell number on new log line in black, saving and restoring
    comment: current position and current color
     make "#sx xcor
     make "#sy ycor
     tasetxy -300.0 taminus 200.0 product 20.0 :#sstep 
     make "#scolor pencolor
     tasetpencolor 0
     label sentence ('box', "427)
     #sstep
     forward 30.0
     label sentence ('box', "339)
     #ssymbol
     forward 20.0
     label sentence ('box', "341)
     #smove
     forward 20.0
     label sentence ('box', "537)
     #sstate
     forward 20.0
     label sentence ('box', "562)
     #scell
     tasetpencolor :#scolor 
    end
