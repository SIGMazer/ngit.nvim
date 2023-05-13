# nvim-auto-git
Neovim plugin that make using git with neovim easer 
## Installation 

Use [packer](https://github.com/wbthomason/packer.nvim) to quick install.
Add to `packer.lua`:
```
    use {
        'SIGMazer/nvim-auto-git',
        run='bash ~/.local/share/nvim/site/pack/packer/start/nvim-auto-git/setup.sh', // repo path 
        post_install = {'UpdateRemotePlugins'}
    }
```
and restart nvim 

Or install it manually
```
git clone https://github.com/SIGMazer/nvim-auto-git.git
cd nvim-auto-git
./setup.sh
```
Use `:UpdateRemotePlugins` to update packeges and restart nvim 

## TO DO
- [x] add 
- [x] commit
- [x] push
- [x] pull
- [x] restore
- [ ] merge
- [ ] diff 
- [ ] branchs (add, switch) 
- [ ] log
- [ ] reset 

## License 
[MIT License](https://github.com/SIGMazer/nvim-auto-git/blob/main/LICENSE)
