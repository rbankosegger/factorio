# Bugs

One belt cannot end into another

Watch out that multiple touching points dont screw up the order
 	-> Construct example such that the belt must touch the following in order
    		a) touch point of order 1
    		b) multi-touch-point of order 3
    		c) touch point of order 2
    		d) another multi-touch-point of order 3


# Factorio-specifics

	* Burner inserters??
	* Long inserters
    * Two inserters with belt inbetween may reduce to one inserter
    * Electric power source as input specification, with reachable-within-distance constraint
		For inserters, assemblers
	* Mining drills can be placed directly in contact with other buildings?
	
# Scenario-ideas

## 	iron gears: don't worry about refuelling or electricity
	
		iron drill
		iron smelter
		1 = { belt: drill < inserter(smelter);	
			  touch(drill,smelter) }
		assembler
		1 = { belt: inserter(smelter) < inserter(assembler);	
		      touch(smelter,inserter,assembler) }
		
## 	automation science pack: don't worry about refuelling or electricity
	
		iron drill
		iron smelter
		direct connection (iron drill, iron smelter)
		
		copper drill
		copper smelter
		direct connection (copper drill, copper smelter)
		
		iron gear assembler
		inserter connection (iron smelter, iron gear assembler)
		
		sci-pack assembler
		inserter connection (copper smelter, sci-pack assembler)
		inserter connection (iron gear assembler, sci-pack assembler)
		
		lab	
		inserter connection(sci-pack assembler, lab)

## 	self-sustaining iron plate smelter
		
		Method 2:
		https://wiki.factorio.com/Burner_mining_drill
		
			coal drill(s)
			belt 
				coal drill(s)
				**burner inserter(s) ??** on axis with coal drill(s)
				targets
					iron drill
					iron smelter
					**burner inserters???**
				
			iron drill
			belt / ** burner inserter ??** / **direct??**
				iron drill
				iron smelter
				
			iron smelter		
				[ ore: 1/3.2s ]
				[ coal: 
			belt
				iron smelter
				(inserter??, **direct??** ) box
			chest
			
			
	
