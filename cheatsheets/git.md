# Help 
* `git help <příkaz>`
* http://ohshitgit.com/

# Global config (git config --list)
* `git config --global user.name "Name surname"`
* `git config --global user.email example@example.com`
* `git config --global core.editor vim`
* `git config --global merge.tool vimdiff`

--------------------------------------------------------------------------------

# Cloning
* `git clone git://github.com/miso-belica/sumy.git [<vlastný_názov>]`

# Add file
* `git add <cesta_k_súboru>`

# Committing
* `git commit -m <správa>`
* `git commit -v # zobrazí diff súborov, kt sa commitujú`
* `git commit -a -m <správa> # zahrnutie všetkých zmenených sledovaných súborov`
* `git commit --amend # zmena poslednej zapísanej revízie`

# Removing files
* `git rm <súbor>`
* `git rm -f <súbor> # odstránenie ak je <súbor> "staged"`
* `git rm --cached <súbor> # odstránenie zo sledovania zmien ale ponechanie na disku`
* `git rm log/\*.log # git robí vlastné nahradzovanie wildcards preto "\" aby to nebolo interpretované už shellom`

# Move file
* `git mv <súbor> <nová_cesta_alebo_názov>`

--------------------------------------------------------------------------------

# Show diff
* `git diff`
* `git diff --staged`
* `git diff --color-words # vysvieti konkrétne zmeny na riadkoch (dobré pre LaTeX)`

# History
* `git log`
* `git log <branch>..<branch> # zoznam zmien medzi vetvami`
* `git log -p # výpis logov s diffom pre každú revíziu`
* `git log -n # kde "n" je číslo # výpis len "n" posledných revízií`
* `git log --stat # stručné info (commit správa + počet zmien v súboroch)`
* `git log --pretty=oneline|short|full|fuller|format:"<formát>"`
* `git log --pretty=format:"%h %s" --graph # história ako graf`
* `git log --since=2.weeks [--until=<dátum>]`
* `git log --author=<autor> # hľadá v histórii podľa autora`
* `git log --grep=<kl_slovo>`
* `git log --author=<autor> --grep=<kl_slovo> # hladá autora alebo slovo`
* `git log --author=<autor> --grep=<kl_slovo> --all-match # hladá autora aj slovo zároveň`
* `git log -# <názov_súboru_alebo_adresára> # revízie len pre urč. súbory`

--------------------------------------------------------------------------------

# Remote repos
* `git remote # zobrazí zoznam vzd. repozitárov`
* `git remote -v # zobrazí zoznam vzd. repozitárov s URL adresami`
* `git remote show <názov_vzd_repa> # info o vzd. repu`

# Update remote repo
* `git remote add <zkrátený_názov> <url> # pridanie`
* `git remote rename <zkrátený_názov> <nový_skrátený_názov> # premenovanie názvo vzd. repa`
* `git remote rm <zkrátený_názov> # zmazanie vzd. repa`
* `git remote prune <remote_name> # zmazanie referencií na neexistujúce vetvy na <remote_name>`

# Fetch changes from remote repo
* `git fetch <názov_vzdialeného_repozitára> # stiahne nové info ale nezačlení ho do repozirára`
* `git pull # automaticky vyzdvihne a začlení (merge) dáta z 'origin'`
* `git pull --rebase # automaticky vyzdvihne a začlení (rebase) dáta z 'origin'`
* https://github.com/aanand/git-up

# Send changes to remote repo
* `git push <názov_vzd_repa> <názov_vetvy>`
* `git push origin master # najčastejší príkaz`
* `git push # alias k "git push origin master"`
* `git push --force # vynútené zaslanie do repa (prepísanie histórie na serveri, ...)`

--------------------------------------------------------------------------------

# Tags
* `git tag # výpis značiek`
* `git tag -l <maska_s_*_ako_patternom> # hľadanie značiek podľa názvu (git tag -l 'v1.4.2.*')`
* `git push origin <názov_značky> # pošle značku na vzd. server`
* `git push origin --tags # pošle všetky značky, kt. tam nie sú na vzd. server`
* `git tag -d <názov_značky> # zmaže tag na lokále`
* `git push origin :refs/tags/<názov_značky> # zmaže tag na vzdialenom serveri`

# Annotated tags
* `git tag -a <značka> -m <správa> # pridá anotovanú značku so správou`
* `git tag -a <značka> <crc_revízie> # pridá anotovanú značku ku konkrétnej revízii`
* `git tag -s <značka> -m <správa> # pridá anotovanú značku so správou podpísanú GPG kľúčom`
* `git tag -v <značka> -m <správa> # overí podpísanú značku pomocou verejného GPG kľúča`
* `git show <značka> # zobrazí informácie o značke (autor, dátum, správa, commit hash, ...)`

# Add tags
* `git tag <značka> # vloží prostú značku`
* `git show <značka> # zobrazí označkovanú revíziu`

--------------------------------------------------------------------------------

# Aliases
* `git config --global alias.ci commit # pridá alias "git ci"`
* `git config --global alias.unstage 'reset HEAD --' # git unstage <súbor>`
* `git config --global alias.last 'log -1 HEAD' # git last # posledný commit`
* `git config --global alias.visual "!gitk" # git visual -> gitk`

--------------------------------------------------------------------------------

# Branches
* `git branch # výpis vetiev`
* `git branch -v # výpis poslednej revízie na každej vetve`
* `git branch --merged # zobrazí vetvy začlenené do súčasnej vetvy`
* `git branch --no-merged # zobrazí vetvy nezačlenené do súčasnej vetvy`
* `git branch <názov_vetvy> # vytvorí novú vetvu`
* `git checkout <názov_vetvy> # prepne sa na danú vetvu`
* `git checkout -b <názov_vetvy> # vytvorí a prepne sa do vetvy v 1 kroku`
* `git branch -d <názov_vetvy> # zmaže danú vetvu`

# Merge branches
* `git checkout <vetva_do_ktorej_chceme_začleniť_inú>`
* `git merge <vetva_ktorú_chceme_začleniť_do_tej_v_ktorej_sa_teraz_nachádzame>`

# Conflicts
* `git add <názov_súboru> # označí súbor ako s vyriešenými konfliktami`
* `git mergetool # grafický nástroj na prevedenie konfliktami`
* `git commit # dokončí zlúčenie`

# Remote branches
* `git fetch origin # aktualizuje vetvu "origin/master"`
* `git push <server> <vetva> # pošle vetvu na vzd. server`
* `git push <server> <vetva>:<vzdialená_vetva> # pošle vetvu <vetva> na vzd. server ako vetvu <vzdialená_vetva>`
* `git merge <server>/<vetva> # začlení vzd. vetvu do aktuálnej lokálnej`
* `git branch -t <vetva> <server>/<vetva> # vytvorí lokálnu vetvu podľa vzdialenej`
* `git checkout --track <server>/<vetva> # ako "git branch -b <vetva> <server>/<vetva>"`
* `git push <server> :<vzdialená_vetva> # zmazanie vzdialenej vetvy`

# Rebasing
* `git rebase <vetva> # preskladá aktuálnu vetvu do vetvy <vetva>`
  on client branch $ git rebase --onto master server client # zober záplaty od spoločného rodiča vetiev server a client po vetve client a aplikuj ich na master
* `git rebase <základňa> <tématická_vetva> # preskladá zmeny <tématickej_vetvy> do <základne>`

# Rebasing (typical use):
* `git rebase master <branch> # preskladaj <branch> do master vetvy`
* `git checkout master # prepni sa do master vetvy`
* `git merge <branch> # začlen "rýchlo vpred" <branch> do vetvy master`
* `git branch -d <branch> # zmaž nepotrebnú vetvu <branch>`

# Delete unverzed files
* `git clean -id <cesta_k_adresárom_alebo_súborom>...`
