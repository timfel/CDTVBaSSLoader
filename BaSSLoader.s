; Hardcode special addresses and library function offsets, so we don't include copyrighted ndk includes

DMACON			EQU $DFF096
SysBase			EQU 4
OpenLibrary		EQU -552
CloseLibrary		EQU -414
Execute			EQU -222

; Note: the program lacks proper startup code, so it will not run from Workbench

	LEA	DosName,A1		; "dos.library" name string
	CLR.L	D0			; whatever version works
	MOVEA.L	SysBase,A6
	JSR	OpenLibrary(A6)

	TST.L	D0			; zero if OpenLibrary() failed
	BEQ.S	NoDos			; if failed, skip to exit

	MOVE.W	#$8120,DMACON		; just make sure to enable sprites and bitplane dma

	MOVEA.L	D0,A6			; moving DOSBase to A6
	MOVE.L	#SteelExe,D1		; string to execute
	CLR.L	D2			; NULL input ptr
	CLR.L	D3			; NULL output ptr
	JSR	Execute(A6)

	MOVEA.L	A6,A1			; A6 has DOSBase ptr, the library to close
	MOVEA.L	SysBase,A6
	JSR	CloseLibrary(A6)

NoDos:
	CLR.L	D0			; return 0 to the system
	RTS

DosName			DC.B		"dos.library",0
SteelExe		DC.B		"steelsky",10,0
