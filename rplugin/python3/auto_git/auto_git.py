import re
import neovim
import subprocess
from pynvim import Nvim

from git.repo import Repo

from auto_git.Git import Git


@neovim.plugin
class AutoGit(object):
    def __init__(self, vim: Nvim):
        self.vim = vim 
        self.git = Git()
        self.branchs: str = ''
        self.buffer_status = """
Help

Branchs -> ({})
{}
Untracked files
{}

Staging files
{}

Ready to push
{}
"""

    def window(self,buf) -> None:
        width = 100 
        height = 30 

        win = self.vim.api.open_win(buf, True, {
            'relative': 'win',
            'width': width,
            'height': height,
            'col': int((self.vim.current.window.width - width) / 2),
            'row': int((self.vim.current.window.height - height) / 2),
            'border': 'rounded',
            'style': 'minimal',
        })
        
        
        self.vim.command('set filetype=git')

        # Prevent editing in the buffer
        self.vim.command('setlocal nomodifiable')
        


    @neovim.command('AutoGit', nargs='*', range='', sync=True)
    def auto_git(self, args, range):
        # Run git status command
        untracked_files, staging_files= self.git.status() 
        current_branch = self.git.current_branch() 
        unpushed = self.git.unpushed()
        content = self.buffer_status.format(current_branch,self.branchs, "\n".join(untracked_files), '\n'.join(staging_files), unpushed).strip().splitlines()

        buf = self.vim.api.create_buf(False, True)

        self.vim.api.buf_set_lines(buf, 0, -1, False, content)

        self.window(buf)
        self.update(0)
        
        # Jump to the first line of files

        # Map 'a' key to return the current line content and perform git add
        self.vim.command("nnoremap <buffer> a :call AutoGitControle()<CR>")
        self.vim.command("nnoremap <buffer> c :call AutoGitCommit()<CR>")
        self.vim.command("nnoremap <buffer> m :call AutoGitMerge()<CR>")
        self.vim.command("nnoremap <buffer> p :call AutoGitPull()<CR>")
        self.vim.command("nnoremap <buffer> b :call AutoGitMakeBranch() <CR>")
        self.vim.command("nnoremap <buffer> d :call AutoGitDeleteBranch() <CR>")
        self.vim.command("nnoremap <buffer> q :q! <CR>")


            
    @neovim.function('AutoGitMerge')
    def merge(self, args):
        line_number = self.vim.current.window.cursor[0]
        line_content = self.vim.current.buffer[line_number - 1][2:]
        valid_branchs = [b.replace(' ','') for b in self.branchs.split('\n') if 'remotes/origin' not in b ] 
        if line_content in valid_branchs[:-1]:
            check =self.vim.call('input', f'Merge {line_content} -> {self.git.current_branch()}? (y/n)')
            if  check == 'y' or check == 'yes':
                out =self.git.merge(line_content)
                self.vim.command(f'echo "{out}"')
            else:
                self.vim.command(f'echo "Abort merging"')
        else:
            self.vim.command('echo ""')
        self.update(0)

    @neovim.function('AutoGitDeleteBranch')
    def delete_branch(self, args):
        line_number = self.vim.current.window.cursor[0]
        line_content = self.vim.current.buffer[line_number - 1][2:]
        msg= f"Delete remote branch {line_content[15:]}? (y/n)" if 'remotes/origin' in line_content else f'Delete branch {line_content}? (y/n)'
        valid_branchs = self.branchs.split('\n')
        if line_content in valid_branchs[:-1] :
            check = self.vim.call('input', msg)
            if check == 'y' or check == 'yes':
                out = self.git.delete_branch(line_content)
                self.vim.command(f'echo "{out}"')
        else:
            self.vim.command(f'echo ""')
        self.update(0)

        
       
    def switch(self, branch: str):
        out = self.git.switch(branch).replace('\n','')     
        self.vim.command('silent update')
        self.vim.command(f'echo "{out}"')
        self.vim.command('silent !git checkout #')

    @neovim.function('AutoGitMakeBranch')
    def make_branch(self, args):
        branch_name=self.vim.call('input', 'Enter branch name: ')
        out = self.git.make_branch(branch_name)
        self.vim.command(f'echo "{out}"')
        self.update(0)
        

    @neovim.function('AutoGitCommit')
    def commit(self, args):
        commit_message = self.vim.call('input', 'Enter commit message: ')
        self.git.commit(commit_message)

        self.vim.command('echo "committed with message: {}"'.format(commit_message))

        self.update(0)


    @neovim.function('AutoGitControle',sync=True)
    def contorle(self, args):
        self.vim.command('echo ""')
        untracked_files, staging_files= self.git.status() 
        line_number = self.vim.current.window.cursor[0]
        line_content = self.vim.current.buffer[line_number - 1]
        valid_branchs = [b.replace(' ','') for b in self.branchs.split('\n') if 'remotes/origin' not in b ] 
        match = re.fullmatch(self.git.hash_regex, line_content) 
        if line_content == '':
            return
        if line_content == 'Untracked files':
            self.git.git_add(line_content,True)
            self.update(0)
            return
        if line_content == 'Staging files':
            self.git.resotre(line_content, True)
            self.update(0)

        if line_content in staging_files:
            self.git.resotre(line_content, False)

        if match is not None:
            result = self.git.push()
            self.vim.command(f'echo "{result}"')
            self.update(0)
            return
        if "branchs" in line_content:
            self.branchs = self.git.branchs() if not self.branchs else '' 
            self.update(0)
        if line_content[2:] in valid_branchs:
            self.switch(line_content[2:])
            self.update(0)
        
        line_content = self.vim.current.buffer[line_number - 1][3:]
        line_content = line_content.replace('"',r"").replace(' ',r'\ ')
        files = [files[3:] for files in untracked_files] 
        if line_content in files:
            self.git.git_add(line_content,False) 

        self.update(0)
   

    @neovim.function('AutoGitUpdate')
    def update(self,buf):
        

        self.vim.command('setlocal modifiable')
        if buf == 0:
            untracked_files, staging_files= self.git.status() 
            current_branch = self.git.current_branch() 
            unpushed = self.git.unpushed()
            self.branchs = self.git.branchs() if self.branchs else ""
            content = self.buffer_status.format(current_branch,self.branchs , "\n".join(untracked_files), '\n'.join(staging_files), unpushed).strip().splitlines()

            self.vim.current.buffer[:] = content 
        
        self.vim.command('setlocal nomodifiable')
   
    
    @neovim.function('AutoGitPull')
    def pull(self,args):

        result =self.git.pull()

        if len(result.stderr) > 0:
            self.vim.command('echo "{}"'.format(result.stderr))
        else: 
            self.vim.command('echo "{}"'.format(result.stdout))
        self.update(0)
