#! /usr/bin/env python3
#
# This warns you if you don't have a decrypted version of all your
# blackbox-controlled files, or if any of them don't match the encrypted
# versions.
# The exit code will normally be 0 if all is well and matches,
# 1 if not, and higher numbers for more serious failings.
#
# You need to `pip install python-gnupg`.  Note that python-gnupg is NOT
# the same (confusingly) as the very similar older 'gnupg'.
#
# Quentin Stafford-Fraser

import sys
from pathlib import Path
from typing import Optional

import gnupg


def find_blackbox_root(start_dir: str = '.') -> Optional[Path]:
    """
    Return the Path of the directory that contains .blackbox
    above or including this one.
    """
    p = Path(start_dir).resolve()
    while not (p / ".blackbox").exists():
        if p.parent == p:
            return None  # We hit root
        p = p.parent
    return p


def main() -> int:
    blackbox_root = find_blackbox_root()
    if blackbox_root is None:
        print("No .blackbox found in this or parent directories", file=sys.stderr)
        return 2
    issue_found = False
    with open(blackbox_root / ".blackbox" / "blackbox-files.txt", "rt") as bbfiles:
        for f in bbfiles.readlines():
            plain_path = Path(blackbox_root / f.strip())
            gpg_path = plain_path.with_suffix(plain_path.suffix + ".gpg")
            if not gpg_path.exists():
                print(f"Can't find {gpg_path}", file=sys.stderr)
                return 3
            if not plain_path.exists():
                print(f"Decrypted file {plain_path} is missing")
                issue_found = True
            else:
                gpg_time = gpg_path.stat().st_mtime
                plain_time = plain_path.stat().st_mtime
                if gpg_time > plain_time:
                    print(f"Encrypted file {gpg_path} is more recent than {plain_path}")
                    issue_found = True
                gpg = gnupg.GPG("gpg", use_agent=True)
                with open(plain_path, "rb") as plain_fp:
                    with open(gpg_path, "rb") as encrypted_fp:
                        plain_data = plain_fp.read().decode('utf-8')

                        decrypted_obj = gpg.decrypt_file(encrypted_fp,  always_trust=True)
                        if decrypted_obj.ok:
                            decrypted_data = str(decrypted_obj)
                            if plain_data != decrypted_data:
                                print(f"Encrypted and decrypted versons of {plain_path} do not match")
                                issue_found = True
                        else:
                            print(f"Decryption of {gpg_path} failed: {decrypted_obj.status}",
                                  file=sys.stderr)
                            return 4

    return 1 if issue_found else 0

if __name__ == "__main__":
    sys.exit(main())
