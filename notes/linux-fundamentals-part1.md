# TryHackMe — Linux Fundamentals Part 1

- Date completed: 2026-02-07
- Room: https://tryhackme.com/room/linuxfundamentalspart1

## Skills & Commands
- Filesystem navigation: `pwd`, `ls -la`, `cd`, wildcards `*`, `?`, hidden files
- Search & read: `cat`, `less`, `head`, `tail`, `grep -R "pattern" .`
- Permissions & ownership: `chmod`, `chown`, numeric and symbolic modes; `umask`
- Processes & services: `ps aux`, `top/htop`, `systemctl status <svc>`
- Packages & archives: `apt update && apt install`, `dpkg -L`, `tar -czf`, `tar -xzf`, `gzip -d`
- Networking basics: `ip a`, `ss -tulpn`
- Remote basics: `ssh user@host`, `scp file user@host:~/`

## Key Takeaways
- Comfort moving around the FS and reading docs/logs is foundational for incident response
- Permission model (user/group/other) directly affects privesc and hardening
- Journals/logs + `systemctl` are your first stop for triage on Linux systems

## Next Steps
- Parts 2 and 3 of Linux Fundamentals
- Do “Crack the Hash” 1 and 2 to apply wordlists/rules with hashcat

---
Notes are non-spoiler and focus on repeatable commands and reasoning.
