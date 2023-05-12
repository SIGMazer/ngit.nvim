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

        self.vim.command('sp')
        self.vim.command('enew')
        self.vim.current.buffer[:] = result.stdout.splitlines()


        # Prevent editing in the buffer
        self.vim.command('setlocal readonly')
        self.vim.command('setlocal nomodifiable')


        # Jump to the first line of the buffer
        self.vim.command('normal gg')

        # Map 'a' key to return the current line content and perform git add
        self.vim.command("nnoremap <buffer> a :call AutoGitAddLine()<CR>")

    @neovim.function('AutoGitAddLine')
    def add_line(self, args):
        line_number = self.vim.current.window.cursor[0]
        line_content = self.vim.current.buffer[line_number - 1][3:]
        subprocess.run(['git', 'add', line_content])

        self.vim.command('echo "Added file: {}"'.format(line_content))
        self.vim.command('setlocal modifiable')
        result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
        self.vim.current.buffer[:] = result.stdout.splitlines()

        self.vim.command('setlocal nomodifiable')
