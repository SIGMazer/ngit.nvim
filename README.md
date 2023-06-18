# nvim-auto-git
Neovim plugin that make using git with neovim easer 

## ScreenShot
<details>
      <summary>Git Status</summary>
<img src="https://github.com/SIGMazer/nvim-auto-git/assets/88988252/bcba7a99-332c-4fe8-abe5-bb55b232439b" alt="Alt text" title="Optional title">
Press the letter in help to execute the command 
Ex. 
    if press `a`  when cursor at the same line with `a.txt` it will add it to staging 
</details>
<details>
      <summary>Git Branch</summary>
<img src="https://github.com/SIGMazer/nvim-auto-git/assets/88988252/88a5bfb6-ec9c-445e-95b2-4b3a2ee47693" alt="Alt text" title="Optional title">
</details>


## Installation 

Use [packer](https://github.com/wbthomason/packer.nvim) to quick install.
Add to `packer.lua`:
```
    use {
        'SIGMazer/ngit.nvim',
        post_install = {'UpdateRemotePlugins'}
    }
```
and restart nvim 


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
- [x] merge
- [ ] stash
- [ ] diff 
- [x] branchs (add, switch, delete) 
- [ ] log
- [ ] reset 

## License 
[MIT License](https://github.com/SIGMazer/nvim-auto-git/blob/main/LICENSE)
