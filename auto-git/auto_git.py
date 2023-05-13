import neovim 
import subprocess



@neovim.plugin
class AutoGitPlugin(object):
    def __init__(self, vim):
        self.vim = vim

        self.buffer_status = """
help

add : a
restore form staging : r
commit : c
push : p
pull : u
exit : q

Current branch = {}

file status

{}
"""
        self.buffer_branch="""
help

switch : i
merge : m
delete branch : d
make branch : a
exit : q

Current branch = {}

Branchs

{}
"""

    @neovim.command('AutoGit', nargs='*', range='')
    def auto_git(self, args, range):
        # Run git status command
        result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
        current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)

        self.vim.command('sp')
        self.vim.command('enew')
        
        self.vim.current.buffer[:] = self.buffer_status.format(current_branch.stdout.strip(), result.stdout).strip().splitlines()

        # Prevent editing in the buffer
        self.vim.command('setlocal nomodifiable')


        # Jump to the first line of the buffer
        self.vim.command('normal gg')

        # Map 'a' key to return the current line content and perform git add
        self.vim.command("nnoremap <buffer> a :call AutoGitAdd()<CR>")
        self.vim.command("nnoremap <buffer> r :call AutoGitRestore()<CR>")
        self.vim.command("nnoremap <buffer> c :call AutoGitCommit()<CR>")
        self.vim.command("nnoremap <buffer> p :call AutoGitPush()<CR>")  
        self.vim.command("nnoremap <buffer> u :call AutoGitPull()<CR>")
        self.vim.command("nnoremap <buffer> q :q! <CR>")
   
    @neovim.command('AutoGitBranch', nargs='*', range='')
    def branchs(self, args, range):
    

        result = subprocess.run(['git', 'branch','-a'], capture_output=True, text=True)
        current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
        result.stdout = result.stdout.replace('*',' ')
        
        self.vim.command('sp')
        self.vim.command('enew')
        
        self.vim.current.buffer[:] = self.buffer_branch.format(current_branch.stdout.strip(), result.stdout).strip().splitlines()

        # Prevent editing in the buffer
        self.vim.command('setlocal nomodifiable')


        # Jump to the first line of the buffer
        self.vim.command('normal gg')
        
        self.vim.command("nnoremap <buffer> q :q! <CR>")
        self.vim.command("nnoremap <buffer> i :call AutoGitSwitch() <CR>")
        self.vim.command("nnoremap <buffer> a :call AutoGitMakeBranch() <CR>")
        self.vim.command("nnoremap <buffer> d :call AutoGitDeleteBranch() <CR>")
        self.vim.command("nnoremap <buffer> m :call AutoGitMerge() <CR>")

    @neovim.function('AutoGitMerge')
    def merge(self, args):
        line_number = self.vim.current.window.cursor[0]
        if line_number < 13:
            self.vim.command('echo "Invalid select "')
            return
        line_content = self.vim.current.buffer[line_number - 1][2:]
        
        result = subprocess.run(['git', 'merge',line_content], capture_output=True, text=True)
        if len(result.stderr) > 0:
            self.vim.command('echo "{}"'.format(result.stderr))
        else:
            self.vim.command('echo "Branch was merged"')
        self.update(1)

    @neovim.function('AutoGitDeleteBranch')
    def delete_branch(self, args):
        line_number = self.vim.current.window.cursor[0]
        if line_number < 13:
            self.vim.command('echo "Invalid select "')
            return
        line_content = self.vim.current.buffer[line_number - 1][2:]

        if line_content[:15] == 'remotes/origin/':
            result = subprocess.run(['git', 'push','origin','--delete', line_content[15:]], capture_output=True, text=True)
            if len(result.stderr) > 0:
                self.vim.command('echo "{}"'.format(result.stderr))
            else:
                self.vim.command('echo "{}"'.format(result.stdout))
            self.update(1)
            return

        result = subprocess.run(['git', 'branch','-D', line_content], capture_output=True, text=True)
        if len(result.stderr) > 0:
            self.vim.command('echo "{}"'.format(result.stderr))
        else:
            self.vim.command('echo "{}"'.format(result.stdout))
        self.update(1)
        
       
    @neovim.function('AutoGitSwitch')
    def switch(self, args):
        line_number = self.vim.current.window.cursor[0]
        if line_number < 13:
            self.vim.command('echo "Invalid select "')
            return
        line_content = self.vim.current.buffer[line_number - 1][2:]

        if line_content[:15] == 'remotes/origin/':
            self.vim.command('echo "Invalid select "')
            return
       
        result = subprocess.run(['git', 'switch', line_content], capture_output=True, text=True)
        
        if len(result.stderr) > 0:
            self.vim.command('echo "{}"'.format(result.stderr[:-1]))
        self.update(1)

    @neovim.function('AutoGitMakeBranch')
    def make_branch(self, args):
        branch_name=self.vim.call('input', 'Enter branch name: ')
        result = subprocess.run(['git', 'branch',branch_name], capture_output=True, text=True)

        if len(result.stderr) > 0:
            self.vim.command('echo "{}"'.format(result.stderr))
        else:
            self.vim.command('echo "Branch was created "')
        self.update(1)


    @neovim.function('AutoGitCommit')
    def commit(self, args):
        commit_message = self.vim.call('input', 'Enter commit message: ')
        subprocess.run(['git', 'commit', '-m', commit_message])

        self.vim.command('echo "Committed with message: {}"'.format(commit_message))

        self.update(0)


    @neovim.function('AutoGitAdd')
    def add(self, args):
        line_number = self.vim.current.window.cursor[0]
        if line_number < 14:
            self.vim.command('echo "Invalid select "')
            return
        
        line_content = self.vim.current.buffer[line_number - 1][3:]
        subprocess.run(['git', 'add', line_content])

        self.vim.command('echo "Added file: {}"'.format(line_content))
    
        self.update(0)

   
    @neovim.function('AutoGitRestore')
    def restore(self, args):
        line_number = self.vim.current.window.cursor[0]
        if line_number < 14:
            self.vim.command('echo "Invalid select "')
            return
        
        line_content = self.vim.current.buffer[line_number - 1][3:]
        subprocess.run(['git', 'restore','--staged', line_content])

        self.vim.command('echo "Restored file: {}"'.format(line_content))
        
        self.update(0)


    @neovim.function('AutoGitUpdate')
    def update(self,buf):
        
        self.vim.command('setlocal modifiable')
        if buf == 0:
            result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
            current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
            self.vim.current.buffer[:] = self.buffer_status.format(current_branch.stdout.strip(), result.stdout).strip().splitlines()

        if buf  == 1:
            result = subprocess.run(['git', 'branch','-a'], capture_output=True, text=True)
            current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
            result.stdout = result.stdout.replace('*',' ')
            self.vim.current.buffer[:] = self.buffer_branch.format(current_branch.stdout.strip(), result.stdout).strip().splitlines()
        
        self.vim.command('setlocal nomodifiable')
   
    

    @neovim.function('AutoGitPush')
    def push(self, args):
        current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
        result =  subprocess.run(['git', 'push','-u','origin',current_branch.stdout[:-1]], capture_output=True, text=True)
        if len(result.stderr) > 0:
            self.vim.command('echo "{}"'.format(result.stderr))
        else: 
            self.vim.command('echo "Pushed changes"')

        self.update(0)
    

    @neovim.function('AutoGitPull')
    def pull(self, args):

        result =  subprocess.run(['git', 'pull'], capture_output=True, text=True)
        
        if len(result.stderr) > 0:
            self.vim.command('echo "{}"'.format(result.stderr))
        else: 
            self.vim.command('echo "{}"'.format(result.stdout))


        self.update(0)
