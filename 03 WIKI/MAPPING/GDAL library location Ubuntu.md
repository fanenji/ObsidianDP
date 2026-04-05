---
title: "GDAL library location Ubuntu"
type: conversation
topic: gis
created: 2026-02-13
tags:
  - gdal
  - ubuntu
  - mapping

---
> From: https://chatgpt.com/c/68090c2f-1bd4-8008-9e47-e0c4f9051fa2

# you asked

where is gdal lib (libgdal.so*) installed on ubuntu 22.04?

---

# chatgpt response

On Ubuntu 22.04, if you install GDAL via the package manager (`apt`), the GDAL shared library (`libgdal.so.*`) is typically located in one of the following directories:

- `/usr/lib/x86_64-linux-gnu/`
- `/usr/lib/` (less common)

You can confirm the exact location using the `dpkg` or `find` command:

### Option 1: Using `dpkg`
```bash
dpkg -L libgdal-dev | grep libgdal.so
```

### Option 2: Using `find`
```bash
sudo find /usr -name "libgdal.so*"
```

If you've built GDAL from source, the location depends on the installation prefix (e.g., `/usr/local/lib/`).

Let me know if you're using a virtual environment, Docker, or custom build — the path may differ accordingly.
