# Easy deployment with systemd and rpm.

This repository gives a simple example of deploying a web server (which happens to be written in go) using systemd and rpm. This deployment stack is meant for small deploys, which don't need on-demand scalability or container-like isolation. The advantages are simplicity and power coming from underlying technologies. The next two chapters provide an opinionated rationale for the approach. You can skip these sections and jump straight to the tutorial.

## Why systemd?

Systemd is arguably the best way to deploy long-running services, suchas web applications, web servers, databases, deamons, etc. The main reasons are:

 * Systemd is everywhere. Every major linux distro has systemd installed and running by default.
 * Systemd is mature. It has been around for years, so many major and minor bugs have been found and fixed, many common and uncommon use cases have been figured out and described in man pages and elsewhere.
 * Systemd is flexible. Major players are deploying with systemd: gnome desktop manager, ssh deamon, Network Manager, cron deamon, /etc/fstab, Microsoft's Hyper-V are just some examples. Note how dramatically different these services are.
 * Systemd is easy. That's how you start your ssh deamon: `systemctl start sshd`. That's how you instruct your OS to ALWAYS start sshd deamon straight after bootup, so you never have to think about it again `systemctl enable sshd`. Things don't go as planned? journalctl --unit=sshd` gives you all the logs from misbehaving service. And that's all you'll mostl likely need. Super easy.
 * Systemd is powerful. It supports complicated multi-component deploys, it has powerful component initiation and dependency management, including lazy dependency management via socket initialisation.
 * Distro developers, Package mainteiners, Dev Ops and such have more arguments to convince you, if you need: [Arch Linux](https://bbs.archlinux.org/viewtopic.php?pid=1149530#p1149530), [Core OS](https://coreos.com/using-coreos/systemd/), [Running lightweight containers in systemd](https://fedoraproject.org/wiki/Features/SystemdLightweightContainers). You'll find people who disagree: [Docker vs Systemd](http://thenewstack.io/why-docker-containers-and-systemd-drive-a-wedge-through-the-concept-of-linux-distributions/)
 * You can reload your service without restarting it. It's a big plus if availability is a concern.

It doesn't mean there are no alternatives!

 * You should also consider docker. Be warned that it won't be easy, docker on itself won't be enough (you'll have to use something like swarm or kubernetes), and many things you're used to won't work or will work differently. For a balanced and outisder opinion have a look at [Dan Walsh's presentation on systemd vs docker](https://www.youtube.com/watch?v=35biGFCWdlQ).
 * Checkout how to deploy with vagrant [danieltcv](https://github.com/danieltcv/product_reviews/tree/master)

## Why rpm (deb, any other distro-specific package)?

There are big benefits from being a first-class citizen among applications installed on a linux distribution. You benefit from:
 * Installation process that works. It does, because millions of people have used it for decades and bugs have been fixed and user experience has been made pleasant.
 * Entire infrasturcture of native package management, such as updates (that's a big one!), dependency resolution and uninstalls.
 * Very easy. Contrast `dnf install websitego.rpm` with "copy-paste this massive bash script, which might work if you've installed these dependencies manually beforehand."

There are drawbacks. If you're targeting multiple distros you have to esentially redo some work.

## Tutorial

`websitego.go` contains golang code of a "hello world" web application, which binds to localhost:8080 and displays some text on GET / HTTP request. We show a way to deploy it to any computer running rpm-based distro. This includes fedora, RHEL and CentOS among others. We first build an rpm package, we install it, and then we run it using systemd.

### Build dependencies (for website developers)

* `rpmbuild` to build the rpm package with the website.

### Runtime dependencies (for sysadmins)

* rpm-based package manager. `yum` or `dnf` will do best. `rpm` will work, but won't provide extra features, like updates, uninstallation and dependency resolution.

* systemd. Don't worry about it. You're using it even if you don' know it.

### Build, installation and running

* Run `./makerpm` to build the rpm package. The shell script builds the package, which includes a compiled binary with our website, and a systemd config file, which will instruct systemd how to run the website.
* Copy the websitego-0.0-1.x86_64.rpm package from the rpm/x86_64 folder wherever you want to install it.
* Run `dnf install websitego-0.0-1.x86_64.rpm` to install the package with all its dependencies (golang >= 1.0.0)
* Run `systemctl start websitego` to run the website. It will listen on localhost:8080/

### Management.

* You can `systemctl enable websitego`. This will make the website always start at system bootup, so you won't have to think about it.
* If things go wrong `journalctl --unit=websitego` will give you the logs produced by the website
* If you decide to realese a new version, modify `website.spec` and `makerpm` with a new, higher version number (you can even automate it, e.g. on each build) and repeat the build process above to update the package on the system hosting the website. dnf should figure out any file additions/ changes/ deletions.
