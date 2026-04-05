---
title: "DuckDB Spatial: Supercharged Geospatial SQL (GeoPython 2024)"
source: "https://www.youtube.com/watch?v=hoyQnP8CiXE"
author:
  - "[[DuckDB]]"
published: 2024-08-02
created: 2026-04-04
description: "Speaker: Max Gabrielsson (DuckDB Labs)Slides: https://blobs.duckdb.org/papers/duckdb-spatial-geopython-2024.pdf"
tags:
  - "clippings"
topic:
type: "note"
---
![](https://www.youtube.com/watch?v=hoyQnP8CiXE)

Speaker: Max Gabrielsson (DuckDB Labs)  
Slides: https://blobs.duckdb.org/papers/duckdb-spatial-geopython-2024.pdf

## Transcript

### Introduction

**0:00** · Yeah, this talk is titled like to be spatial supercharged give spatial SQL.

**0:05** · Uh quick info about me. Uh yeah, my name is Max Gabrien. I have a bachelor's in computer science from Upsal University.

**0:12** · I like to say that I'm a fan turned software engineer at D2B Labs. Uh where I mostly work on Dr. B's execution layer and it's gatial extension. Now ductb Labs is a company founded by the duct creators. We're based in Amsterdam.

**0:28** · We're a small company uh currently around 18 people and uh we provide development and support for ductb. All right. So what is ductb?

### What is DuckDB

**0:40** · Ductb is an analytical embedded SQL database. Uh it originally started out as a research project at the CWI research uh national research institute in Amsterdam. Uh it is free and open source MIT licensed. Uh there's no dual license, no open core. You get uh yeah all the code. Uh duct is also very portable. It has no external dependencies. It runs almost everywhere.

**1:09** · Uh and it's currently in pre-release version uh v 0ero 10.3.

**1:15** · Uh despite that it has very extensive Python and uh client integrations to to other data science uh languages. And I think the coolest part about ductb is that it really makes the most out of your laptop.

### Why DuckDB

**1:31** · Now, usually when I talk about ductb in particular to people that come from more of a data science background, uh there is a bit of hesitation or confusion. Why would I want to run like a clunky database engine locally where I have to write my queries in this pseudo English language from the 70s? I have my my notebooks, my my uh data frames. Uh it's so much more nicer, so much faster for me to iterate. Um so let me try to explain why I think ductb will not only make efficient use of your computing resources, but also your time and your patience. So I'm going to try to do that by talking about what I think are the three main focuses of ductb so to speak. Those are execution, storage, and user experience.

**2:21** · So, uh let's just jump right into execution. Basically, any sort of query processing engine, whether or not it's a database or uh some cloud warehouse or a data frame, works in one of three ways. So, the first way is what's called a row at a time execution model. Uh basically if you imagine you want to process a big data set of table tabular data you iterate over all the rows one at a time you chunk like one row through the pipeline at a time. Uh and this is the classic database approach. This is how SQLite postgress SQL server uh yeah almost all classic SQL databases uh work and it's great because it has a very low memory footprint. Um a lot of these these tools are very old. They come from a time where uh RAM memory was very scarce and you could never almost never fit your whole working set in memory at the same time. Uh the downside of this is that it has a very high CPU overhead.

### Execution Models

**3:16** · You spend a lot of CPU cycles not actually like operating on your data but just shuffling rows around and synchronizing between different parts of your pipeline. So the alternative is the column at a time model. And this is like how almost all data frame libraries work. Uh yeah, you basically keep your entire column in memory at the same time and uh it's very efficient to just iterate through that. It's already there for you. Uh you can also if you really want to optimize use this modern SIMD instructions that are present in most CPUs uh to make it go or to implement a lot of operations even faster. Uh the downside of this of course is that you have a very large memory footprint. you need to keep your whole column in memory and any intermediate results also have to be materialized for the whole column.

### Vector at a Time

**4:04** · So uh third way to do it that's becoming very uh uh trendy nowadays I guess is uh the vector at a time model that duct among many use. Uh and it's kind of like a best of both worlds. Instead of operating on a row at a time or at the whole column, you operate on a vector of rows which is yeah like a chunk of rows.

**4:24** · Uh and the trick here is to kind of optimize this vector size so that all of your current working rows fit into your CPU cache. So you don't even have to go out to memory to access it.

**4:37** · Additionally, DUTB is multi-threaded.

**4:39** · Now this isn't actually tied to the the processing model. You can write multi-threaded row at a time and column at a time query engines as well. But it synergizes very well with vectorzed processing uh because it's very natural to parallelize over vectors. Any sort of like lock or synchronization overhead you have in a multi-ended program, you can kind of amortize that over uh your vector instead. Now the reason I bring this up is that parallelism is increasingly is becoming increasingly important uh in 2024. Uh even consumer grade laptops like the M3 uh chip that was announced last year, I think they even came out with a new one just a couple weeks ago, uh have like 16 cores in them, which is a ton of performance you're just leaving on the table if you can't make use of that. Uh, additionally, a kind of cool thing about duct execution model is that it's optionally order preserving, which is uh a behavior that is like explicitly not supported in uh most database engines.

**5:37** · But this kind of gives you the same uh yeah like data frame semantics where you can uh kind of slice and dice rows or tables on the vertical axis and know that your uh input and uh output rows are going to be correlated.

**5:51** · Uh now this is kind of where the a lot of excitement productiveb tends to die down. People learn about the vectorzed execution model. It's really fast. It goes really well in in a lot of benchmarks. Uh they use it to query their CSVs or perk files or whatever.

**6:05** · But I think a critically underrated feature of ductb as well uh especially for people in a more yeah data science background is that ductb as a database engine also provides you with storage.

### Data Science Background

**6:19** · So, okay, why is this important? Uh, here's a picture of every analytics or GIS progress uh project ever, right? You start out thinking, okay, I'm going to keep it clean. I have my data subdirectory. Uh, you get some exported CSV file somewhere. Of course, it's dirty. You have to manually clean it yourself. Uh, you got your shape files.

**6:38** · There's some auxiliary file missing always. Uh, you have some Giojson, but you have to manually split it up into multiple parts because Giojson is a terrible format. Uh you start out with your uh your main Pi, then you realize it's too annoying, so you switch to a notebook instead. Uh at some point, your coworker asks you to send over uh some data, so you just zip everything and drop it into Google Drive. Uh you have your worker script to run some annoying batch in the background. Uh and you know, at some point finally, you realize you get some useful result. You produce your parquet file because you want to leave the world in a better place than you found it. But of course, parquet doesn't do updates. So uh obviously something was wrong and you end up with a dreaded final V2. Um the thing is if you recognize this picture then you need a database. This is the exact problem that like a database is trying to solve managing your data and by not using a database you have offloaded all this work onto you basically.

**7:35** · So uh this is another reason why I think that B is pretty compelling. Uh DB provides a storage back end. It's a common misconception that ductb is an in-memory database. That's not true. Uh ductb has a database file format where similar to sqlite one database is represented as one file. So it's very easy to to share and back up. And uh yeah uh also because this is a proper database it supports updates. You have this these acid uh properties that most databases uh usually provide. Also you have transactions which again criminally underrated feature. Uh even if you are the only one operating on your data in your database, having access to to transactions is great because you can set up this big transformation pipeline in a transaction. You can yeah create tables, delete tables, update tables, whatever. And you know that either all of this is going to succeed or nothing is going to succeed and the database is going to revert back to its previous state. Uh of course you can store multiple tables in one database.

### DuckDB Storage

**8:36** · Uh but internally ductb will also store the columns individually on disk. Uh this is pretty great because ductb also stores past or like per column statistics basically. So it's very fast to search on disk for specific values uh in specific columns. Also because columns are stored separately uh we can apply uh specialized lightweight compression algorithms on these uh data that's like in the same column uh compress usually compresses much better than if you do row wise they have the same data type and usually share the same sort of distribution right so there's no u uh less entropy I guess uh and in practice this can save you almost three to five times uh on storage use and paradoxically this also improves query speed. Even though you're doing more work to compress and decompress, when you're reading data from disk, the bottleneck is not actually your CPU, it's your disk. So, it's much faster to store data compressed and decompress it in memory than it is to store data uncompressed and try to read it back.

**9:40** · Uh, so this is a chart of how uh duct compression has improved throughout the years. This is actually a pretty old uh figure. This is like the last one is 0.6. We're on 0.10 now. We actually have this new compression algorithm out of CWI that is like super state-of-the-art for floating port compression. I don't have any numbers on it, but it replaces both the FSSD and GM. So, uh I expect this uh number to be even better today than it was in 2022.

**10:09** · All right. Lastly, I want to talk about UX. So, D2B has this inprocess deployment model. Um meaning there's no separate server. So there's no config, there's no environment, god forbid, there's no docker. Uh and a great thing about this is that you also have very minimal transfer uh delay overhead to get data in and out of ductb. uh if you have I don't know compute some big uh result in postgress and you want to pull this into your notebook postgress first has to serialize this result into some binary encoding ship that over the wire and then the serialize it back in your client library and then eventually uh it ends up in in in Python or whatever but because ductb runs in process you can skip almost all of that uh this also means it's very easy to run ductb as part of a larger system not just as end user tool but also as a component in u yeah a bigger I don't know data warehousing solution right uh so you can run ductb of course in the back end just slap uh together a fast API server and import ductb uh you can run it in the client if you have some sort of client application it even runs in the browser using wom which of course isn't as fast but it's much faster than javascript uh and it also even runs on your phone and I think my watch but I haven't tried uh now because ductb runs in process it and shares the resources with your program. Uh it tries to be a good guest so to speak uh by doing what we call graceful degradation. Now this doesn't really sound like something a good guest would be up to like you you don't really want to invite somebody over to be gracefully degraded but uh graceful degradation is basically the answer to the question what do you do when you run out of RAM? Uh and in duct case this means that almost all operators the different parts of the database that executes different parts of a query will spill to disk meaning they will offload their intermediate result into a temporary file on your hard drive and then keep processing and then in the end try to reassemble the the final result.

### DuckDB UX

### Graceful Degradation

**12:15** · Um so the idea is that duct should never crash always make progress in some way but this isn't just about not crashing.

**12:25** · Uh this is a figure of uh from a paper very recently published by my dear colleagues uh Lawrence and and Hannes together with Peter Bonds uh comparing duct tob with some other database engines uh running this big kind of group by query where on the x- axis it's uh kind of the size of the data set and the y-axis is ex execution time and all of these databases runs with a me run with a memory limit of 32 gigabytes. So you can see how uh once you reach that 32 gigabyte data set size uh some of these uh engines tend to either abort or time out or they get this really sharp performance spike where they need all of a sudden to read stuff from disk. While DB tries at least to have more of a smooth uh transition to not just immediately hit this wall once you run out of memory. Okay, so these are all things that run kind of under the hood to make ductb or using ductb a more pleasant experience. Uh but we also try to make using ductb for end user nicer.

**13:31** · Uh one of these things is what we call friendly SQL. So uh ductb SQL dialect is the superset of the postgress dialect. We actually use their their like parser implementation uh or used to use anyway. Um so we have a lot of funky syntax uh extensions like first syntax. You can swap the form and the select. Uh you can do group by all uh dynamic column selections which are really nice if you have a tables with a ton of columns. Uh nested types, lambda functions, also a lot of like Python inspired stuff uh like list comprehensions and this kind of unified function call syntax where you can pretend functions are methods. Uh speaking of Python, Dr. B has a very special uh relationship with Python. It is by far I think our most uh well-developed like client integration. Uh we actually have three different Python APIs. So there is the the standard like Python DB API. If you used any other database through Python, this will look familiar uh with connections and cursors and whatnot. Uh we also have this kind of crazy new thing uh where we try to implement a PIS spark compatible API. So the idea is that you can just drop in replace uh your pispark code with ductb instead. Um but I think by far the best way to access ductb is through this relational API. Uh and this is pretty cool because basically how it works is that you kind of chain together uh these operators through Python. But this is a completely lazy API, meaning nothing actually gets executed until you have like one of these terminating statements like show or uh to table or or fetch. Um, and the cool thing about this is is that you can kind of focus on just composing uh your query uh kind of imperatively like it was a data frame, right? But ductb still has access to the entire query plan at once once you call show. So ductb can use all of different uh like optimizations and and query rewriting and reorder your uh operators to be more efficient and you don't have to think about that. You just write it as you you want to. Uh we also have this really cool thing uh about with zero copy data frame interoperability. So in this case you can create like a panace data frame and then query it directly from ductb uh you say from df and ductb will then look up anything in scope that looks like a data frame and uh read that memory immediately.

### DuckDB Python

**16:00** · Uh you can also convert your results back into data frames if you want to continue working in in dataf frame land.

**16:06** · uh use yeah kind of these these methods and functions that ductb doesn't support like plotting right uh and this also works with polars and numpy and pyro as well so yeah it allows you to scan data frames and arrays in scope directly from memory uh yeah as I said polar numpy pandas and pyro uh and this is like a product of being an inrocess database this is only really feasible because we share the same address space as pandas or python in this Uh so the idea is that you can use the best tool for the O. All right. So far what's missing spatial support of course. Uh so ductb has this thing called uh ductb extensions. These are basically compiled code modules I guess or plugins maybe.

### DuckDB Extensions

**16:57** · uh they are downloadable and or loadable at at runtime directly from within DUCD and they can provide types, functions, operators, optimizer rules, uh scans, all kinds of crazy stuff. Uh you can write your own if you're proficient in in C++. Uh but at DB Labs, our philosophy is basically that anything that isn't essential to Dr. B should be an extension. Uh so we basically support and provide all of the yeah available extensions that you would use in practice uh like extensions adding JSON support integrations with postgress my SQL SQL lights u AWS ashure uh yeah and of course spatial socatial is uh the extension that I've been working on during my time at labs it is a uh official extension supported extension uh by us that adds your special capabilities. It does this through this simple features vector geometry type. Uh yeah, so you can store points and polygons and line strings. Uh all that good stuff. Um and this is kind of modeled after what PostgJS supports.

### Spatial

**18:09** · DuctB itself is kind of inspired by Postgress. So it makes sense that we uh try to follow what PostJS does for the spatial extension. It's also kind of where my uh background in in JS uh where I have most experience. So we're not like fully compatible yet but we provide if you count overloads 100 plus of these SD functions already. So uh most things are there. Now crucially like ductb this extension doesn't have any runtime dependencies. Uh we actually statically bundle g.js and proy into the binary. So we will never conflict with whatever you have installed locally. Uh we also embed like the whole default pro prediction database. Uh so DB will or DB special will recognize like over 3,000 uh like of the most common CRS uh definitions out of the box. Uh and of course we ship this as pre-built binaries for over 10 platforms. So it's supported in uh Windows, Linux, Mac OS, even web assembly. All right. So quick uh demo um of using the special extension together with uh some some Python. Uh first off, we just import duct. Uh we're gonna install and load a special extension. It looks like this. You just write a SQL install special load special. That's it. No other setup required. Um we're going to I have this uh this extract of the New York City taxi data set uh with 1 million rides in paret format. We're going to create this relation uh to to uh that basically scans this paret file. Um, now we can also execute. We're going to drop down into SQL for a bit and execute this summarize class. It's not exposed into the Python API yet, but uh, basically summarize will compute a bunch of statistics uh, for any query. And but we really just care about column name, column type to figure out what this perk file really contains, right? So that's going to look like this. Um now yeah the only thing we really care about here is the the pickup longitude and latitude and I think the the trip uh distance as well. So we are going to convert these latitude and longitudes into geometries using this sd function. Uh if you're familiar with postgress or postjs this should all uh not come as any surprise to you. Um so yeah we execute the selection and then call to table to actually create a table in our database from this relation. Now this longitude or latitude and longitude is in VJS 84.

### Demo

**20:45** · Uh this taxi data set of course is localized to New York City. So let's also transform it into uh uh a CRS that is more suited for this this region uh using the transform function where you pass a source and a target uh SR.

**21:02** · Now, okay, if you look at this and think, wait a minute, I thought the whole thing with the Python API was that I didn't have to write SQL. This looks like an awful lot of SQL, don't worry, I got you. So, uh, normally when we pass kind of expressions through this relation API, you can pass it as a SQL string and duct will then figure out and parse this, uh, realizing that okay, this point is a SD point is a function.

**21:23** · Pick up latitude and pick up longitude are both columns that are in scope. Uh but you can also create this expression manually through Python using this function expression class where you pass the function name and then any parameters. Now okay we have kind of hardcoded column names here. So let's create a function instead that returns this expression. So it's going to look like this instead.

**21:44** · Uh so we now created this make point uh function that is converted into or returns a ductive expression to create point. Uh we're going to do this with transform as well in which case it looks like this. Now in transform the parameters are strings right the ids. So we're going to use this constant expression instead of just passing a normal string to really tell ductb that this is a string. Don't try to think about this as a column. Um and we're going to be a little bit cheeky. We're going to attach this to the expression class itself. I know this is like not really uh this is kind of frowned upon in Python but uh we're going to do it anyway. So now that we have these helper functions that produce expressions, instead of having this big SQL string, we can use them instead. And it's going to look like this. Much nicer. Uh right.

**22:34** · So we have our data now as uh or we have this express or relation to create geometries. Um it would be nice if we could also use our spatial knowledge to do some data cleaning. If you worked with this taxi data set before, you know it's a very uh noisy and messy and kind of dirty data set. So I'm going to convert our relation back to a relation and also add this distance uh expression to to calculate the distance between the pickup point and the drop off points. Uh this sr uh 102718 prediction is in feet. So I'm going to divide it by 5,280 to turn it into kilometers again, which is the same unit used by the trip distance in the original data set. U so now we can filter out and say, okay, how many of our taxi rides have a trip distance that is smaller than the aerial distance, right? That doesn't really make sense.

**23:30** · Um so if we count that, it's going to tell us 65,000, right? So for a million rides, this is a yeah, pretty dirty data set, I'd say. And now we instead of uh computing this count, I'm actually going to turn this back into a table producing relation, but uh injecting the filter uh instead.

**23:55** · So we now have created this kind of cleaned or a little bit cleaned at least right data sets. Uh let's also look at creating some taxi zones. So I mentioned that DB specially integrates with JO uh out of the box. So you can check any all of the or list all of the GTO drivers available to you by invoking this SD driver table function and it's going to look like this. Uh now the really thing that I'm really interested in here is of course shape shape shape file support.

**24:26** · Uh so it's good to see that that's supported. Uh I happen to have the shape files uh locally. So I'm going to invoke this st read function provided by activity spatial that basically calls into gol to read any sort of spatial data sets. Um now I'm going to join this with my uh cleaned rides and use the the st within spatial predicates to get all of the uh to join yeah all the rides with the zones that they are drop somebody off in. Uh now I'm also going to aggregate this to kind of count how many uh how many trips was was in need sown. I'm going to sort them by descending. And if I then call show and finally execute this expression or relation uh I'm going to get this result. Cool. But wouldn't it be great if we could also visualize this result some way? Of course. Even though duct can't do it, I know somebody who can. So I'm going to change this aggregation to also return the uh the geometry of the zone but I'm going to convert it into WKT. Um now I'm going to turn this relation then into a pandas data frame which I'm going to turn into a gi pandas data frame which I then can plot and then it looks like this.

**25:48** · All right. So this was kind of like a baby example of how to use spatial together with uh Python. Um actually I think if you were to do this in Gopandas like straight up it would probably be faster because this data set is not really uh big enough or the queries aren't really complex enough productive bit to really uh shine. I mean everything fits handily in memory. Um but hopefully uh it was illustrative at least on how to do some basic spatial operations. Now I really quickly want to end on some uh notes about uh limitations and kind of future work for for spatial. So so far uh I've been really really focused on the kind of internal infrastructure of spatial like having an efficient representation of geometry internally. Uh also pushing a lot of stuff into ductb core like exposing a lot of APIs internal APIs so we can make use of them in in spatial.

### Future Work

**26:44** · Uh but the plan now like I I managed to land a lot of really big things that I'm I'm very excited about. So the plan now is to kind of build on top of this foundation that we have and provide some of these kind of long awaited features uh like spatial indexes, better projection handling as you saw you have to kind of juggle the prediction information around yourself. Uh that's going to change hopefully soon. Also more functions of course. Uh also the documentation is a little bit lacking.

**27:11** · Um so but we have like a new kind of uh documentation system underways at the labs and of course I want to spend more time to work on better integrations with like go park gio arrow maybe gop pandas as well. In the example I showed you I had to create this geometry into WKT and then feed it into Gopandas. I think in the future uh maybe if like when both Gopandas and DB spatial have better support for Gio arrow you can kind of do that natively and treat Gopana's data frames just as duct can treat normal data frames. Now also of course add better support for spatial in client libraries. Uh it was nice because I could kind of show you now how to create these expressions but it would be also great if Dr. Spatial could provide a lot of these gpatial expressions out of the box uh in as part of the python uh API so you don't have to create them yourself. Now despite this there are uh some uh people that have been kind of building things on top of spatial that I just really quickly like to chat out. So uh there's this project called Quark OSM by Camille Rchiki at Roswav University.

### DuckOSM

**28:14** · Um It's a tool to to work with open street map data. Uh it's provides a lot of like uh convenient uh user features.

**28:23** · Uh automatic download and like selection given a certain bounds. You can export things as gear paret. It exists both as a CLI and a Python module. Uh it's really fast. Uh and yeah, next time you want to extract some of the street map data, I highly recommend to give it a shot. Um, also if you've heard of IBIS, it's actually a project out of uh, Voltron Labs. It's kind of this universal interface to databases and data frames. It has great support for duct in general. Uh, but uh, not Clementi has also been adding uh, support for uh, ductb spatials kind of give spatial expression here. So if you weren't too impressed with the Python relational API and you want something more data framey, then uh, give uh, give IBS a shot. Uh, yeah. Yeah, and they also expose uh Dr. Spatial's like digital integration uh which is pretty nice. Also lastly uh I want to give a a shout out to Dr. Kishenu's spatial data management course. So Kishen is a professor at the University of Tennessee. He runs this course Gioorg 414 about your spatial data management but he's published all the course material available online. So there's like a web book and a YouTube videos. I think there's even like lab exercises.

### IBIS

### Special Data Management Course

**29:36** · Uh I know you guys are all already deep into the gatial sauce but if you want to learn more about Python and GMAP and duct and postgs uh this is a really good uh resource. Uh now of course there are many more things as well I'd like to talk about. I know I saw if you saw Kyle Baron's talk yesterday uh there's like duct support for uh Lawnboard. Uh I think there's a DBER plugin a QBS plugin. I haven't used them myself but there's definitely things happening uh in the space. So quickly to conclude uh ductb is a portable analytics embedded database. It gives you kind of the best of databases and data frames. Uh next time you have trouble installing uh jid give uh the duct special extension a try and uh yeah keep an eye out because there's lots of cool stuff on the way.

### Conclusion

**30:24** · Thank you.

### Questions

**30:33** · Thank you very much, Maxon.

**30:36** · Any questions?

**30:49** · Thank you for the exciting talk. I have one questions. Can you use ND arrays with stock TV and if yes, should you at all?

**30:57** · Sorry. n dimensional arrays like um multi-dimensional arrays.

**31:02** · Um yeah, so I think I guess I want to stand here. Yeah. Um I guess you're asking about raster support, right? I guess you're asking about uh support for raster data maybe. Yeah. So um okay, we actually got a uh really impressive contribution from a third party uh that added support for uh managing raers or at least work in progress support for managing raers through jol in ductb spatial. Um I think I will eventually have a look at merging that. I don't necessarily think that raers are a good fit for Dr. B's execution model. Right. A big problem that I've had to deal with, a big challenge with even just vector geometries is that geometries tend to be pretty big and duct as a vectorzed engine needs to keep a lot of things in memory at the same time. Um, and yeah, raers are a lot bigger than than uh than vectors. Uh, like if you were to load I think the standard vector size inductive is like 248 elements. So if you were to load like 248 uh raers that are like 512 times 512 uh four bands, you're looking at like 2 gigabytes for just a single vector. Uh and DB creates a lot of these. Uh so I don't know. I think we might uh maybe have something in that. I think we might support it soon, but it's it's uh it's going to be like use at your own risk kind of thing. Yeah.

**32:40** · Yeah. I have a question. Um, do you support threedimensional in?

**32:45** · Yes.

**32:46** · Uh, this was one of the big things that I've been working on this spring. Uh, yeah, like postJS, we support Z M and Z M. Uh, also intersection and all these functions.

**32:57** · Uh, if Kios does it, then we do it, too.

**33:00** · \[laughter\] I I don't know. I think intersections are uh probably 2D as far as I can tell in g uh so far. Yeah.

**33:09** · Any more questions?

**33:16** · Okay, that's it. Thank you very much, Max again.