# Obeservation's :
I explore the three ways of how to cloning git repo with token with readonly permission.

First is simply genereate token which have no permisssion.
Second is for the private repos.
Thrid is by organisation repos.

# Token which have no permission :

Step 1: Go to the main settings in that go the developers setting and select the Token generate option.
Step 2: After that write the name of token and do not give any of the permission to this particular token and generate this.
Step 3: After that clone any repo give the token to this after the repo and clone it.
Step 4: Cat any file or folder in repo.
Step 5: Then perform the following commands i.e.

      1. git add .
      2. git commit -m "name"
      3. git push

Step 6: After you apply git push you will see the permission is denied.     

# Private Repos :

step 1: Go to the repo setting then collaboraters setting then select the private repo option and upadate this setting.
step 2: Go to the main setting select develper setting in this and update the token setting.
step 3: Run the command:
            git clone and the url of repo with token.
step 4: after that run this command.

# In private repo we add any user in the repo.

# ORG. Repos :

