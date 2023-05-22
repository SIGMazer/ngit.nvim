import typing
import os
from git.repo import Repo
import subprocess
class Git(object):
    def __init__(self) -> None:
        try:
            self.path= Repo(search_parent_directories=True)
            self.git = Repo(self.path.git.rev_parse("--show-toplevel"))
        except:
            exit(0)

    def status(self) -> typing.List[typing.List[typing.Any]]:
        untracked_files = self.git.git.status(short=True)
        staging_files = self.git.index.diff("HEAD")
        return [untracked_files.split('\n'), staging_files]

    def current_branch(self) -> str :
        return self.git.active_branch.name

    def git_add(self, file, all:bool) -> None :
        if not os.path.exists(file):
            subprocess.run(['git','add',file])
        if all:
            a, s = self.status()
            for i in a :
                if not os.path.exists(i):
                    subprocess.run(['git','add',i[3:]])
                    continue
                self.git.index.add(i[3:])
            return
        self.git.index.add(file)

    
    def resotre(self, file, all:bool) -> None :
        if all:
            subprocess.run(['git','restore','--staged',self.path.git.rev_parse("--show-toplevel")])
            return
        subprocess.run(['git','restore','--staged',file])
