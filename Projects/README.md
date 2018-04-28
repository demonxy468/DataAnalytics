# Analytics
Data Analytics

#Creating a new branch:
git checkout -b 'branch-name'

#adding files/folders to commit:
git add folder-name/*

#commit the changes: 
git commit -m "message to comment on the commit"

#push to remote:
git push origin branch-name

#checkout master:
git checkout master
git pull origin master

#Process of merging branches:
git checkout master
git pull origin master
git merge test
git push origin master

#delete the branch:
git branch -D branch-name 
