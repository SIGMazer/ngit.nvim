syntax match AutoGitHeader /^[A-Z][a-z][^:]*/ 

syntax match CommitHash /^[0-9a-f][^:]*/

highlight def link AutoGitHeader @keyword 
highlight def link CommitHash @annotation
