# Security

Security in a homelab is mostly about **reducing what is exposed** and **knowing when something changes**.

## Access model

| Layer | Measure |
| --- | --- |
| **Router** | No port forwarding. Nothing at home is directly reachable from the internet |
| **Public services** | Only through Pangolin on the VPS, over an outbound WireGuard tunnel; per-resource auth available |
| **Admin UIs** | LAN only (Dockge, Prometheus, Syncthing UI, …) — never published |
| **SSH** | Key-only, non-standard port, no root login, no passwords; remote access is tunnelled through the VPS |
| **Docker API** | Never mounted into public-facing containers; tools that need it go through a read-only socket proxy |

## Host hardening

- **SSH**: `PermitRootLogin no`, `PasswordAuthentication no`, challenge/keyboard-interactive disabled, public keys only.
- **UFW**: default deny incoming; allow only private ranges and the specific ports that need it; standard SSH port explicitly denied.
- **Fail2ban**: SSH jail enabled; Docker networks are whitelisted so internal tools (e.g. a web terminal) are not banned by mistake.
- **unattended-upgrades**: automatic security updates; reboots are manual and planned.
- **AppArmor** enabled, kernel `sysctl` hardening (network and kernel pointer restrictions).
- **Boot safety**: GRUB menu with timeout, saved default and initramfs backups, so a broken kernel upgrade can always fall back to the previous kernel (see [Lessons Learned](lessons-learned.md)).

## Secrets

- Secrets live in per-stack `.env` files that are **git-ignored**; the public homelab repository only contains Compose files.
- Restic backups are encrypted client-side before leaving the server.
- This website is checked in CI for IP addresses, tokens, private keys and personal identifiers before every deploy.

## Updates

- OS: security updates automatically, the rest reviewed weekly with the help of the [APT metrics exporter](monitoring.md#custom-apt-metrics-exporter).
- Containers: updated **deliberately**, stack by stack, after reading release notes. I used Watchtower for a long time and moved away from fully automatic updates to stay in control of breaking changes (database major versions, config migrations).

## Next steps

- Identity provider / SSO in front of more services
- Rootless or user-namespaced Docker for stacks that allow it
- Regular, tested restores instead of "backups that probably work"
