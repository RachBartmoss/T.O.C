
# T.O.C
                            
                                                                                                    
                                                                                                    
                                                                                                    
                        .:::.                                        :~7JJJ?!:                      
                      ^?JJJYYJ?^                               !~^^7Y5YJ77?JPGY:                    
          :!7??!^    :57::^:!JYP5:               .:!~!7^^:     .!??7^.     .!JGG^:~^^:.             
        ^YP5J77?5Y:   !?!!:  :7?PG^      :^:   .~J5GGGGG5J!^             .:~^7?BG!PGGPY7:           
       ~B5?::.  ^PY     .     :J?B5    .Y?^:. :?5BY~::^?BB5?!          ^~??PJ!?P#Y^^~7PGJ^          
       5G?~ :!~!?Y^           .J7GG.   ^G?:.:!YGP~      ~BB5?~       ^!JYGB#Y!?PBG.    5P7          
       ?#Y?^..::.     .. :... :??BY     ~Y555P5!.       .GBG??      ~?JGBBY^.??GBG.    ~G7          
        JBP5?7!!!!!777????????!?77~       .::.          JBBG?7     ^J?BBB? .!?5B#5     :G?          
         ^?PGGBGBGGBGBGG#GBBGBPY57?7^.                ^5#BBJJ:     ?7PBBG:!7Y5##G^      !J!^.       
            :^~!!77777777?YY5PB##GGJ?J^             :JB#BPJ?:      ?7GBBP!55B##P^         ..        
                        :YBG!77?G#BBG7J7          ^YB#BGYJ!.   :~?!?7GBBB!G#BP7.                    
                       7B#P?J!. :PBBBG??7      .!5B#BGJJ!:  ^?5GB#J7?PBBBY7J~.                      
                      ?#BG?J!    ^BBBBG?J~   :?G##BGJJ!^ .7PB#BBB#J7?5BBBB~                         
                     ~BBBY7?.     5BBB#Y?J..?G#BBGYJ7^ .?G#BBBBGY5!775BBB#J                         
                     J#BB7J7      Y#BBBB!J~J#BBB5J?~. ^P#BBBBPJJ!~.7?5BBBBP                         
                     ?#BBP!J^     Y#BBBBJ?!?#BBP7?:  !BBBBBB?J!:   ?7PBBBB5                         
                     :GBBBJJ?^    5BBBBB?J7!#B5?J.  ^BBBBBBY?~    ^J?BBBB#?                                            
                     

## What is this?

T.O.C is an automated tool for open source investigation. It uses 4 other tools/sources and fuses them in one command-line script. It runs the 4 tools consecutively on a list of domain and outputs the result to a separate file for each domain and tool.

## What does it do and how does it do it ?

T.O.C takes a texte file as input and iniate 4 scans from 4 different tools on each of the domain listed.

The functions pertinent to the scan are as follows:

|Function's name|Role|
|---------------|----|
|`run_theHarvester()`|Initiate a theHarvester scan on each of the domain using the --source argument as the source|
|`run_dnscan()`|Initiate a dsncan scan on each of the domain|
