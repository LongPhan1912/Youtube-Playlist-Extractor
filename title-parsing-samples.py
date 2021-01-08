from youtube_title_parse import get_artist_title
# https://github.com/lttkgp/youtube_title_parse

# just a small test to see the outputs of the youtube_title_parse api
# there's a heuristic in how the artist and song name are detected, but overall pretty good

full = '''The Golden Girls Theme Song Extended
Andrew Gold - Thank You For Being A Friend (Official Music Video)
BIG CHUNGUS | Official Main Theme | Song by Endigo
Kygo, Donna Summer - Hot Stuff (Official Video)
MAX - Lights Down Low feat. gnash (Official Video)
MAX, Felly - Acid Dreams (Official Video)
MAX - Love Me Less (feat. Quinn XCII) (Official Video)
MAX - Working For The Weekend (feat. bbno$) [prod. AJR] Official Video
MAX - Blueberry Eyes (feat. SUGA of BTS) [Official Music Video]
Miley Cyrus - my future (Billie Eilish cover) in the Live Lounge
Palace - Heaven Up There
Chamber Of Reflection
Prince   The Beautiful Ones   Uncut Version
Arctic Monkeys - Four Out Of Five (Official Video)
Can't Help Falling In Love on a Kalimba
Childish Gambino - 12.38 (Audio) ft. 21 Savage, Ink, Kadhja Bonet
Calvin Harris, The Weeknd - Over Now (Official Video)
[Study Sleep Relax 💖] Meditation - Monoman .beautiful comment section peaceful relaxing soothing
There You Are
Star Wars Cantina Band w/ Maple on the Drums
I love it when you call me Señorita - Lukas Arnold Impressions
thank u, next - Ariana Grande - FUNK cover feat. Rozzi!!
The Neighbourhood - Cherry Flavoured (Official Video)
Kanye West - "Ghost Town" but you're in church
MAC DEMARCO - HAVE YOURSELF A MERRY LITTLE CHRISTMAS
Jack Harlow - Way Out feat. Big Sean [Official Video]
Time Inversion | Tenet
Paramore - Decode but it's lofi hip hop
Blinding Lights (Medieval Style)
In The Morning Official Video - J. Cole Feat. Drake
Eat Them Apples
Tame Impala - Breathe Deeper
JAY-Z - Change Clothes ft. Pharrell
AC/DC - Demon Fire (Official Video)
Love Again
SZA - Together (feat. Tame Impala)
Conan & The Basic Cable Band Perform "Run Run Rudolph"
Forever Man by Eric Clapton
Edge of Desire
Janis Ian - At Seventeen (Audio)
Afterthought
the office theme song but it's lofi & sad
Short Change Hero
Joji - NITROUS
Miley Cyrus - Hate Me (Audio)
Miley Cyrus - High (Audio)
Teddy Swims - Blinding Lights (The Weeknd Cover)
Miley Cyrus - Angels Like You (Audio)
Miley Cyrus - Night Crawling (Audio) ft. Billy Idol
Labrinth feat. Emeli Sandé - Beneath Your Beautiful Cover (Liz Gillies & Max Schneider (MAX))
Cheryl Lynn - Got To Be Real (Audio)
Huey Lewis And The News - If This Is It (Official Music Video)
Sultans of Swing // DIRE STRAITS Acoustic Cover
Michael Jackson and Eddie Murphy "What's Up WIth You ?"
SEPTEMBER by EARTH, WIND & FIRE | Fabulous Fabio Cover
Mild Orange - Foreplay [Full Album]
George Benson - Give Me The Night (Official Music Video)'''

list = full.split('\n')

for item in list:
    a = get_artist_title(item)
    print(a)
