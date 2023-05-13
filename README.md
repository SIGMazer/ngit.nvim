# nvim-auto-git
Neovim plugin that make using git with neovim easer 

## ScreenShot
<details>
      <summary>Git Status</summary>
<img src="https://github.com/SIGMazer/nvim-auto-git/assets/88988252/b8950455-6d7e-445e-8b9b-1fa7dfd904da" alt="Alt text" title="Optional title">
Press the letter in help to execute the command 
Ex. 
    if press `a`  when cursor at the same line with `a.txt` it will add it to staging 
</details>

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

## Remap
Add to `remap.lua` :
```
vim.keymap.set("n","<leader>gs",'<Cmd>lua vim.cmd(":AutoGit")<CR>')
```

## TO DO
- [x] add 
- [x] commit
- [x] push
- [x] pull
- [x] restore
- [ ] merge
- [ ] stash
- [ ] diff 
- [ ] branchs (add, switch) 
- [ ] log
- [ ] reset 

## License 
[MIT License](https://github.com/SIGMazer/nvim-auto-git/blob/main/LICENSE)
