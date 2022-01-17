
Gui, Add, Link,,<a href="www.google.com">Welcome to Wolf v2.</a>
Gui, Font, norm
Gui, Add, Text, , Hold r to use auto clicker
Gui, Add, Text, , Hold x and sit to use brige
Gui, Add, Text, , Press ctrl + g to Reloads script
Gui, Add, Text, , Press ctrl + p to close
Gui, Add, Button, , OK




 
  ButtonOK:
MsgBox Out of date version.
  MsgBox Pls try again.
MsgBox Done.
 Gui, Submit, Destroy
  Return



  Gui, Show
  Return
 


;YEs
 ;Auto clicker
r:: 						
	continue := true			
	Sleep 5
	
	Loop {
		Sleep 1
		if not GetKeyState("r","P"){
			
			break
		}	
		
		Loop, 12
		{
		Click left
		Sleep 1
		}
		
		Sleep 1
	
		Loop, 12
		{
		Click left
		Sleep 1
		}

	}
return

;brige zone


x:: 						
	continue := true			
	Sleep 5
	Send {s down}
	Loop {
		Sleep 1
		if not GetKeyState("p","P"){
			Send {s up}
			break
		}	
		Send {d down}
		Loop, 12
		{
		Click right
		Sleep 1
		}
		Send {d up}
		Sleep 1
		Send {a down}
		Loop, 12
		{
		Click right
		Sleep 1
		}
		Send {a up}	
	}
return
;end


  ;Reloads the script (save before reloading!)

^g::Reload
return

;Closes the script entirely

^p::ExitApp 
