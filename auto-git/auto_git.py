from abc import update_abstractmethods
import neovim 
import subprocess



@neovim.plugin
class AutoGitPlugin(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.command('AutoGit', nargs='*', range='')
    def auto_git(self, args, range):
        # Run git status command
        result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
        current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)

        self.vim.command('sp')
        self.vim.command('enew')
        
        buffer_view = f"""
help

add : a
restore : r
commit : c
push : p
pull : u
exit : :q!

Current branch = {current_branch.stdout.strip()}

file status

{result.stdout}
"""

        self.vim.current.buffer[:] = buffer_view.strip().splitlines()

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
   
    @neovim.function('AutoGitCommit')
    def commit(self, args):
        commit_message = self.vim.call('input', 'Enter commit message: ')
        subprocess.run(['git', 'commit', '-m', commit_message])

        self.vim.command('echo "Committed with message: {}"'.format(commit_message))

        self.update()


    @neovim.function('AutoGitAdd')
    def add(self, args):
        line_number = self.vim.current.window.cursor[0]
        if line_number < 14:
            self.vim.command('echo "Invalid select "')
            return
        
        line_content = self.vim.current.buffer[line_number - 1][3:]
        subprocess.run(['git', 'add', line_content])

        self.vim.command('echo "Added file: {}"'.format(line_content))
    
        self.update()

   
    @neovim.function('AutoGitRestore')
    def restore(self, args):
        line_number = self.vim.current.window.cursor[0]
        if line_number < 14:
            self.vim.command('echo "Invalid select "')
            return
        
        line_content = self.vim.current.buffer[line_number - 1][3:]
        subprocess.run(['git', 'restore','--staged', line_content])

        self.vim.command('echo "Restored file: {}"'.format(line_content))
        
        self.update()


    @neovim.function('AutoGitUpdate')
    def update(self):
        
        self.vim.command('setlocal modifiable')
        result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
        current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
      

        buffer_view = """
help

add : a
restore : r
commit : c
push : p
pull : u
exit : :q!

Current branch = {}

file status

{}
""".format(current_branch.stdout.strip(),result.stdout)

        self.vim.current.buffer[:] = buffer_view.strip().splitlines()

        self.vim.command('setlocal nomodifiable')
   
    

    @neovim.function('AutoGitPush')
    def push(self, args):
        subprocess.run(['git', 'push'])

        self.vim.command('echo "Pushed changes"')

        self.update()
    

    @neovim.function('AutoGitPull')
    def pull(self, args):
        subprocess.run(['git', 'pull'])

        self.vim.command('echo "Pulled changes"')

        self.update()
