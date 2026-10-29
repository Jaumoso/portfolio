<div class="hero" markdown>

# 👋 Hi, I'm Jaume

**Developer & DevOps** based in Valencia, Spain.
I build things, automate them, and run (almost) everything I use on my own infrastructure.

</div>

This site is the long version of my GitHub profile: what I have built at home, how it works, how it is backed up, and how it has evolved over time.

<div class="grid cards" markdown>

-   :material-server-network:{ .lg .middle } **Homelab**

    ---

    A single low-power server running ~60 Docker stacks, published to the internet through a self-hosted reverse proxy on a VPS, with 3-2-1 backups and full observability.

    [:octicons-arrow-right-24: Explore the homelab](homelab/index.md)

-   :material-rocket-launch:{ .lg .middle } **Projects**

    ---

    Apps I wrote because I needed them — and now run in production at home.

    [:octicons-arrow-right-24: Kalenda](projects/kalenda.md) · [docker-picard](projects/docker-picard.md)

-   :material-timeline-clock:{ .lg .middle } **Timeline**

    ---

    From a spare laptop running a couple of containers to a small self-hosted platform.

    [:octicons-arrow-right-24: See the timeline](timeline.md)

-   :material-map-marker-path:{ .lg .middle } **Roadmap**

    ---

    What I am working on now and what comes next.

    [:octicons-arrow-right-24: See the roadmap](roadmap.md)

</div>

## What this shows

| Area | In practice |
| --- | --- |
| **Containers** | ~60 Docker Compose stacks, Compose files versioned in Git, isolated networks, socket proxy |
| **Networking** | Reverse proxy on a VPS + WireGuard tunnel → no inbound ports open at home; custom domain with TLS |
| **Observability** | Prometheus, Grafana, Loki, Beszel, SMART monitoring, push alerts with ntfy |
| **Data safety** | 3-2-1 backups: real-time sync, weekly cloud copy, encrypted Restic snapshots to object storage |
| **Linux administration** | Ubuntu Server hardening, UFW, Fail2ban, unattended upgrades, kernel/Wi-Fi troubleshooting |
| **Software** | Full-stack TypeScript app (Kalenda), Python services, Docker images published to GHCR with CI |
| **Automation** | Cron-driven maintenance scripts, GitHub Actions (this site regenerates itself from my homelab repo) |

!!! info "About the details on this site"
    Everything here describes my real setup, but IP addresses, ports, user names, hostnames and
    internal paths are intentionally left out. A CI check blocks any publish that contains them.
