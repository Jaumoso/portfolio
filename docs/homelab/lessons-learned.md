# Lessons Learned

Real incidents from running this server, what caused them and what I changed. These are the
parts of a homelab that teach the most.

??? failure "Random total network loss on a Wi-Fi-only server"
    **Symptom:** every few days the server lost all connectivity (could not even reach the gateway) until the network was restarted. Two manual reboots in one day was the breaking point.

    **Investigation:** kernel logs showed `iwlwifi: No beacon heard`, the adapter was on the congested 2.4 GHz band despite 5 GHz being available, Wi-Fi power-save was on, and `systemd-networkd-wait-online` timed out every few hours because of an unplugged Ethernet port. On top of that, the firewall dropped the WireGuard handshake at boot until Docker added its own rules.

    **Fix:**

    - Disabled Wi-Fi power saving (persisted with a systemd unit and `iwlwifi`/`iwlmvm` module options for a 24/7 profile).
    - Pinned the access point's 5 GHz BSSID.
    - Marked the unused Ethernet interface as `optional` in netplan.
    - Added an explicit firewall rule for the tunnel's WireGuard traffic.
    - Rewrote the network watchdog: restart only the Wi-Fi interface, retry three times, **never** act while Docker is pulling images, and reboot only as a last resort.

    **Lesson:** a watchdog that reboots too eagerly creates its own outages. Fix the root cause and make the recovery gentle.

??? failure "Filesystem errors on a data disk"
    **Symptom:** `EXT4-fs error … checksum invalid` in `dmesg` on the application-data disk.

    **Cause:** a corrupted cache file left behind by an old photo app (PhotoPrism) I no longer used.

    **Fix:** stopped the 17 stacks using that disk, removed the stale data (~20 GB), ran `fsck`, remounted and restarted everything in order. No new errors since.

    **Lesson:** retired apps should not leave data behind; and knowing *which* stacks use *which* disk makes maintenance safe.

??? failure "Boot failure after a kernel upgrade"
    **Symptom:** `Initramfs unpacking failed: ZSTD-compressed data is corrupt` after an unattended kernel upgrade.

    **Fix:** regenerated the initramfs, then made boot resilient: GRUB menu with a timeout, a consistent default entry, initramfs backups enabled and a post-upgrade check — so a bad kernel can always fall back to the previous one.

    **Lesson:** unattended upgrades need a safety net, especially on a machine without a screen.

??? failure "Backups that silently stopped"
    **Symptom:** the weekly push of Compose files to GitHub had stopped without anyone noticing.

    **Cause:** the job ran as `root` on a repository owned by my user → Git refused with *dubious ownership*.

    **Fix:** marked the directory as safe and moved all cron jobs to a UI (Cronmaster) where last run, exit code and logs are visible. The weekly commits in the homelab repo now act as a public heartbeat.

    **Lesson:** a backup without monitoring is a hope, not a backup.

??? failure "Container wrote data inside itself instead of the volume"
    **Symptom:** a music app was storing its files inside the container instead of the mounted folders — they would have been lost on the next recreate.

    **Cause:** a mismatch between the folder names the app expected and the bind-mount paths in the Compose file, so files were written to the container's writable layer.

    **Fix:** copied the data out of the container first, corrected the mounts and recreated it.

    **Lesson:** after deploying a new app, check that the data really lands on the host (`docker diff` is great for this).

??? success "Dropping a mesh VPN in favour of the existing tunnel"
    I used Tailscale for remote access, but everything it gave me could be done through the
    Pangolin/WireGuard tunnel that already existed. Removing it meant one less agent, one less
    account and one less moving part. Remote SSH now hops through the VPS into the tunnel.
