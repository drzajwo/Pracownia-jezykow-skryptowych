# Space Invaders Lua

Prosta implementacja gry Space Invaders napisana w języku Lua z wykorzystaniem bilbioteki LOVE 2D

### Uruchamianie:
`path/to/love/exe path/to/this/directory`
example:
`/c/Program\ Files/LOVE/love.exe /d/programs/space-invaders`

### Opis
Względem [szablonu](https://github.com/kprzystalski/love2d-space-invader-template) dodani zostali wrogowie, którzy obniżają swoją pozycję oraz strzelają do gracza.  
Wybór przeciwnika który będzie strzelał jest losowy. Dodane zostało sprawdzanie kolizji pocisków przeciwnika na graczu i pocisków gracza na przeciwnikach.  
W przypadku trafienia pocisku gracza w przeciwnika, zostaje on zniszczony, po wyeliminowaniu wszystkich gra jest zakończona sukcesem.  
W przypadku trafienia pocisku przeciwnika w gracza gra zostaje zakończona porażką.  

### Wygląd gry

#### Ekran gry
![Ekran gry](game_screen.png "Ekran gry")

#### Ekran końca gry
![Ekran końca gry](game_over_screen.png "Ekran końca gry")

#### Ekran ukończenia gry
![Ekran ukończenia gry](win_screen.png "Ekran ukończenia gry")


Images:  
https://opengameart.org/content/8-bit-alien-assets  
Sounds:  
https://www.zapsplat.com/sound-effect-category/lasers-and-weapons/  
https://www.jamendo.com/track/271084/zone  
https://freesound.org/people/kyles/sounds/452596/  
https://freesound.org/people/Taira%20Komori/sounds/212757/  
 
