import typing
import re
import os
from git.repo import Repo
import subprocess
import pynvim as vim
class Git(object):
    def __init__(self) -> None:

        self.vim = vim
        try:
            self.path= Repo(search_parent_directories=True).git.rev_parse("--show-toplevel")
            self.git = Repo(self.path)
        except:
            exit(0)

        self.hash_regex = r'\b[0-9a-f]{5,40}\b'
    def status(self) -> typing.List[typing.List[typing.Any]]:
        files = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True).stdout.split('\n')
        untracked_files = [a for a in files  if a != "" and a[1] != ' ' ] 
        staging_files = [a[3:] for a in files if a != "" and a[1] == ' ' ]        
        return [untracked_files , staging_files]
        
    def current_branch(self) -> str :
        return self.git.active_branch.name

    def git_add(self, file, all:bool) -> None :
        if all :
            subprocess.run(["git","add", self.path])

        subprocess.run(["git","add", file])

    
    def resotre(self, file, all:bool) -> None :
        if all:
            subprocess.run(['git','restore','--staged',self.path])
            return
        subprocess.run(['git','restore','--staged',file])
    def commit(self, commit_message):
        subprocess.run(['git', 'commit', '-m', commit_message])

    def unpushed(self):
        cmd = f"git log {self.current_branch()} --oneline"
        log_local = subprocess.run(cmd.split(' '),capture_output=True ,text=True).stdout.split('\n')
        cmd = f"git log origin/{self.current_branch()} --oneline"
        log_remote= subprocess.run(cmd.split(' '),capture_output=True ,text=True).stdout.split('\n')
        hash_local = log_local[0].split(' ')[0] 
        hash_remote= log_remote[0].split(' ')[0]
        if hash_local == hash_remote :
            return ""
        return hash_local
    
    def push(self) -> str :
        cmd = f"git push -u origin {self.unpushed()}:{self.current_branch()}"
        result =  subprocess.run(cmd.split(' '), capture_output=True, text=True)
        return "Pushing {self.unpushed()} to {self.current_branch()}"         
        
    def pull(self):

        return  subprocess.run(['git', 'pull'], capture_output=True, text=True)
        

    def branchs(self) -> str:
        return subprocess.run(['git', 'branch','-a'], capture_output=True, text=True).stdout.replace('*',' ')

    def make_branch(self,name:str) -> str:
        
        branch =subprocess.run(['git', 'branch',name], capture_output=True, text=True)
        return branch.stderr if branch.stderr else f"Create branch {name}"

    def merge(self, branch: str) -> str:
        cmd = f'git merge {branch}'
        out =subprocess.run(cmd.split(' '), capture_output=True, text=True).stderr
        return out if out else f'Merge branch -> {self.current_branch()}'

    def switch(self, branch: str) -> str:
        cmd = f'git switch {branch}'
        out =subprocess.run(cmd.split(' '), capture_output=True, text=True).stderr
        return out if out else f'Switch to {branch}'

    def delete_branch(self, branch: str) -> str:
        if 'remotes/origin' in branch:
            out= subprocess.run(['git', 'push','origin','--delete', branch[15:]], capture_output=True, text=True).stderr
        else :
            out= subprocess.run(['git', 'branch','-D', branch], capture_output=True, text=True).stderr
        return out if out  else f"Branch {branch} was deleted "
            
        
