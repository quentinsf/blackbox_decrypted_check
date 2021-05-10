# Blackbox_decrypted_check

A utility for use with the excellent [Blackbox](https://github.com/StackExchange/blackbox/) 
secret-management system.

We've encountered a problem with our use of Blackbox: someone has a decrypted copy of a file in their working directory, they pull updates from git and the encrypted copy has changed in the repo, but they don't know or notice this so keep on using their plain-text version.

This is script that checks for that, and warns you if you don't have a decrypted version of all your blackbox-controlled files, or if any of them don't match the encrypted versions.  The idea is that you might incorporate the script into some post-checkout process, or the first stage of whatever you might do next with the decrypted files (e.g. deploying your system).

The exit code will normally be 0 if all is well and matches, 1 if not, and higher numbers for more serious failings.

To use this, you need to `pip install python-gnupg`.  Note that python-gnupg is NOT
the same (confusingly) as the very similar older 'gnupg'.

No warranties, no licence, handle with care and at your own risk!  Hope it's useful!

Quentin Stafford-Fraser
