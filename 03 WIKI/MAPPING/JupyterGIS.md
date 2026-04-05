---
title: JupyterGIS
source: https://blog.jupyter.org/jupytergis-d63b7adf9d0c
author:
  - "[[Sylvain Corlay]]"
published: 2024-06-12
created: 2026-04-04
description: JupyterGIS Pioneering Web-based, Collaborative, and Open-source GIS Tools By Sylvain Corlay [1], Anne Fouilloux [2], and Monika Weissschnur [3] We are thrilled to announce that the European Space …
tags:
  - clippings
  - mapping
topic:
type: note
---
[Sitemap](https://blog.jupyter.org/sitemap/sitemap.xml)## [Jupyter Blog](https://blog.jupyter.org/?source=post_page---publication_nav-95916e268740-d63b7adf9d0c---------------------------------------)

[![Jupyter Blog](https://miro.medium.com/v2/resize:fill:76:76/1*VigrxIzP3-wH7oxoPULjrA.png)](https://blog.jupyter.org/?source=post_page---post_publication_sidebar-95916e268740-d63b7adf9d0c---------------------------------------)

The Jupyter Blog

![The logo of Project Jupyter next to a stylised terrestrial globe](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*IkYCf2cbk3SaxaROQ0eUsA.png)

The logo of Project Jupyter next to a stylised terrestrial globe

Pioneering Web-based, Collaborative, and Open-source GIS Tools

*By Sylvain Corlay \[1\], Anne Fouilloux \[2\], and Monika Weissschnur \[3\]*

We are thrilled to announce that the European Space Agency (ESA) is funding our proposal “ *Real-time collaboration and collaborative editing for GIS workflows with Jupyter and QGIS*.”

The consortium spearheading this project comprises [QuantStack](https://quantstack.net/) and [Simula Research Lab](https://www.simula.no/) (Simula), two organizations with a long history of contributions to the Jupyter project and the broader open-source scientific computing ecosystem.

The goal of the project is to build solid foundations for a versatile web-based user interface for Geographic Information Systems (GIS) workflows. It will comprise several components, including a JupyterLab extension for collaboratively editing QGIS project files and the integration of these APIs in the Jupyter Notebook. We will then explore integration with platforms like the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (CDSE) and the [European Open Science Cloud](https://eosc.eu/) (EOSC).

## Collaborative workflows in geosciences

Collaborative editing of documents has become an integral part of our digital lives and has made us collectively more productive. Gone are the days of cumbersome email exchanges with documents shuttling back and forth.

Looking ahead, the potential of co-editing extends far beyond text documents and will apply to all authoring UIs, from CAD to image processing. We think that the shift to collaborative editing will be even more transformative for larger and more complex projects, which are inherently social and require the concerted effort of large teams. Whether you are designing a stadium, a plane, or an ocean liner, you need to coordinate a diverse expertise to build a unified model. In geosciences, it may range from climate modeling to agriculture, ecology, urban planning, and many more areas of expertise. For such endeavors, we must embrace tools favoring collaboration, and this applies to the future web-based user interfaces for geoscience research.

We have been working on collaborative editing in the core of JupyterLab for the past three years. Our approach is based on the [Yjs framework](https://yjs.dev/), an implementation of CRDT data structures (Conflict-free Replicated Data Type). We have learned that since it is so tied to the data model, retrofitting these features into an existing application is considerably more arduous than building the initial data model on the appropriate paradigm from inception. This is why JupyterGIS will be built from the ground up with collaborative editing in mind.

*JupyterGIS will be the first open-source GIS tool to provide collaborative editing features.*

Importantly, JupyterGIS is part of a broader mission to enable collaborative workflows in open-source technical computing. The [JupyterCAD](https://blog.jupyter.org/collaborative-cad-in-jupyterlab-8eb9e8f81f0) project, a collaborative CAD modeler, is another example of this endeavor. By sharing knowledge and resources, both JupyterGIS and JupyterCAD will benefit from and contribute to each other’s progress, ultimately driving innovation and productivity in their respective fields.

## From the desktop to the web

Advanced authoring tools, including IDEs, CAD modelers, image processing software, and GIS applications, are essential for professionals who rely on them for extended periods. These users have high expectations and demand key features to optimize their productivity and workflow. Among these features are extensibility with plugins, configurable keyboard shortcuts, themability, internationalization, scriptability, a unified settings system, and the ability to operate across multiple browser windows and devices.

Developing a new application from the ground up that meets all these requirements is a formidable challenge. This is where the JupyterLab application framework proves invaluable. By leveraging this framework, developers can build custom, feature-rich authoring tools that incorporate these essential features from the outset, making it an ideal solution for creating modern, user-centric applications.

Beyond the pure authoring user interface, for which JupyterLab is a great tool, it is also the *perfect* tool for integration with notebook-based workflows. As part of this project, we will develop an advanced Python API to manage JupyterGIS sessions, leveraging Jupyter’s robust display system to incorporate sophisticated GIS features inline in Jupyter notebooks and consoles. This integration will further enhance the capabilities and versatility of our application. This feature will follow the same architecture as that of JupyterCAD for the integration with the notebook user interface.

## Real-world applications

JupyterGIS is meant to become a *general-purpose* tool. However, we will work with teams of practitioners on *specific* real-world applications to ensure that it addresses their needs.

One such project concerns the use of digital and GIS solutions for emergency management. While practitioners involved in emergency management already have experience with such tools, we are convinced that web-based applications built with collaboration in mind from the start can foster improved coordination and collaboration, and therefore the effectiveness of the response.

Response teams comprise different organizations, including the affected municipalities, police, emergency response organizations like the Red Cross, and advisers such as the U.S. Army Corps of Engineers (USACE) in the United States or the Norwegian Water Resources and Energy Directorate (NVE) in Norway. Even when using the same incident management system, miscommunications and misunderstandings can occur between these stakeholders, resulting in delays or improper use of resources. An improved integration of collaborative GIS software can improve upon the existing tooling.

## Building collaborations in Europe and beyond

We will partner with key practitioners and make sure JupyterGIS addresses their use cases. Integration in the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (CDSE) and the [European Open Science Cloud](https://eosc.eu/) (EOSC) will be key to the adoption of JupyterGIS and demonstrate its deployment in such environments.

Beyond Europe, we are currently working on including this project into a broader scope.We are excited to be partnering with the “ [LIVE-Env](https://www.live-env.org/) ” project, an open-source initiative spearheaded by Alyssa Goodman at Harvard University. Furthermore, we are establishing a key collaboration with the [Berkeley Institute for Data Sciences](https://bids.berkeley.edu/home) (BIDS) and the [Schmidt Center for Data Science and Environment](https://dse.berkeley.edu/) (DSE) at UC Berkeley and [2i2c](https://2i2c.org/), with a focus on Jupyter-based geosciences.

## Affiliations

\[1\] [QuantStack  
](https://quantstack.net/)\[2\] [Simula  
](https://www.simula.no/)\[3\] [Simula](https://www.simula.no/)

[![Sylvain Corlay](https://miro.medium.com/v2/resize:fill:96:96/0*n-JT2lBRip5wuFWH.jpg)](https://medium.com/@SylvainCorlay?source=post_page---post_author_info--d63b7adf9d0c---------------------------------------)

[![Sylvain Corlay](https://miro.medium.com/v2/resize:fill:128:128/0*n-JT2lBRip5wuFWH.jpg)](https://medium.com/@SylvainCorlay?source=post_page---post_author_info--d63b7adf9d0c---------------------------------------)

[15 following](https://medium.com/@SylvainCorlay/following?source=post_page---post_author_info--d63b7adf9d0c---------------------------------------)

@ProjectJupyter core developer, #PyData Paris Meetup organizer, co-author of #xtensor, entrepreneur, mathematician, quant, #cpp #python #JuliaLang #dataviz