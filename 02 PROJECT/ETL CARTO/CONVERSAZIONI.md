
# CONVERSIONI

## RQA

```other
Convert this groovy script to a python script with the same name.
--
Change references to config.properties to the file .env and populate 
the .env file with the required referenced variables from config.properties if missing. 
Use load_dotenv to read the .env file
--
Read the OGR2OGR command from the OGR2OGR_CMD var in the .env file
--
Read the pgHost var from the .env file.
--
Change all references to the env var pgHost to the env var PG_HOST
--

<OTHER ENV VARS>
--
Create a .py.bat and a .sh file to launch the script in Windows and Ubuntu
--
Use argparse to read input params:
<DESCRIZIONE PARAMETRI>
```

```other

```

# PROJ GDB

I have a containerized gdal intallation with proj version 8

how can i add some gsb files to it?

i mounted a custom dir to /usr/share/proj but proj returns an error:

RROR 1: PROJ: proj_create_from_database: /usr/share/proj/proj.db lacks DATABASE.LAYOUT.VERSION.MAJOR / DATABASE.LAYOUT.VERSION.MINOR metadata. It comes from another PROJ installation.

ERROR 1: Failed to process SRS definition: EPSG:7791

## RESPONSE

Okay, the error message is the key here:

```other
ERROR 1: PROJ: proj_create_from_database: /usr/share/proj/proj.db lacks DATABASE.LAYOUT.VERSION.MAJOR / DATABASE.LAYOUT.VERSION.MINOR metadata. It comes from another PROJ installation.
```

This tells you exactly what went wrong:

1. PROJ (version 8 in your container) relies heavily on the `proj.db` SQLite database file located in its data directory (usually `/usr/share/proj`). This database contains metadata about projections, transformations, and crucially, *where to find grid shift files*.
2. When you mounted your custom directory to `/usr/share/proj`, you **replaced** the original PROJ 8 `proj.db` file (and potentially other necessary files/subdirectories) with whatever was in your custom directory.
3. If your custom directory contained an older `proj.db` or no `proj.db` at all, the PROJ 8 library inside the container can no longer read it correctly, leading to the error. PROJ cannot initialize properly, and therefore cannot find *any* grids, including the ones you wanted to add, or even standard ones.

**The Correct Approach: Use `PROJ_DATA`**

The recommended way to add custom grid files without interfering with the core PROJ installation is to:

1. **Mount your custom grids to a *separate* directory** inside the container.
2. **Tell PROJ to look in this additional directory** using the `PROJ_DATA` environment variable.

**Steps:**

1. **Prepare your host directory:**
    - Create a directory on your host machine that contains *only* your `.gsb` files (and potentially other custom resource files like `.gtx`, `.itrf`, etc.).
    - **Crucially, do NOT put a `proj.db` file in this directory.**
    - Example structure on your host:

```other
/path/on/host/my-custom-proj-grids/
├── my_vertical_grid.gsb
├── my_horizontal_grid.gsb
└── another_grid.gtx
```

1. **Mount the custom directory and set `PROJ_DATA`:**
    - When you run your container, mount this host directory to a location *other than* `/usr/share/proj`. A good choice might be `/opt/proj-custom-grids` or similar.
    - Set the `PROJ_DATA` environment variable. This variable takes a list of paths separated by colons (`:`) on Linux/macOS or semicolons (`;`) on Windows (inside the container, it will be Linux, so use colons). You need to include *both* the original PROJ data directory *and* your new custom directory.

```bash
# Determine the default PROJ data directory inside the container first if unsure.
# Often it's /usr/share/proj, but could be different (e.g., /opt/conda/share/proj).
# You can check by running the container interactively:
# docker run -it --rm your-gdal-image proj

# Let's assume the default is /usr/share/proj

docker run -d \\
  -v /path/on/host/my-custom-proj-grids:/opt/proj-custom-grids:ro \\
  -e PROJ_DATA="/usr/share/proj:/opt/proj-custom-grids" \\
  your-gdal-image:tag \\
  [your_container_command]
```

    - `v /path/on/host/my-custom-proj-grids:/opt/proj-custom-grids:ro`: Mounts your host directory read-only (`:ro`) into the container at `/opt/proj-custom-grids`.
    - `e PROJ_DATA="/usr/share/proj:/opt/proj-custom-grids"`: Sets the environment variable. PROJ will first search `/usr/share/proj` (and its `proj.db`), and then search `/opt/proj-custom-grids` for needed resource files like your `.gsb` files.

**Alternative: Build a Custom Docker Image**

If you prefer a more permanent solution, you can build a custom Docker image:

```other
# Start from your existing GDAL image
FROM your-gdal-image:tag

# Create a directory for custom grids
RUN mkdir -p /opt/proj-custom-grids

# Copy your custom grid files from your build context into the image
COPY /path/to/your/gsb_files/*.gsb /opt/proj-custom-grids/
# Add other file types if needed (e.g., .gtx)
# COPY /path/to/your/gtx_files/*.gtx /opt/proj-custom-grids/

# Set the PROJ_DATA environment variable permanently in the image
# Make sure to use the correct original path for your base image!
ENV PROJ_DATA="/usr/share/proj:/opt/proj-custom-grids"

# Optional: Set WORKDIR, ENTRYPOINT, CMD etc.
...
```

Then build and run this new image:

```bash
docker build -t my-custom-gdal-image .
docker run -d my-custom-gdal-image [your_container_command]
```

**Verification:**

Once your container is running with the correct setup, you can verify that PROJ can find and potentially use your grid:

1. Exec into the container: `docker exec -it <container_name_or_id> bash`
2. Use `projinfo` or `cs2cs`:
    - `projinfo -s EPSG:XXXX` (where XXXX is a CRS that *requires* your grid file for a transformation). Look at the output for transformation details - it might mention the grid file.
    - `cs2cs +init=epsg:YYYY +to +init=epsg:ZZZZ < input.txt` where the transformation between YYYY and ZZZZ requires your grid. If it works without error and gives correct results, the grid is likely being used.
    - Check PROJ logs/verbosity if needed (e.g., `export PROJ_DEBUG=3` before running a command).

This approach correctly uses PROJ's search path mechanism without breaking its core database dependency.

## DOCKER COMPOSE

Okay, here is a `docker-compose.yml` file that demonstrates how to run your GDAL container, mount your custom grid files, and set the `PROJ_DATA` environment variable correctly.

**Assumptions:**

1. Your container image is named `your-gdal-image:with-proj8` ( **You MUST change this** to your actual image name and tag).
2. The *default* PROJ data directory inside your *specific* container image is `/usr/share/proj`. **You MUST verify this.** If it's different (e.g., `/opt/conda/share/proj` in some Conda-based images), you need to adjust the `PROJ_DATA` variable accordingly.
3. You have a directory named `custom-proj-grids` on your host machine (in the same directory where you save this `docker-compose.yml` file) containing your `.gsb` files.
4. You want the container to run some command (replace the placeholder `sleep infinity`).

**Directory Structure on Host:**

```other
.
├── docker-compose.yml
└── custom-proj-grids/
    ├── your_grid_1.gsb
    ├── your_grid_2.gsb
    └── other_custom_file.gtx  # (optional)
```

**`docker-compose.yml`:**

```yaml
version: '3.8' # Specify compose file version

services:
  gdal-service:
    # --- REQUIRED: Change this to your actual GDAL image ---
    image: your-gdal-image:with-proj8

    container_name: my-gdal-app # Optional: give the container a specific name

    volumes:
      # Mount your custom grid files directory into the container
      # Host path (./custom-proj-grids) is relative to the docker-compose.yml file
      # Container path (/opt/proj-custom-grids) is where grids will be inside the container
      # ':ro' makes the mount read-only, which is safer
      - ./custom-proj-grids:/opt/proj-custom-grids:ro

    environment:
      # --- IMPORTANT: Verify '/usr/share/proj' is the correct default PROJ data path inside YOUR image ---
      # You can verify by running your image interactively (docker run -it --rm your-image bash) and then running `proj` or `echo $PROJ_DATA` if set by default.
      # This variable tells PROJ to look in the default location FIRST, then in your custom location.
      PROJ_DATA: "/usr/share/proj:/opt/proj-custom-grids"

      # Add any other environment variables your application needs
      # OTHER_VAR: "some_value"

    # --- REQUIRED: Define what your container should do ---
    # Replace 'sleep infinity' with the actual command to start your application
    # 'sleep infinity' is just a placeholder to keep the container running for testing/exec
    command: ["sleep", "infinity"]
    # Or, if your image has a default ENTRYPOINT/CMD you want to use, you might omit the 'command' line.
    # Or, define a specific entrypoint and command:
    # entrypoint: ["python", "my_gdal_script.py"]
    # command: ["--input", "/data/input.tif", "--output", "/data/output.tif"]

    # Optional: Restart policy
    # restart: unless-stopped

    # Optional: Mount other volumes if needed (e.g., for input/output data)
    # volumes:
    #   - ./custom-proj-grids:/opt/proj-custom-grids:ro
    #   - ./input-data:/data/input:ro
    #   - ./output-data:/data/output

networks: # Optional: Define networks if needed
  default:

# Optional: Define volumes if you need persistent named volumes managed by Docker
# volumes:
#   output-data-volume:
```

**Explanation:**

1. **`version: '3.8'`**: Defines the Docker Compose file format version.
2. **`services:`**: Defines the containers to be run.
3. **`gdal-service:`**: A name you give to this specific service/container definition.
4. **`image: your-gdal-image:with-proj8`**: **Crucial:** Replace this with the name and tag of the Docker image you built or pulled.
5. **`container_name: my-gdal-app`**: Assigns a predictable name to the running container.
6. **`volumes:`**: Defines directory mappings between the host and the container.
    - `./custom-proj-grids:/opt/proj-custom-grids:ro`: This mounts the `custom-proj-grids` directory (located alongside your `docker-compose.yml` file) into the container at `/opt/proj-custom-grids`. The `:ro` makes it read-only inside the container.
1. **`environment:`**: Sets environment variables inside the container.
    - `PROJ_DATA: "/usr/share/proj:/opt/proj-custom-grids"`: This is the key part. It tells PROJ library to search for data files (like `proj.db` and grid files) first in `/usr/share/proj` (the default location *assumed* for your image - **verify this!**) and then in `/opt/proj-custom-grids` (where your custom files are mounted).
1. **`command: ["sleep", "infinity"]`**: **Crucial:** Replace this with the command that should run inside your container. `sleep infinity` is useful to just start the container and keep it running so you can `docker exec` into it for testing, or if it's running a background service.

**How to Use:**

1. Save the code above as `docker-compose.yml`.
2. Create a directory named `custom-proj-grids` in the same location as the `docker-compose.yml` file.
3. Place your `.gsb` files inside the `custom-proj-grids` directory.
4. **Modify** the `image:` line to point to your actual GDAL image.
5. **Verify** the `/usr/share/proj` path in the `PROJ_DATA` variable is correct for your image. If not, change it.
6. **Modify** the `command:` line to run your actual application or desired process.
7. Open a terminal in the directory containing the `docker-compose.yml` file.
8. Run `docker-compose up -d` to build (if necessary) and start the container in detached mode.
9. Your GDAL/PROJ tools inside the container should now be able to find and use the `.gsb` files located in `/opt/proj-custom-grids` when needed for transformations.

# BUILD MULTISTAGE

Implementa nel seguente dockerfile una build multi-stage.

Non modificare il meccanismo di build attuale.

Nella immagine finale devono essere presenti e funzionanti gli applicativi gdal/ogr e il binding con python

Certamente! Ecco il Dockerfile modificato per implementare una build multi-stage, mantenendo il meccanismo di build originale e garantendo la presenza e funzionalità di GDAL/OGR con i binding Python nell'immagine finale.

**Spiegazione delle modifiche:**

1. **Stage `builder`:**
    - Questo stage contiene tutto il necessario per *compilare* GDAL e le sue dipendenze (come `libecw`).
    - Include l'installazione di tutti i pacchetti `dev`, gli strumenti di compilazione (`build-essential`, `cmake`, `g++`, `swig`, ecc.), il download e l'installazione di Oracle Instant Client SDK e la compilazione di `libecw` e GDAL stesso.
    - L'intero processo di build originale è contenuto in questo stage.
1. **Stage Finale (Immagine Risultante):**
    - Questo stage parte da una base pulita (`ubuntu:22.04`).
    - Installa *solo* le dipendenze *runtime* necessarie per eseguire GDAL, Python, Oracle Client e `libecw`. Questo esclude tutti i pacchetti `dev`, i compilatori e altri tool non necessari nell'immagine finale, riducendone significativamente le dimensioni.
    - Imposta le variabili d'ambiente necessarie per Oracle (`ORACLE_HOME`, `LD_LIBRARY_PATH`, etc.) e per `libecw`.
    - Utilizza `COPY --from=builder` per copiare selettivamente solo gli artefatti compilati e le librerie necessarie dallo stage `builder`:
        - Le librerie `libecw` compilate (`/usr/local/lib/`).
        - Le librerie e i file di Oracle Instant Client (`$ORACLE_BASE`).
        - Le librerie GDAL compilate (`/usr/lib/libgdal.so*`).
        - I file di dati GDAL (`/usr/share/gdal`).
        - Gli eseguibili GDAL/OGR (`/usr/bin/gdal*`, `/usr/bin/ogr*`).
        - I binding Python di GDAL (copiati nella directory `site-packages` di Python).
    - Esegue `ldconfig` per assicurarsi che il sistema trovi le librerie condivise copiate (Oracle, libecw, GDAL).

```other
# Stage 1: Builder - Compila GDAL con tutte le dipendenze
FROM ubuntu:22.04 AS builder

ARG GDAL_VERSION=3.10.0
ENV PLATFORM=arm64

# Environment variables per la build
ENV DEBIAN_FRONTEND=noninteractive
ENV ORACLE_BASE=/usr/lib/oracle
ENV ORACLE_HOME=$ORACLE_BASE/instantclient_19_26
ENV LD_LIBRARY_PATH=$ORACLE_BASE/instantclient_19_26
ENV PATH=$ORACLE_HOME:$PATH
ENV TNS_ADMIN=$ORACLE_HOME/network/admin

# Installazione dipendenze di build iniziali + tools + libecw build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ build-essential autoconf automake m4 libtool gcc make unzip wget swig patch \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install libecwj2 (ECW 3.3 SDK)
COPY lib_ecw /tmp/lib_ecw
# VERSIONE MAC OS --build=aarch64-unknown-linux-gnu --> Corretto per build Linux ARM64
RUN cd /tmp/lib_ecw \
    && unzip libecwj2-3.3-2006-09-06.zip \
    && patch -p0 < libecwj2-3.3-msvc90-fixes.patch \
    && cd libecwj2-3.3 \
    && ./configure --build=aarch64-unknown-linux-gnu \
    && make -j$(nproc) \
    && make install \
    && ldconfig \
    && cd / \
    && rm -rf /tmp/lib_ecw

# Installazione dipendenze di build per GDAL (librerie -dev)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    apt-transport-https \
    gnupg \
    lsb-release \
    cmake \
    libaio1 \
    libsqlite3-dev \
    libexpat1-dev \
    libgeos-dev \
    libproj-dev \
    libpq-dev \
    libtiff-dev \
    libpng-dev \
    libjpeg-dev \
    libgif-dev \
    libwebp-dev \
    libzstd-dev \
    libxml2-dev \
    python3 python3-pip python3-dev python3-numpy \
    libjson-c-dev \
    libcurl4-openssl-dev \
    liblzma-dev \
    libgeotiff-dev \
    pkg-config \
    libssl-dev && \
    curl -fsSL https://apache.jfrog.io/artifactory/arrow/ubuntu/apache-arrow-apt-source-latest-$(lsb_release -cs).deb -O && \
    apt-get install -y ./apache-arrow-apt-source-latest-$(lsb_release -cs).deb && \
    rm apache-arrow-apt-source-latest-$(lsb_release -cs).deb && \
    apt-get update && \
    apt-get install -y \
    libarrow-dev \
    libarrow-dataset-dev \
    libparquet-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia ed estrae Oracle Instant Client (richiede SDK per la build di GDAL)
COPY ./oracle_zip_$PLATFORM/instantclient-basic-linux.$PLATFORM-19.26.0.0.0dbru.zip /tmp/
COPY ./oracle_zip_$PLATFORM/instantclient-sdk-linux.$PLATFORM-19.26.0.0.0dbru.zip /tmp/
COPY ./oracle_zip_$PLATFORM/instantclient-sqlplus-linux.$PLATFORM-19.26.0.0.0dbru.zip /tmp/

RUN mkdir -p $ORACLE_BASE && \
    cd $ORACLE_BASE && \
    unzip -q /tmp/instantclient-basic-linux.$PLATFORM-19.26.0.0.0dbru.zip && \
    unzip -q /tmp/instantclient-sdk-linux.$PLATFORM-19.26.0.0.0dbru.zip && \
    unzip -q /tmp/instantclient-sqlplus-linux.$PLATFORM-19.26.0.0.0dbru.zip && \
    rm -f /tmp/instantclient-*.zip && \
    # Crea i symlink necessari per la build e runtime
    ln -sf $ORACLE_HOME/libclntsh.so.19.1 $ORACLE_HOME/libclntsh.so && \
    ln -sf $ORACLE_HOME/libocci.so.19.1 $ORACLE_HOME/libocci.so && \
    # Configura ldconfig per la build
    echo $ORACLE_HOME > /etc/ld.so.conf.d/oracle.conf && ldconfig

# Download e build di GDAL con supporto Oracle OCI, ECW e Python bindings
RUN cd /tmp && \
    wget -q https://github.com/OSGeo/gdal/releases/download/v${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz && \
    tar -xzf gdal-${GDAL_VERSION}.tar.gz && \
    cd gdal-${GDAL_VERSION} && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr \
        -DBUILD_SHARED_LIBS=ON \
        -DGDAL_USE_TIFF=ON \
        -DGDAL_USE_GEOTIFF=ON \
        -DGDAL_USE_PNG=ON \
        -DGDAL_USE_JPEG=ON \
        -DGDAL_USE_GIF=ON \
        -DGDAL_USE_WEBP=ON \
        -DGDAL_USE_ZSTD=ON \
        -DGDAL_USE_GEOS=ON \
        -DGDAL_USE_CURL=ON \
        -DGDAL_USE_POSTGRESQL=ON \
        -DGDAL_USE_ARROW=ON \
        -DGDAL_USE_PARQUET=ON \
        -DBUILD_PYTHON_BINDINGS=ON \
        -DGDAL_USE_ECW=ON \
        -DECW_INCLUDE_DIR=/usr/local/include \
        -DECW_LIBRARY=/usr/local/lib/libNCSEcw.so \
        -DGDAL_USE_ORACLE=ON \
        -DOracle_INCLUDE_DIR=$ORACLE_HOME/sdk/include \
        -DOracle_LIBRARY=$ORACLE_HOME/libclntsh.so \
        -DOracle_LIBRARY_DIR=$ORACLE_HOME \
        -DOracle_ROOT=$ORACLE_HOME && \
    make -j$(nproc) && \
    make install DESTDIR=/build-output && \
    cd / && \
    rm -rf /tmp/gdal-${GDAL_VERSION} /tmp/gdal-${GDAL_VERSION}.tar.gz

# NOTA: make install DESTDIR=/build-output è opzionale ma può aiutare a separare gli output della build
# Se non si usa DESTDIR, gli artefatti verranno installati direttamente in /usr, /usr/local etc.
# In questo caso, useremo i path assoluti standard (/usr, /usr/local) per semplicità nel COPY successivo

# Verifica opzionale installazione nello stage builder
# RUN /usr/bin/ogrinfo --formats | grep Oracle

# --------------------------------------------------------
# Stage 2: Final Image - Contiene solo runtime e artefatti compilati
FROM ubuntu:22.04

ARG GDAL_VERSION
ENV PLATFORM=arm64 # Potrebbe non essere necessario qui, ma lo manteniamo per coerenza

# Variabili d'ambiente necessarie al runtime
ENV DEBIAN_FRONTEND=noninteractive
ENV ORACLE_BASE=/usr/lib/oracle
ENV ORACLE_HOME=$ORACLE_BASE/instantclient_19_26
# Assicurarsi che LD_LIBRARY_PATH includa sia Oracle che libecw
ENV LD_LIBRARY_PATH=$ORACLE_HOME:/usr/local/lib
ENV PATH=$ORACLE_HOME:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin # Aggiunto ORACLE_HOME a PATH
ENV TNS_ADMIN=$ORACLE_HOME/network/admin
# Potrebbe essere necessario impostare anche GDAL_DATA se non trovato automaticamente
# ENV GDAL_DATA=/usr/share/gdal

# Installazione solo delle dipendenze RUNTIME
# Nota: python3-numpy è necessario anche al runtime per i bindings
# Nota: libgdal-dev e gdal-bin NON sono necessari qui perché li abbiamo compilati/copiati
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    lsb-release \
    libaio1 \
    libsqlite3-0 \
    libexpat1 \
    libgeos-c1v5 \
    libproj22 \
    libpq5 \
    libtiff5 \
    libpng16-16 \
    libjpeg-turbo8 \
    libgif7 \
    libwebp7 \
    libzstd1 \
    libxml2 \
    python3 python3-numpy \
    libjson-c5 \
    libcurl4 \
    liblzma5 \
    libgeotiff5 \
    libssl3 \
    # Dipendenze runtime per Arrow/Parquet (ottenute dal repo aggiunto nello stage builder)
    # È necessario aggiungere nuovamente il repository qui o installare i .deb manualmente
    && curl -fsSL https://apache.jfrog.io/artifactory/arrow/ubuntu/apache-arrow-apt-source-latest-$(lsb_release -cs).deb -O \
    && apt-get install -y ./apache-arrow-apt-source-latest-$(lsb_release -cs).deb \
    && rm apache-arrow-apt-source-latest-$(lsb_release -cs).deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       libarrow1000 \
       libarrow-dataset1000 \
       libparquet1000 \
    # Pulizia
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia artefatti compilati e librerie dallo stage builder
COPY --from=builder /usr/local/lib/libNCSEcw* /usr/local/lib/
COPY --from=builder $ORACLE_BASE $ORACLE_BASE
COPY --from=builder /usr/lib/libgdal.so* /usr/lib/
COPY --from=builder /usr/share/gdal /usr/share/gdal
COPY --from=builder /usr/bin/gdal* /usr/bin/
COPY --from=builder /usr/bin/ogr* /usr/bin/
# Il path esatto per i binding python può variare leggermente a seconda della versione di python/ubuntu
# Controllare il path nello stage builder se questo non funziona
COPY --from=builder /usr/lib/python3/dist-packages/osgeo /usr/lib/python3/dist-packages/osgeo
COPY --from=builder /usr/lib/python3/dist-packages/GDAL*.egg-info /usr/lib/python3/dist-packages/

# Configura il dynamic linker per trovare le librerie copiate
RUN echo $ORACLE_HOME > /etc/ld.so.conf.d/oracle.conf && \
    echo /usr/local/lib > /etc/ld.so.conf.d/libecw.conf && \
    ldconfig

# Verifica opzionale (richiede python3)
# RUN python3 -c "from osgeo import gdal; print(gdal.__version__)"
# RUN ogrinfo --formats | grep Oracle

# Comando di default
CMD ["/bin/bash"]
```

# GDAL OCI

GOAL

Build a docker image with the following:

- based on ubuntu 22.04
- ORACLE CLIENT: install oracle instantclient versione 19.26 using the .zip files stored in a folder on the host machine
    - oracle_zip_arm64
- GDAL: do not use gdal-bin but compile gdal from source
    - version 3.10 (parametrize the gdal version to install)
    - make sure to install all required dev library (libgeotiff-dev, libproj-dev, etc.)
    - compile with support for oracle, postgres, geoparquet

GIVE ME

- the dockerfile
- the build command on arm64 platform
- the run command to test if oci support is correctly installed

Okay, let's set up the Dockerfiles and commands for building GDAL with Oracle OCI support using local Instant Client zip files.

**Prerequisites on Host Machine:**

1. **Docker:** Ensure Docker is installed and running.
2. **Oracle Instant Client Zip Files:**
    - Download the **Basic Light** (or Basic) and **SDK** packages for **version 19.26** from the Oracle Instant Client Downloads page. You'll need separate downloads for Linux x86-64 (amd64) and Linux ARM (aarch64) (arm64).
    - Create the following directory structure in the same directory where you will run the `docker build` command:

```other
.
├── oracle_zip_amd64/
│   ├── instantclient-basiclite-linux.x64-19.26.0.0.0dbru.zip
│   └── instantclient-sdk-linux.x64-19.26.0.0.0dbru.zip
├── oracle_zip_arm64/
│   ├── instantclient-basiclite-linux.arm64-19.26.0.0.0dbru.zip
│   └── instantclient-sdk-linux.arm64-19.26.0.0.0dbru.zip
├── Dockerfile.amd64
└── Dockerfile.arm64
```

        *(Replace the zip filenames with the exact names you downloaded if they differ slightly)*

**1. Dockerfile for amd64 (Dockerfile.amd64)**

```other
# Base image for amd64
FROM --platform=linux/amd64 ubuntu:22.04

ARG GDAL_VERSION=3.10.0
ARG ORACLE_CLIENT_VERSION_MAJOR=19
ARG ORACLE_CLIENT_VERSION_FULL=19.26

# Set environment variables non-interactively
ENV DEBIAN_FRONTEND=noninteractive
ENV ORACLE_HOME=/opt/oracle/instantclient_${ORACLE_CLIENT_VERSION_MAJOR}_${ORACLE_CLIENT_VERSION_FULL}
ENV LD_LIBRARY_PATH=${ORACLE_HOME}
ENV PATH=${ORACLE_HOME}:${PATH}

# Install essential packages and Oracle dependencies
RUN apt-get update && \\
    apt-get install -y --no-install-recommends \\
    wget \\
    unzip \\
    libaio1 \\
    # Build dependencies for GDAL
    build-essential \\
    pkg-config \\
    cmake \\
    libsqlite3-dev \\
    libproj-dev \\
    libcurl4-openssl-dev \\
    libtiff-dev \\
    libgeotiff-dev \\
    python3-dev \\
    swig \\
    ca-certificates && \\
    rm -rf /var/lib/apt/lists/*

# Install Oracle Instant Client for amd64
WORKDIR /tmp/oracle_install
COPY oracle_zip_amd64/*.zip ./

# Unzip Oracle files
RUN unzip instantclient-basiclite-linux.x64-${ORACLE_CLIENT_VERSION_FULL}.0.0.0dbru.zip -d /opt/oracle && \\
    unzip instantclient-sdk-linux.x64-${ORACLE_CLIENT_VERSION_FULL}.0.0.0dbru.zip -d /opt/oracle && \\
    # Rename the created directory to match ORACLE_HOME
    mv /opt/oracle/instantclient_${ORACLE_CLIENT_VERSION_MAJOR}.* ${ORACLE_HOME} && \\
    # Create symbolic link for libclntsh.so (needed by some linkers)
    ln -s ${ORACLE_HOME}/libclntsh.so.${ORACLE_CLIENT_VERSION_MAJOR}.1 ${ORACLE_HOME}/libclntsh.so && \\
    # Configure dynamic linker
    echo ${ORACLE_HOME} > /etc/ld.so.conf.d/oracle-instantclient.conf && \\
    ldconfig && \\
    # Clean up zip files
    rm -rf /tmp/oracle_install

# Download and compile GDAL
WORKDIR /tmp/gdal_install
RUN wget <http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz> && \\
    tar -xzf gdal-${GDAL_VERSION}.tar.gz && \\
    cd gdal-${GDAL_VERSION} && \\
    ./configure \\
        --prefix=/usr/local \\
        --with-proj=/usr/include \\
        --with-libtiff=internal \\
        --with-geotiff=internal \\
        --with-oci \\
        --with-oci-include=${ORACLE_HOME}/sdk/include \\
        --with-oci-lib=${ORACLE_HOME} && \\
    make -j$(nproc) && \\
    make install && \\
    cd /tmp && \\
    rm -rf /tmp/gdal_install && \\
    # Run ldconfig again to include GDAL libs
    ldconfig

# Clean up build dependencies (optional, reduces image size)
# RUN apt-get purge -y --auto-remove build-essential pkg-config cmake <other build-deps> && \\
#     apt-get clean && \\
#     rm -rf /var/lib/apt/lists/*

# Verify OCI driver (optional, can be done in run command too)
RUN gdalinfo --formats | grep -i oci

WORKDIR /

# Set default command (optional)
# CMD ["bash"]
```

**2. Dockerfile for arm64 (Dockerfile.arm64)**

This file is almost identical to the amd64 version, only changing the `COPY` source directory and the specific Instant Client zip filenames it expects and extracts.

```other
# Base image for arm64
FROM --platform=linux/arm64 ubuntu:22.04

ARG GDAL_VERSION=3.10.0
ARG ORACLE_CLIENT_VERSION_MAJOR=19
ARG ORACLE_CLIENT_VERSION_FULL=19.26

# Set environment variables non-interactively
ENV DEBIAN_FRONTEND=noninteractive
ENV ORACLE_HOME=/opt/oracle/instantclient_${ORACLE_CLIENT_VERSION_MAJOR}_${ORACLE_CLIENT_VERSION_FULL}
ENV LD_LIBRARY_PATH=${ORACLE_HOME}
ENV PATH=${ORACLE_HOME}:${PATH}

# Install essential packages and Oracle dependencies
RUN apt-get update && \\
    apt-get install -y --no-install-recommends \\
    wget \\
    unzip \\
    libaio1 \\
    # Build dependencies for GDAL
    build-essential \\
    pkg-config \\
    cmake \\
    libsqlite3-dev \\
    libproj-dev \\
    libcurl4-openssl-dev \\
    libtiff-dev \\
    libgeotiff-dev \\
    python3-dev \\
    swig \\
    ca-certificates && \\
    rm -rf /var/lib/apt/lists/*

# Install Oracle Instant Client for arm64
WORKDIR /tmp/oracle_install
COPY oracle_zip_arm64/*.zip ./

# Unzip Oracle files
RUN unzip instantclient-basiclite-linux.arm64-${ORACLE_CLIENT_VERSION_FULL}.0.0.0dbru.zip -d /opt/oracle && \\
    unzip instantclient-sdk-linux.arm64-${ORACLE_CLIENT_VERSION_FULL}.0.0.0dbru.zip -d /opt/oracle && \\
    # Rename the created directory to match ORACLE_HOME
    mv /opt/oracle/instantclient_${ORACLE_CLIENT_VERSION_MAJOR}.* ${ORACLE_HOME} && \\
    # Create symbolic link for libclntsh.so (needed by some linkers)
    ln -s ${ORACLE_HOME}/libclntsh.so.${ORACLE_CLIENT_VERSION_MAJOR}.1 ${ORACLE_HOME}/libclntsh.so && \\
    # Configure dynamic linker
    echo ${ORACLE_HOME} > /etc/ld.so.conf.d/oracle-instantclient.conf && \\
    ldconfig && \\
    # Clean up zip files
    rm -rf /tmp/oracle_install

# Download and compile GDAL
WORKDIR /tmp/gdal_install
RUN wget <http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz> && \\
    tar -xzf gdal-${GDAL_VERSION}.tar.gz && \\
    cd gdal-${GDAL_VERSION} && \\
    ./configure \\
        --prefix=/usr/local \\
        --with-proj=/usr/include \\
        --with-libtiff=internal \\
        --with-geotiff=internal \\
        --with-oci \\
        --with-oci-include=${ORACLE_HOME}/sdk/include \\
        --with-oci-lib=${ORACLE_HOME} && \\
    make -j$(nproc) && \\
    make install && \\
    cd /tmp && \\
    rm -rf /tmp/gdal_install && \\
    # Run ldconfig again to include GDAL libs
    ldconfig

# Clean up build dependencies (optional, reduces image size)
# RUN apt-get purge -y --auto-remove build-essential pkg-config cmake <other build-deps> && \\
#     apt-get clean && \\
#     rm -rf /var/lib/apt/lists/*

# Verify OCI driver (optional, can be done in run command too)
RUN gdalinfo --formats | grep -i oci

WORKDIR /

# Set default command (optional)
# CMD ["bash"]
```

**3. Build Commands**

Make sure you are in the directory containing the `Dockerfile.*` files and the `oracle_zip_*` subdirectories.

- **For amd64:**

```bash
docker build --platform linux/amd64 \\
             --build-arg GDAL_VERSION=3.10.0 \\
             -t gdal-oci:3.10-amd64 \\
             -f Dockerfile.amd64 .
```

    *(If you are building on an amd64 machine, you might be able to omit `--platform linux/amd64`, but explicitly stating it is safer).*

- **For arm64:**

```bash
docker build --platform linux/arm64 \\
             --build-arg GDAL_VERSION=3.10.0 \\
             -t gdal-oci:3.10-arm64 \\
             -f Dockerfile.arm64 .
```

    *(If you are building on an arm64 machine (like a Raspberry Pi 4/5, AWS Graviton, or Apple Silicon Mac with Docker configured for arm64), you might omit `--platform linux/arm64`. If you are cross-compiling from an amd64 machine, you must specify `--platform linux/arm64` and ensure your Docker setup supports cross-platform builds, possibly requiring QEMU setup via `docker buildx`)*.

**4. Run Command to Test OCI Support**

Use the appropriate tag based on the image you built or the platform you want to run on.

- **Testing the amd64 image:**

```bash
docker run --rm -it gdal-oci:3.10-amd64 gdalinfo --formats | grep -i OCI
```

- **Testing the arm64 image:**

```bash
docker run --rm -it gdal-oci-arm64 gdalinfo --formats | grep -i OCI
```

**Expected Output:**

If the build and OCI integration were successful, you should see a line similar to this in the output:

```other
OCI -raster,vector- (rw+): Oracle Spatial
```

The `(rw+)` indicates read/write support for vector data, and the presence of the line confirms the OCI driver was compiled and detected by GDAL.
