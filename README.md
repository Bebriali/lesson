# lesson
repository for scripts from lesson
trying to do the exercises

### how to make ssh-key

enter command:
ssh-keygen -t ed25519 -C "name.surname@phystech.edu"

## add keys in ssh-agency
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

## to clone repository
git clone git@github.com:username/repository.git 
dgf