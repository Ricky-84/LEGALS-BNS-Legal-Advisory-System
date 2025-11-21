# Git Guide - Quick Reference

**Purpose:** Understanding Git version control and how to safely manage code changes

---

## 🎯 What is Git?

**Git is like a time machine for your code.**

Every time you make a "commit", Git takes a **snapshot** of your entire project. You can travel back to any snapshot at any time.

Think of commits as **save points in a video game** - you can always load a previous save if something goes wrong.

---

## 📸 Basic Git Concepts

### 1. Repository (Repo)
- Your project folder that Git is tracking
- Contains all your code + a hidden `.git` folder with history

### 2. Commit
- A snapshot of your code at a specific point in time
- Has a unique ID (hash) like `03b2f89`
- Cannot be changed once created (immutable)

### 3. Branch
- A separate timeline of commits
- `main` is usually the primary branch
- You can create branches to experiment without affecting main

### 4. Working Directory
- Your current files (what you see in your folders)
- May have uncommitted changes

### 5. Staging Area (Index)
- Files you've marked to be included in the next commit
- Use `git add` to stage files

---

## 🔄 The Git Workflow

```
Working Directory → Staging Area → Repository (Commit)
     (edit)            (git add)      (git commit)
```

**Example:**
```bash
# 1. Edit a file (Working Directory)
nano myfile.py

# 2. Stage the file (Staging Area)
git add myfile.py

# 3. Commit the file (Repository)
git commit -m "Added new feature to myfile"
```

---

## 📋 Essential Git Commands

### Check Status

```bash
# See what files have changed
git status

# See commit history
git log

# See commit history (one line per commit)
git log --oneline

# See last 10 commits
git log --oneline -10

# See what changed in a file
git diff myfile.py
```

### Making Commits

```bash
# Stage a single file
git add myfile.py

# Stage multiple files
git add file1.py file2.py file3.py

# Stage all changed files
git add .

# Stage all files in a folder
git add data/

# Commit staged files
git commit -m "Your commit message here"

# Stage and commit in one command (only for already-tracked files)
git commit -am "Your commit message"
```

### Good Commit Messages

✅ **Good:**
```bash
git commit -m "Add semantic similarity service for entity extraction"
git commit -m "Fix bug in neo4j_service.py line 234"
git commit -m "Update CSV with enhanced legal elements"
```

❌ **Bad:**
```bash
git commit -m "changes"
git commit -m "fixed stuff"
git commit -m "update"
```

**Format:** Start with a verb (Add, Fix, Update, Remove, Refactor)

---

## ⏪ Going Back in Time (Reverting Changes)

### 1. Discard Uncommitted Changes

```bash
# Discard changes to a specific file (go back to last commit)
git restore myfile.py

# Discard ALL uncommitted changes (CAREFUL!)
git restore .
```

### 2. View Old Commits (Read-Only)

```bash
# See what the code looked like at a previous commit
git checkout 03b2f89

# Look around, read files, test code...
# Nothing you do here affects your main timeline

# Go back to present
git checkout main
```

### 3. Undo Last Commit (Keep Changes)

```bash
# Undo the last commit, but keep the changes as uncommitted files
git reset --soft HEAD~1

# Now you can edit more and make a new commit
```

### 4. Undo Last Commit (Delete Changes)

```bash
# Undo the last commit AND delete all changes (CAREFUL!)
git reset --hard HEAD~1

# This is PERMANENT - your changes are gone!
```

### 5. Undo Multiple Commits

```bash
# Go back 3 commits (keep changes)
git reset --soft HEAD~3

# Go back to specific commit (delete everything after)
git reset --hard 03b2f89
```

### 6. Revert a Commit (Safest Method)

```bash
# Create a NEW commit that undoes a previous commit
git revert 03b2f89

# This is the safest because it doesn't delete history
# Good for commits that have been pushed to remote
```

---

## 🌿 Working with Branches

### Why Use Branches?

- Experiment with new features without breaking main code
- Work on multiple features simultaneously
- Easy to throw away if experiment fails

### Branch Commands

```bash
# See all branches
git branch

# Create a new branch
git branch feature-semantic-similarity

# Switch to a branch
git checkout feature-semantic-similarity

# Create and switch in one command
git checkout -b feature-semantic-similarity

# Switch back to main
git checkout main

# Merge branch into main
git checkout main
git merge feature-semantic-similarity

# Delete a branch
git branch -d feature-semantic-similarity

# Delete a branch (force, even if not merged)
git branch -D feature-semantic-similarity
```

### Recommended Branch Workflow

```bash
# You're on main branch, everything works
git checkout main

# Create branch for Phase 2
git checkout -b phase2-cypher-rules

# Make changes, test, commit
git add .
git commit -m "Phase 2: Implement Cypher graph rules"

# If it works: merge back to main
git checkout main
git merge phase2-cypher-rules

# If it fails: just delete the branch and stay on main
git checkout main
git branch -D phase2-cypher-rules
```

---

## 🔍 Viewing Changes

```bash
# See what changed in working directory (not staged)
git diff

# See what changed in staging area (staged, not committed)
git diff --staged

# See what changed in last commit
git show

# See what changed in a specific commit
git show 03b2f89

# See what changed in a specific file
git log -p myfile.py

# See who changed each line of a file
git blame myfile.py
```

---

## 🌐 Working with Remote (GitHub, GitLab, etc.)

```bash
# See remote repositories
git remote -v

# Add a remote repository
git remote add origin https://github.com/username/repo.git

# Push commits to remote
git push origin main

# Push a branch to remote
git push origin feature-branch

# Pull changes from remote
git pull origin main

# Clone a repository
git clone https://github.com/username/repo.git

# Fetch changes without merging
git fetch origin
```

---

## 👥 Collaborating with Others (IMPORTANT!)

### What Happens When Your Friend Commits?

**Scenario:**
```
Your computer:          Remote (GitHub):       Friend's computer:
main (commit A)         main (commit A)        main (commit A)
                             ↓
                        Friend pushes
                             ↓
                        main (commit B) ←---- main (commit B)
```

**Now:** Remote has commit B, but you still only have commit A!

---

### What You Need to Do

#### Option 1: You Have NO Local Changes (Clean Working Directory)

```bash
# Check if you have uncommitted changes
git status

# If clean (no changes), simply pull
git pull origin main

# Now you have commit B too!
```

**This is the EASY case** - Git just downloads the new commits and updates your code.

---

#### Option 2: You Have Uncommitted Changes

```bash
# You have changes but haven't committed them
git status
# Shows: modified files

# SOLUTION 1: Commit your changes first
git add .
git commit -m "My changes"
git pull origin main

# SOLUTION 2: Stash your changes temporarily
git stash                    # Hide your changes temporarily
git pull origin main         # Get friend's changes
git stash pop                # Bring back your changes
```

---

#### Option 3: You BOTH Made Commits (Most Complex)

**Scenario:**
```
Remote (GitHub):           Your Computer:
commit A                   commit A
   ↓                          ↓
commit B (friend)          commit C (you)
```

You try to push:
```bash
git push origin main
# ERROR! rejected - remote has changes you don't have
```

**Solution:**

```bash
# Step 1: Pull friend's changes
git pull origin main

# Git tries to merge automatically...

# CASE A: No conflicts (you edited different files)
# ✅ Git auto-merges successfully!
# ✅ Creates a merge commit
# ✅ You're done! Now push:
git push origin main

# CASE B: Conflicts (you both edited the same file)
# ❌ Git shows: CONFLICT in file.py
# You must resolve manually...
```

---

### Resolving Merge Conflicts (When You Both Edited Same File)

#### Step 1: Git Shows Conflict

```bash
git pull origin main
# Auto-merging file.py
# CONFLICT (content): Merge conflict in file.py
# Automatic merge failed; fix conflicts and then commit the result.
```

#### Step 2: Open the Conflicted File

Git marks conflicts in the file like this:

```python
def my_function():
<<<<<<< HEAD
    # Your code
    return "Your version"
=======
    # Friend's code
    return "Friend's version"
>>>>>>> origin/main
```

**Meaning:**
- `<<<<<<< HEAD` = Your code (local)
- `=======` = Separator
- `>>>>>>> origin/main` = Friend's code (remote)

#### Step 3: Manually Edit to Resolve

Choose what to keep:

**Option A: Keep your version:**
```python
def my_function():
    # Your code
    return "Your version"
```

**Option B: Keep friend's version:**
```python
def my_function():
    # Friend's code
    return "Friend's version"
```

**Option C: Keep both (merge manually):**
```python
def my_function():
    # Combined code
    result = "Your version"
    result += "Friend's version"
    return result
```

**Remove the conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`)!

#### Step 4: Mark as Resolved

```bash
# After editing the file
git add file.py

# Commit the merge
git commit -m "Resolve merge conflict in file.py"

# Push to remote
git push origin main
```

---

### 🎯 Best Practices for Collaboration

#### 1. Always Pull Before You Start Working

```bash
# Every morning or before starting work
git pull origin main
```

This gets the latest changes from your collaborators.

#### 2. Pull Before You Push

```bash
# Before pushing your commits
git pull origin main    # Get latest changes
git push origin main    # Then push yours
```

#### 3. Commit Frequently

```bash
# Small, frequent commits are easier to merge
git commit -m "Add function X"
git commit -m "Fix bug in Y"
# Better than one huge commit with everything
```

#### 4. Communicate with Your Team

- **Before editing a file:** Tell your friend "I'm working on neo4j_service.py"
- **After pushing:** Let them know "Pushed changes to neo4j_service.py"
- Use branches for big features (explained below)

#### 5. Use Branches for Features (RECOMMENDED!)

```bash
# Instead of both working on main...

# You work on a branch:
git checkout -b your-feature
# Make changes, commit
git push origin your-feature

# Friend works on their branch:
git checkout -b friend-feature
# Make changes, commit
git push origin friend-feature

# Merge to main one at a time (no conflicts!)
git checkout main
git merge your-feature
git merge friend-feature
```

---

### 📋 Daily Collaboration Workflow

#### Morning Routine:

```bash
# 1. Check what you have
git status

# 2. Get latest changes from team
git pull origin main

# 3. Start working
```

#### While Working:

```bash
# Commit frequently (every 30 mins to 1 hour)
git add .
git commit -m "Descriptive message"
```

#### Before Lunch/End of Day:

```bash
# 1. Pull latest changes
git pull origin main

# 2. Resolve any conflicts if needed

# 3. Push your commits
git push origin main
```

---

### 🚨 Common Collaboration Problems & Solutions

#### Problem 1: "My push was rejected!"

```bash
git push origin main
# ERROR: Updates were rejected because the remote contains work...
```

**Solution:**
```bash
git pull origin main    # Get friend's changes first
git push origin main    # Then push yours
```

---

#### Problem 2: "I pulled and now my code is broken!"

Your friend pushed broken code or something incompatible.

**Solution:**
```bash
# Go back to before the pull
git log --oneline
# Find the commit before the pull

git reset --hard <your-last-commit-hash>

# Now talk to your friend about the broken code!
```

---

#### Problem 3: "We both edited the same file and Git is confused!"

**Solution:**
```bash
# This is a merge conflict (see section above)
# 1. Open the file
# 2. Look for <<<<<<< markers
# 3. Manually choose what to keep
# 4. Remove the markers
# 5. git add <file>
# 6. git commit
```

---

#### Problem 4: "I pushed something by mistake!"

**If you just pushed 1 minute ago and friend hasn't pulled yet:**
```bash
# Undo the push (DANGEROUS - only if friend hasn't pulled!)
git reset --hard HEAD~1
git push --force origin main  # This is risky!
```

**Better solution - if friend already pulled:**
```bash
# Create a new commit that undoes the mistake
git revert HEAD
git push origin main
```

---

### 🎯 Collaboration Strategy for This Project

#### Strategy 1: Main Branch Only (Simple, for 2 people)

**Rules:**
1. Always pull before starting work: `git pull origin main`
2. Commit frequently with clear messages
3. Pull before pushing: `git pull`, then `git push`
4. Talk before editing the same file

**When to use:** Small team, working on different parts of code

---

#### Strategy 2: Feature Branches (Better for Collaboration)

**Rules:**
1. Main branch is always working code
2. Each person works on their own branch
3. Merge to main when feature is complete

**Example:**

```bash
# You: Working on Phase 2
git checkout -b phase2-cypher-rules
# Make changes, commit
git push origin phase2-cypher-rules

# Friend: Working on frontend improvements
git checkout -b frontend-improvements
# Make changes, commit
git push origin frontend-improvements

# When ready: Merge one at a time
git checkout main
git merge phase2-cypher-rules
git push origin main

# Friend pulls the merged changes
git checkout main
git pull origin main
```

**Benefits:**
- No conflicts!
- Main branch always works
- Easy to review each other's code before merging
- Can throw away a branch if experiment fails

---

#### Strategy 3: GitHub Pull Requests (Professional)

**Workflow:**
1. Create branch for feature
2. Push branch to GitHub
3. Open Pull Request on GitHub website
4. Friend reviews code, comments
5. Make changes based on feedback
6. Friend approves and merges
7. Pull merged changes to local

```bash
# 1. Create and work on branch
git checkout -b my-feature
git commit -m "Add feature"
git push origin my-feature

# 2. Go to GitHub website
# Click "New Pull Request"
# Select: base=main, compare=my-feature
# Add description, click "Create Pull Request"

# 3. Friend reviews on GitHub
# Friend clicks "Merge" when approved

# 4. You pull the merged changes
git checkout main
git pull origin main

# 5. Delete the feature branch
git branch -d my-feature
```

---

### 📊 Visualization: Typical Collaboration Scenario

```
Timeline:

9:00 AM  - You pull latest changes
         git pull origin main

10:00 AM - You make commits locally
         git commit -m "Feature A"
         git commit -m "Feature B"

11:00 AM - Friend pushes their changes to remote
         (You don't know this yet!)

12:00 PM - You try to push
         git push origin main
         ❌ ERROR: rejected!

         # Solution:
         git pull origin main    # Get friend's changes
         # Git auto-merges if possible
         # If conflict: resolve manually
         git push origin main    # Now it works!
```

---

### 🛡️ Collaboration Safety Rules

#### ✅ DO:

1. **Pull before starting work** - Get latest changes
2. **Commit frequently** - Small commits are easier to merge
3. **Pull before pushing** - Avoid conflicts
4. **Communicate** - Tell team what you're working on
5. **Use branches** - For big features or experiments
6. **Write clear commit messages** - Help team understand changes
7. **Test before pushing** - Don't break main branch
8. **Review code** - Check what you're committing

#### ❌ DON'T:

1. **Don't force push to main** - Can delete friend's work!
2. **Don't commit directly to main** - Use branches for features
3. **Don't push broken code** - Test first
4. **Don't ignore conflicts** - Resolve them carefully
5. **Don't work on same file simultaneously** - Coordinate first
6. **Don't commit large files** - Slows down everyone
7. **Don't commit secrets** - Passwords, API keys
8. **Don't ignore pull requests** - Review teammate's code

---

### 🆘 Emergency: "I Broke Everything!"

#### If you broke your local code:

```bash
# Throw away ALL local changes, get fresh copy from remote
git fetch origin
git reset --hard origin/main
```

#### If you broke the remote (pushed broken code):

```bash
# Create commit that fixes the problem
# ... fix the code ...
git add .
git commit -m "Fix: Resolve issue with X"
git push origin main

# OR: Revert the broken commit
git revert HEAD
git push origin main
```

#### If merge conflicts seem impossible:

```bash
# Abort the merge, try again
git merge --abort

# Or: Start fresh from remote
git fetch origin
git reset --hard origin/main
# You'll lose local changes! Make backup first
```

---

### 📞 Quick Collaboration Commands

```bash
# Daily workflow
git pull origin main           # Get teammate's changes
git status                     # Check what changed
git add .                      # Stage your changes
git commit -m "Description"    # Commit
git pull origin main           # Pull again before push
git push origin main           # Push your changes

# Check remote status
git fetch origin               # Download info (don't merge)
git status                     # See if remote is ahead

# See what teammate did
git log origin/main            # See remote commits
git diff main origin/main      # See differences

# Branch workflow
git checkout -b my-feature     # Create feature branch
git push origin my-feature     # Push branch
# (Merge on GitHub via Pull Request)
git checkout main              # Switch to main
git pull origin main           # Get merged changes
```

---

### 💡 Tips for Smooth Collaboration

1. **Set up VS Code Git integration** - See changes visually
2. **Use GitHub Desktop** - If command line is intimidating
3. **Create .gitignore** - Don't commit unnecessary files
4. **Agree on code style** - Reduces conflicts
5. **Use GitHub Issues** - Track tasks and bugs
6. **Regular team syncs** - Discuss who's working on what
7. **Code reviews** - Learn from each other

---

**Remember:** Communication is key! Most Git problems in collaboration come from lack of communication, not Git itself.

---

## ⚠️ Common Mistakes and How to Fix Them

### Mistake 1: Committed to wrong branch

```bash
# You're on main, but wanted to commit to feature branch
git log --oneline -1  # Get the commit hash

git reset --hard HEAD~1  # Remove commit from main
git checkout feature-branch  # Switch to correct branch
git cherry-pick <commit-hash>  # Apply commit here
```

### Mistake 2: Forgot to add files to commit

```bash
# Make the commit
git commit -m "Add feature"

# Oops, forgot a file!
git add forgotten-file.py
git commit --amend --no-edit  # Add to previous commit
```

### Mistake 3: Bad commit message

```bash
git commit --amend -m "Better commit message"
```

### Mistake 4: Committed secrets (passwords, API keys)

```bash
# Remove file from last commit
git rm --cached secret-file.txt
git commit --amend -m "Remove secret file"

# Add to .gitignore so it doesn't happen again
echo "secret-file.txt" >> .gitignore
```

### Mistake 5: Merge conflict

```bash
# When merging, Git shows conflicts
git merge feature-branch
# CONFLICT in myfile.py

# Open myfile.py, you'll see:
<<<<<<< HEAD
your code
=======
their code
>>>>>>> feature-branch

# Manually edit to keep what you want
# Then:
git add myfile.py
git commit -m "Resolve merge conflict"
```

---

## 🛡️ Git Safety Rules

### ✅ DO:

1. **Commit frequently** - After each working feature
2. **Write clear commit messages** - Describe WHAT you did and WHY
3. **Commit before big changes** - Create checkpoints
4. **Use branches for experiments** - Keep main stable
5. **Test before committing** - Make sure code works
6. **Pull before push** - Get latest changes first
7. **Use .gitignore** - Don't commit unnecessary files

### ❌ DON'T:

1. **Don't commit broken code** to main branch
2. **Don't commit secrets** (passwords, API keys, .env files)
3. **Don't use `--force` unless necessary** - Can delete others' work
4. **Don't commit large files** (videos, datasets > 100MB)
5. **Don't commit dependencies** (node_modules, venv)
6. **Don't change history after pushing** - Causes problems for others

---

## 📝 .gitignore File

Create a `.gitignore` file to tell Git which files to ignore:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
*.sqlite
data/large_files/
```

---

## 🎯 Recommended Workflow for This Project

### Phase Checkpoint Strategy

```bash
# 1. Before starting Phase 2, commit Phase 1
git add data/csv_friend/bns_10_sections_enhanced.csv
git add neo4j_import_enhanced.cypher
git add verify_enhanced_graph.cypher
git add tasks/todo.md
git commit -m "Phase 1: Enhanced BNS knowledge graph

- Created enhanced CSV with legal elements
- Added Neo4j import script
- Graph has 159 nodes and 176 relationships"

# 2. Create branch for Phase 2
git checkout -b phase2-cypher-rules

# 3. Work on Phase 2
# ... make changes ...
git add backend/app/services/neo4j_service.py
git commit -m "Phase 2: Replace keyword matching with Cypher queries"

# 4. Test thoroughly
# If it works:
git checkout main
git merge phase2-cypher-rules

# If it breaks:
git checkout main
# Phase 2 changes are isolated in branch, main is still working!
```

### Daily Workflow

```bash
# Morning: Start working
git status  # See what's changed
git pull    # Get latest changes (if working with others)

# During work: Commit frequently
git add <files>
git commit -m "Description of changes"

# Evening: Push to remote (if using GitHub)
git push origin main
```

---

## 🔧 Useful Git Configurations

```bash
# Set your name and email (appears in commits)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Use better diff colors
git config --global color.ui auto

# Set default editor
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "nano"         # Nano

# See all configurations
git config --list

# Create aliases (shortcuts)
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --all"

# Now you can use: git st instead of git status
```

---

## 📊 Visual Git History

```bash
# Beautiful graph of commits and branches
git log --oneline --graph --all --decorate

# Example output:
* 03b2f89 (HEAD -> main) Update README
* b387322 Add Neo4j import script
* d686a04 Initial commit
```

---

## 🆘 Emergency Commands

### "I messed up everything, just go back to last commit!"

```bash
git reset --hard HEAD
git clean -fd  # Remove untracked files
```

### "I need to see my code from yesterday!"

```bash
# Find commits from yesterday
git log --since="yesterday"

# Checkout that commit
git checkout <commit-hash>

# Look around, copy code you need
# Then go back to present
git checkout main
```

### "I accidentally deleted a file!"

```bash
# If not committed yet
git restore deleted-file.py

# If deleted in a previous commit
git log --all --full-history -- deleted-file.py  # Find when it existed
git checkout <commit-hash> -- deleted-file.py    # Restore it
```

### "I want to start over with a clean slate"

```bash
# This keeps your commits but removes all uncommitted changes
git reset --hard HEAD
git clean -fd

# This removes ALL commits and starts fresh (NUCLEAR OPTION)
rm -rf .git
git init
git add .
git commit -m "Fresh start"
```

---

## 📚 Learning More

### Useful Resources

- **Official Git Book:** https://git-scm.com/book/en/v2
- **Interactive Git Tutorial:** https://learngitbranching.js.org/
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf
- **Oh Shit, Git!?!** https://ohshitgit.com/ (fixing common mistakes)

### Practice

```bash
# Create a test repository to practice
mkdir git-practice
cd git-practice
git init

# Practice making commits, branches, merges
# Experiment freely - you can't break anything!
```

---

## 🎓 Git Philosophy

**Key Principles:**

1. **Commit early, commit often** - Small, frequent commits are better than large ones
2. **Commits are cheap** - Don't be afraid to commit
3. **History is valuable** - Don't delete commits unless necessary
4. **Branches are your friend** - Use them for experiments
5. **Main branch should always work** - Keep it stable

**Remember:**
- Git is your safety net, not your enemy
- You can almost always undo mistakes
- When in doubt, commit before trying something risky
- Branches let you experiment without fear

---

## 📞 Quick Command Reference

```bash
# Status and History
git status              # What's changed?
git log --oneline       # Show commits
git diff                # What changed?

# Making Changes
git add <file>          # Stage file
git commit -m "msg"     # Commit staged files
git restore <file>      # Discard changes

# Branches
git branch              # List branches
git checkout -b <name>  # Create and switch
git merge <branch>      # Merge branch into current

# Time Travel
git checkout <commit>   # View old commit
git reset --hard HEAD~1 # Undo last commit (delete changes)
git reset --soft HEAD~1 # Undo last commit (keep changes)
git revert <commit>     # Create commit that undoes another

# Remote
git pull                # Get changes from remote
git push                # Send changes to remote
git clone <url>         # Copy repository

# Emergency
git reset --hard HEAD   # Discard everything, go back to last commit
git reflog              # See ALL actions (can recover "deleted" commits)
```

---

**Last Updated:** 2025-01-09

**Remember:** Git is a tool to help you, not hurt you. When in doubt, commit first, then experiment!

---

## 🎯 For This Project Specifically

**Current State:**
- Branch: `main`
- Last commit: `03b2f89` - "Update README to reference neo4j_import.cypher file"
- Working on: Phase 1 (Enhanced Knowledge Graph) - COMPLETED
- Next: Phase 2 (Cypher Graph Rules)

**Recommended Next Steps:**
1. Commit Phase 1 work
2. Create `phase2` branch
3. Implement Phase 2 changes
4. Test thoroughly
5. Merge back to `main` if successful

**Safety Net:**
- You can ALWAYS go back to commit `03b2f89` where the system was working
- Each phase should be its own commit
- Use branches for major changes
