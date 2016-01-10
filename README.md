# lessandmore
## Translates a body of text to be less like some things and more like others!

### Screenshots
* Web GUI http://i.imgur.com/fejHEXw.png
* New York Times article with less 'drugs' and more 'candy'! http://i.imgur.com/14kIerg.jpg

### Implementation
Uses word2vec to find analogous words and a layer of basic language processing to repair grammar issues.

language: Python
libraries used: gensim, pattern, Flask, BeautifulSoup

### Notable examples
input: "the Communists ally with the Social-Democrats against the conservative and radical bourgeoisie, reserving, however, the right to take up a critical position in regard to phases and illusions traditionally handed down from the great Revolution' - Communist Manifesto
less: 'communism'
more: 'music'

output: 'the Musicians tune with the Social-Democrats against the conservative and radical musicians, reserving, however, the right to take up a critical position in keyboardist extraordinaire to tunes and tunes traditionally handed down from the great Revolution SuperNOVA"
input: 'I visited the mall'
less: 'normal'
more: 'weird'
output: 'lol visited strange shopping mall'

input: 'Obama is my friend'
less: 'democrat'
more: 'republican'
output: 'McCain seems my pal'
