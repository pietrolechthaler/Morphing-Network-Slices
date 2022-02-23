# Morphing Network Slicing

Authors: 
Ascari Giacomo,
Gatti Matteo,
Lechthaler Pietro

## CONTENUTI:

### Controller-redirect
morphing da stringa ad anello utilizzando il controller per il redirect delle porte, una volta raggiunto l'ultimo switch i messaggi venogno poi inviati al primo per ricominciare il giro, emulando quindi a tutti gli effetti una topologia ad anello pur avendo una topologia fisica sottostante a stringa

```
sudo python3 ./main.py
```

Viene avviato prima il controller "standard" per gestire la topologia a stringa, poi tramite ``` exit ``` usciamo da mininet e viene avviata la seconda situazione con il controller che gestisce l'anello. La topologia sottostante è invariata


### Routing-tables solution
morphing eseguito da un controller "ad hoc" e non da RYU, permette di fare morphing tra le topologie "string", "circle" e "star" a piacimento, utilizzandone una come topologia fisica e poi scegliendo quella logica.. soluzione basata sulla modifica delle tabelle di routing per instradamento dei pacchetti, da parte di "NetContoller" "TopoController" e "slicController" classi python da noi predisposte

```
sudo python3 ./main.py
```
