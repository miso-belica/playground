- pomoc:
  $ git help <příkaz>

- globálna zmena info (git config --list):
  $ git config --global user.name "Michal Belica"
  $ git config --global user.email miso.belica@gmail.com
  $ git config --global core.editor vim
  $ git config --global merge.tool vimdiff

--------------------------------------------------------------------------------

- klonovanie:
  $ git clone git://github.com/miso-belica/sumy.git [<vlastný_názov>]

- pridanie súboru:
  $ git add <cesta_k_súboru>

- commit:
  $ git commit -m <správa>
  $ git commit -v # zobrazí diff súborov, kt sa commitujú
  $ git commit -a -m <správa> # zahrnutie všetkých zmenených sledovaných súborov
  $ git commit --amend # zmena poslednej zapísanej revízie

- zmazanie súboru:
  $ git rm <súbor>
  $ git rm -f <súbor> # odstránenie ak je <súbor> "staged"
  $ git rm --cached <súbor> # odstránenie zo sledovania zmien ale ponechanie na disku
  $ git rm log/\*.log # git robí vlastné nahradzovanie wildcards preto "\" aby to nebolo interpretované už shellom

- premenovanie/presun súboru:
  $ git mv <súbor> <nová_cesta_alebo_názov>

--------------------------------------------------------------------------------

- zobrazenie zmien:
  $ git diff
  $ git diff --staged
  $ git diff --color-words # vysvieti konkrétne zmeny na riadkoch (dobré pre LaTeX)

- história revízií:
  $ git log
  $ git log <branch>..<branch> # zoznam zmien medzi vetvami
  $ git log -p # výpis logov s diffom pre každú revíziu
  $ git log -n # kde "n" je číslo - výpis len "n" posledných revízií
  $ git log --stat # stručné info (commit správa + počet zmien v súboroch)
  $ git log --pretty=oneline|short|full|fuller|format:"<formát>"
  $ git log --pretty=format:"%h %s" --graph # história ako graf
  $ git log --since=2.weeks [--until=<dátum>]
  $ git log --author=<autor> # hľadá v histórii podľa autora
  $ git log --grep=<kl_slovo>
  $ git log --author=<autor> --grep=<kl_slovo> # hladá autora alebo slovo
  $ git log --author=<autor> --grep=<kl_slovo> --all-match # hladá autora aj slovo zároveň
  $ git log -- <názov_súboru_alebo_adresára> # revízie len pre urč. súbory

--------------------------------------------------------------------------------

- zoznam vzdialených repozitárov:
  $ git remote # zobrazí zoznam vzd. repozitárov
  $ git remote -v # zobrazí zoznam vzd. repozitárov s URL adresami
  $ git remote show <názov_vzd_repa> # info o vzd. repu

- úpravy vzd. repozitára:
  $ git remote add <zkrátený_názov> <url> # pridanie
  $ git remote rename <zkrátený_názov> <nový_skrátený_názov> # premenovanie názvo vzd. repa
  $ git remote rm <zkrátený_názov> # zmazanie vzd. repa
  $ git remote prune <remote_name> # zmazanie referencií na neexistujúce vetvy na <remote_name>

- vyzdvihnutie zmien z repa:
  $ git fetch <názov_vzdialeného_repozitára> # stiahne nové info ale nezačlení ho do repozirára
  $ git pull # automaticky vyzdvihne a začlení (merge) dáta z 'origin'
  $ git pull --rebase # automaticky vyzdvihne a začlení (rebase) dáta z 'origin'
  # https://github.com/aanand/git-up

- odoslanie zmien do vzd. repozitára:
  $ git push <názov_vzd_repa> <názov_vetvy>
  $ git push origin master # najčastejší príkaz
  $ git push # alias k "git push origin master"
  $ git push --force # vynútené zaslanie do repa (prepísanie histórie na serveri, ...)

--------------------------------------------------------------------------------

- značky (tags):
  $ git tag # výpis značiek
  $ git tag -l <maska_s_*_ako_patternom> # hľadanie značiek podľa názvu (git tag -l 'v1.4.2.*')
  $ git push origin <názov_značky> # pošle značku na vzd. server
  $ git push origin --tags # pošle všetky značky, kt. tam nie sú na vzd. server
  $ git tag -d <názov_značky> # zmaže tag na lokále
  $ git push origin :refs/tags/<názov_značky> # zmaže tag na vzdialenom serveri

- anotované značky:
  $ git tag -a <značka> -m <správa> # pridá anotovanú značku so správou
  $ git tag -a <značka> <crc_revízie> # pridá anotovanú značku ku konkrétnej revízii
  $ git tag -s <značka> -m <správa> # pridá anotovanú značku so správou podpísanú GPG kľúčom
  $ git tag -v <značka> -m <správa> # overí podpísanú značku pomocou verejného GPG kľúča
  $ git show <značka> # zobrazí informácie o značke (autor, dátum, správa, commit hash, ...)

- prosté značky:
  $ git tag <značka> # vloží prostú značku
  $ git show <značka> # zobrazí označkovanú revíziu

--------------------------------------------------------------------------------

- aliasy:
  $ git config --global alias.ci commit # pridá alias "git ci"
  $ git config --global alias.unstage 'reset HEAD --' # git unstage <súbor>
  $ git config --global alias.last 'log -1 HEAD' # git last - posledný commit
  $ git config --global alias.visual "!gitk" # git visual -> gitk

--------------------------------------------------------------------------------

- vetvy:
  $ git branch # výpis vetiev
  $ git branch -v # výpis poslednej revízie na každej vetve
  $ git branch --merged # zobrazí vetvy začlenené do súčasnej vetvy
  $ git branch --no-merged # zobrazí vetvy nezačlenené do súčasnej vetvy
  $ git branch <názov_vetvy> # vytvorí novú vetvu
  $ git checkout <názov_vetvy> # prepne sa na danú vetvu
  $ git checkout -b <názov_vetvy> # vytvorí a prepne sa do vetvy v 1 kroku
  $ git branch -d <názov_vetvy> # zmaže danú vetvu

- začleňovanie vetiev:
  $ git checkout <vetva_do_ktorej_chceme_začleniť_inú>
  $ git merge <vetva_ktorú_chceme_začleniť_do_tej_v_ktorej_sa_teraz_nachádzame>

- konflikty:
  $ git add <názov_súboru> # označí súbor ako s vyriešenými konfliktami
  $ git mergetool # grafický nástroj na prevedenie konfliktami
  $ git commit # dokončí zlúčenie

- vzdialené vetvy:
  $ git fetch origin # aktualizuje vetvu "origin/master"
  $ git push <server> <vetva> # pošle vetvu na vzd. server
  $ git push <server> <vetva>:<vzdialená_vetva> # pošle vetvu <vetva> na vzd. server ako vetvu <vzdialená_vetva>
  $ git merge <server>/<vetva> # začlení vzd. vetvu do aktuálnej lokálnej
  $ git branch -t <vetva> <server>/<vetva> # vytvorí lokálnu vetvu podľa vzdialenej
  $ git checkout --track <server>/<vetva> # ako "git branch -b <vetva> <server>/<vetva>"
  $ git push <server> :<vzdialená_vetva> # zmazanie vzdialenej vetvy

- preskladanie (rebase):
  $ git rebase <vetva> # preskladá aktuálnu vetvu do vetvy <vetva>
  on client branch $ git rebase --onto master server client # zober záplaty od spoločného rodiča vetiev server a client po vetve client a aplikuj ich na master
  $ git rebase <základňa> <tématická_vetva> # preskladá zmeny <tématickej_vetvy> do <základne>

- preskladanie (typické použitie):
  $ git rebase master <branch> # preskladaj <branch> do master vetvy
  $ git checkout master # prepni sa do master vetvy
  $ git merge <branch> # začlen "rýchlo vpred" <branch> do vetvy master
  $ git branch -d <branch> # zmaž nepotrebnú vetvu <branch>

- mazanie neverzovaných súborov
  $ git clean -i <cesta_k_adresárom_alebo_súborom>...
