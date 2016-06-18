# Easy deployment with systemd and rpm.

This repository gives a simple example of deploying a web server (which happens to be written in go) using systemd and rpm. This deployment stack is meant for small deploys, which don't need on-demand scalability or container-like isolation. The advantages are simplicity and power coming from underlying technologies. The next two chapters provide an opinionated rationale for the approach. You can skip these sections and jump straight to the tutorial.

## Why systemd?

Systemd is arguably the best way to deploy long-running services, such as web applications, web servers, databases, deamons, etc. The main reasons are:

 * Systemd is everywhere. Every major linux distro has systemd installed and running by default.
 * Systemd is mature. It has been around for years, so many major and minor bugs have been found and fixed, many common and uncommon use cases have been figured out and described in man pages and elsewhere.
 * Systemd is flexible. Major players are deploying with systemd: gnome desktop manager, ssh deamon, Network Manager, cron deamon, /etc/fstab, Microsoft's Hyper-V are just some examples. These services are very different, yet systemd supports them all. This means there's plenty of material to learn from. You can start by reading the unit file of sshd `/usr/lib/systemd/system/sshd.service` 
 * Systemd is easy. That's how you start your ssh deamon: `systemctl start sshd`. That's how you instruct your OS to ALWAYS start sshd deamon straight after bootup, so you never have to think about it again: `systemctl enable sshd`. Things don't go as planned? `journalctl --unit=sshd` gives you all the logs from misbehaving service. And that's all you'll most likely need. Super easy.
 * Systemd is powerful. It supports complicated multi-component deploys, it has powerful component initiation and dependency management, including lazy dependency management via socket initialisation.
 * Distro developers, Package mainteiners, Dev Ops and such have more arguments to convince you, if you need: [Arch Linux](https://bbs.archlinux.org/viewtopic.php?pid=1149530#p1149530), [Core OS](https://coreos.com/using-coreos/systemd/), [Running lightweight containers in systemd](https://fedoraproject.org/wiki/Features/SystemdLightweightContainers). You'll find people who disagree: [Docker vs Systemd](http://thenewstack.io/why-docker-containers-and-systemd-drive-a-wedge-through-the-concept-of-linux-distributions/)
 * You can reload your service without restarting it. It's a big plus if availability is a concern.

It doesn't mean there are no alternatives!

 * You should also consider docker. Be warned that it won't be easy, docker on itself won't be enough (you'll have to use something like swarm or kubernetes), and many things you're used to won't work or will work differently. For a balanced and outsider opinion have a look at [Dan Walsh's presentation on systemd vs docker](https://www.youtube.com/watch?v=35biGFCWdlQ).
 * Checkout how to deploy with vagrant [danieltcv](https://github.com/danieltcv/product_reviews/tree/master)

## Why rpm (deb, any other distro-specific package)?

There are big benefits from being a first-class citizen among applications installed on a linux distribution. You benefit from:
 * Installation process that works. It does, because millions of people have used it for decades and bugs have been fixed and user experience has been made pleasant.
 * Entire infrastructure of native package management, such as updates (that's a big one!), dependency resolution and uninstalls.
 * Very easy. Contrast `dnf install websitego.rpm` with "copy-paste this massive bash script, which might work if you've installed these dependencies manually beforehand."

There are drawbacks. If you're targeting multiple distros you have to esentially redo some work.

## Tutorial

`websitego.go` contains golang code of a "hello world" web application, which binds to localhost:8080 and displays some text on GET / HTTP request. We show a way to
* Make an rpm with all development dependencies (everything that is required to build the project).
* Install it.
* Make an rpm with the website we want to deploy, again with all dependencies.
* Deploy it to any computer running an rpm-based distro.

### Build dependencies (for website developers)

* `rpmbuild` to build the rpm package with the website.

### Runtime dependencies (for sysadmins)

* rpm-based package manager. `yum` or `dnf` will do best. `rpm` will work, but won't provide extra features, like updates, uninstallation and dependency resolution. You need to adjust the instructions if you're not using `dnf`. For example, if you're using `yum`, replace and occurrence of `dnf` with `yum`.

* systemd. Don't worry about it. You've got it installed even if you don't know it.

### Build, installation and running

* `git clone git@github.com/picrin/deployment.git` to get the project with all the files you need.
* `dnf install rpm-build` to get rpm-build, which is a tool that lets you build packages for rpm-based linux distributions (fedora, centOS, RHEL).
* `./makeDevEnvironment` to make an rpm containing all dependencies required to build the project.
* `dnf install rpm/x86_64/devEnvironment-0.0-1.x86_64.rpm` to install dev environment.
* `./makerpm` to build the rpm package with the website.
* Copy the package you built, which now lives in `rpm/x86_64/websitego-0.0-1.x86_64.rpm` folder wherever you want to install it. Or skip this step to install locally.
* `dnf install rpm/x86_64/websitego-0.0-1.x86_64.rpm` to install the package with all its dependencies (golang >= 1.0.0).
* Run `systemctl start websitego` to run the website. It will listen on localhost:8080/.

### Management.

* You can `systemctl enable websitego`. This will make the website always start at system bootup, so you won't have to think about it.
* If things go wrong `journalctl --unit=websitego` will give you the logs produced by the website
* If you decide to deploy a new version of your website or devEnvironment edit one of `version/patch`, `version/minor` or `version/major` to a higher number. Do the build/deployment process above as normal to update the package on the system hosting the website. `dnf` will figure out any file additions/ changes/ deletions.
